import json
import random  # Import the random module
from messageHeader import MessageHeader
from bundle import Bundle
from genericFHIRresource import GenericFHIRresource
from task import Task
from serviceRequest import ServiceRequest
from organization import OrganizationL1, OrganizationL2
from specimen import Specimen
from binary import BinaryData

class Laboratory:
    def __init__(self):
        # Initialize instance variables
        self.resourcesList = []
        self.serviceRequestReferenceList = []
        self.organizationResourcesWereCreated = False
        self.encounterReference = None
        self.fillerLab = None
        self.performerReference = None
        self.orgL1 = None
        self.orgL2 = None

    def process_message(self, data):
        # Reset instance variables for each new message
        self.__init__()
        
        for entry in data['entry']:
            resource = entry['resource']
            full_url = entry['fullUrl']
            resource_type = resource['resourceType']

            # Process different resource types
            if resource_type == "MessageHeader":
                self.process_message_header(resource, full_url)

            elif resource_type == "Encounter":
                self.encounterReference = full_url
                self.resourcesList.append(GenericFHIRresource(fullUrl=full_url, resourceContent=resource))

            elif resource_type == "ServiceRequest":
                self.process_service_request(resource, full_url)

            elif resource_type == "Specimen":
                self.process_specimen(resource, full_url)
            
            elif resource_type == "AllergyIntolerance":
                # Go on, this resource is not necessary in the response messages
                continue

            else:
                # Generic FHIR resource
                self.resourcesList.append(GenericFHIRresource(fullUrl=full_url, resourceContent=resource))

    def process_message_header(self, resource, full_url, response_code = "ORL"):
        # Extract information from MessageHeader resource
        request_message_code = resource['eventCoding']["code"]
        request_code_number = request_message_code[-3:]
        
        if response_code == "ACK":  
            response_code_number = f"{request_code_number[0]}{int(request_code_number[1:])}"
        else:
            response_code_number = f"{request_code_number[0]}{int(request_code_number[1:]) + 1}"
        #response_code = "ORL" #This is set as an argument
        new_message_code = f"{response_code}^{response_code_number}"
        new_display_code = f"{response_code}^{response_code_number}^{response_code}_{response_code_number}"
        message_header = MessageHeader(new_message_code, new_display_code)
        
        # Extract filler lab information and add MessageHeader to resources list
        self.fillerLab = message_header.ExtractMessageHeaderInfo(resource, initFocus=1)
        self.resourcesList.append(message_header)

    def process_service_request(self, resource, full_url):
        # Process ServiceRequest resource
        self.serviceRequestReferenceList.append(full_url)
        service_request = ServiceRequest(fullUrl=full_url, resourceContent=resource)

        # Create and link OrganizationL1 and OrganizationL2 if not created before
        if not self.organizationResourcesWereCreated:
            self.orgL1 = OrganizationL1(self.fillerLab['L1'])
            orgL1FillerReference = self.orgL1.fullUrl
            self.orgL2 = OrganizationL2(self.fillerLab['L2'], orgL1FillerReference)
            self.performerReference = self.orgL2.fullUrl
            self.organizationResourcesWereCreated = True

        # Link performer in the service request and add to resources list
        service_request.addPerformer(self.performerReference)
        self.resourcesList.append(service_request)

    def process_specimen(self, resource, full_url):
        # Process Specimen resource
        if self.serviceRequestReferenceList:
            specimen = Specimen(fullUrl=full_url, resourceContent=resource)
            
            # Add a random decision for pdfLabel with 50% chance
            pdfLabel = random.choice([True, False])

            # Add pdf label or structured data label
            if pdfLabel:
                pdfIdentifier = specimen.addPDF()
            else: 
                specimen.addLabels()
    
            # Append Speciment to the resource list
            self.resourcesList.append(specimen) 
            
            # If the label is a pdf, append BinaryData to the resource list
            if pdfLabel: 
                binary = BinaryData(pdfIdentifier)
                self.resourcesList.append(binary)

    def generate_task_resources(self, task_statuses):
        # Generate Task resources for each accepted service request and add to resources list
        for idx, service_request_full_url in enumerate(self.serviceRequestReferenceList):
            # Extract task status
            if type(task_statuses) is list:
                task_status = task_statuses[idx]
            elif type(task_statuses) is str:
                task_status = task_statuses

            # initialize task resource
            task = Task(task_status, service_request_full_url, self.encounterReference)
            
            # Add a rejection note
            if task_status == "rejected":
                rejection_note = "This is an example of rejection note"
                task.addNotes(rejection_note)
            # Add a reference to the new Task resource in MessageHeader.focus
            task_reference = {"reference": task.fullUrl}
            self.resourcesList[0].resource['focus'].append(task_reference)
            self.resourcesList.insert(1, task)

    def append_organization_resources(self):
        # Append Organization resources at the end of the list if created
        if self.organizationResourcesWereCreated:
            self.resourcesList.append(self.orgL1)
            self.resourcesList.append(self.orgL2)

    def create_bundle_object(self, profile):
        # Create a Bundle object with the headers
        bundle = Bundle(self.resourcesList, profile)
        return json.loads(bundle.to_json())

    def process_message_for_ack(self, data):
        # Reset instance variables for each new message
        self.__init__()
        
        # Loop all over the resources
        for entry in data['entry']:
            resource = entry['resource']
            full_url = entry['fullUrl']
            resource_type = resource['resourceType']

            # Process the MessageHeader resource
            if resource_type == "MessageHeader":
                self.process_message_header(resource, full_url, "ACK")
                # Remove the 'focus' property from the MessageHeader resource
                self.resourcesList[0].resource.pop('focus', None)
                break
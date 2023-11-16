import json
import random  # Import the random module
from messageHeader import MessageHeader
from bundle import Bundle
from genericFHIRresource import GenericFHIRresource
from task import Task
from serviceRequest import ServiceRequest
from organization import OrganizationL1, OrganizationL2
from specimen import Specimen

class FillerLaboratory:
    def __init__(self):
        # Initialize instance variables
        self.resourcesList = []
        self.serviceRequestReferenceList = []
        self.organizationResourcesWereCreated = False
        self.encounterReference = None
        self.fillerLab = None
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

            else:
                # Generic FHIR resource
                self.resourcesList.append(GenericFHIRresource(fullUrl=full_url, resourceContent=resource))

    def process_message_header(self, resource, full_url):
        # Extract information from MessageHeader resource
        request_message_code = resource['eventCoding']["code"]
        request_code_number = request_message_code[-3:]
        
        response_code_number = f"{request_code_number[0]}{int(request_code_number[1:]) + 1}"
        response_code = "ORL"
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
            performerReference = self.orgL2.fullUrl
            self.organizationResourcesWereCreated = True

        # Link performer in the service request and add to resources list
        service_request.addPerformer(performerReference)
        self.resourcesList.append(service_request)

    def process_specimen(self, resource, full_url):
        # Process Specimen resource
        if self.serviceRequestReferenceList:
            specimen = Specimen(fullUrl=full_url, resourceContent=resource)
            specimen.addLabels()
            self.resourcesList.append(specimen)

    def generate_task_resources(self, task_status):
        # Generate Task resources for each accepted service request and add to resources list
        for service_request_full_url in self.serviceRequestReferenceList:
            task = Task(task_status, service_request_full_url, self.encounterReference)
            
            # Add a rejection note
            if task_status == "rejected":
                reje_note = "This is an example of rejection note"
                task.addNotes(reje_note)
            
            task_reference = {"reference": task.fullUrl}
            self.resourcesList[0].resource['focus'].append(task_reference)
            self.resourcesList.insert(1, task)

    def append_organization_resources(self):
        # Append Organization resources at the end of the list if created
        if self.organizationResourcesWereCreated:
            self.resourcesList.append(self.orgL1)
            self.resourcesList.append(self.orgL2)

    def create_bundle_object(self):
        # Create a Bundle object with the headers
        bundle = Bundle(self.resourcesList)
        return json.loads(bundle.to_json())

    def fillerLabAcceptsAllRequest(self, data):
        # Process the message, generate tasks, append organization resources, and create a bundle
        self.process_message(data)
        self.generate_task_resources("accepted")  # Set task_status to "accepted"
        self.append_organization_resources()
        return self.create_bundle_object()

    def fillerLabRejectsAllRequest(self, data):
        # Process the message, generate tasks, append organization resources, and create a bundle
        self.process_message(data)
        self.generate_task_resources("rejected")  # Set task_status to "rejected"
        self.append_organization_resources()
        return self.create_bundle_object()

    def fillerLabAcceptsRandomRequests(self, data):
        # Process the message, generate tasks with a randomly chosen task_status,
        # append organization resources, and create a bundle
        self.process_message(data)
        random_status = random.choice(["accepted", "rejected"])  # Randomly choose between "accepted" and "rejected"
        self.generate_task_resources(random_status)
        self.append_organization_resources()
        return self.create_bundle_object()

    def fillerSendsPositiveACK(self, data):
        # Process the message and create a bundle
        self.process_message(data)
        return self.create_bundle_object()

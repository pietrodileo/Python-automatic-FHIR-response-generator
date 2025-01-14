import json
import random  # Import the random module
import uuid
from messageHeader import MessageHeader
from bundle import Bundle
from genericFHIRresource import GenericFHIRresource
from task import Task
from serviceRequest import ServiceRequest
from organization import OrganizationL1, OrganizationL2, OrganizationL3, OrganizationL4, OrganizationCodiceLabOMR
from specimen import Specimen
from binary import BinaryData
from operation_outcome import OperationOutcome

class Laboratory:
    def __init__(self):
        # Initialize instance variables
        """
        Initialize instance variables

        self.resourcesList: list of resources
        self.serviceRequestReferenceList: list of references to service request resources
        self.diagnostic_report_reference_list: list of references to diagnostic report resources
        self.organizationResourcesWereCreated: boolean indicating if organization resources were created
        self.encounterReference: reference to the encounter resource
        self.fillerLab: dictionary containing information about the laboratory
        self.performerReference: reference to the performer resource
        self.orgL1: OrganizationL1 instance
        self.orgL2: OrganizationL2 instance
        self.orgL3: OrganizationL3 instance
        self.orgL4: OrganizationL4 instance
        self.orgOMR: OrganizationCodiceLabOMR instance
        self.serviceRequestIntent: list of strings representing the intent of the service request
        """
        self.resourcesList = []
        self.serviceRequestReferenceList = []
        self.diagnostic_report_reference_list = []
        self.organizationResourcesWereCreated = False
        self.encounterReference = None
        self.fillerLab = None
        self.performerReference = None
        self.orgL1 = None
        self.orgL2 = None
        self.orgL3 = None
        self.orgL4 = None
        self.orgOMR = None
        self.serviceRequestIntent = []

    # This is the main method for processing a new request message
    def process_new_request(self, data):
        # Reset instance variables for each new message
        """
        Process a new request message.

        This method processes a new request message, which is a message received from the placer that starts a new order.
        The method resets the instance variables, processes each entry in the bundle, and adds labels to the Specimen resources referred by the ServiceRequest resources.

        Parameters
        ----------
        data : dict
            The JSON representation of the FHIR message received from the placer.

        Returns
        -------
        None
        """
        self.__init__()
        
        # Define a list containing all the Specimen resources that have already been assigned with a label
        specimen_with_label = []
        
        # Process each entry in the bundle
        for entry in data['entry']:
            resource = entry['resource']
            full_url = entry['fullUrl']
            resource_type = resource['resourceType']

            # Process different resource types
            if resource_type == "MessageHeader":
                status = self.process_message_header(resource, full_url)
                if not status:
                    raise ValueError("An error occurred while processing the MessageHeader resource")
                # Extract the link to the Encounter resource
                for ref in resource['focus']:
                    if 'Encounter' in ref['reference']:
                        self.encounterReference = ref['reference']
                        continue

            elif resource_type == "Encounter": # Save EncounterReference in order to link it to the ServiceRequest
                self.encounterReference = full_url
                self.resourcesList.append(GenericFHIRresource(fullUrl=full_url, resourceContent=resource))

            elif resource_type == "ServiceRequest":
                # Save the current intent to the list  
                self.serviceRequestIntent.append(resource['intent'])
                self.process_service_request_for_new_request(resource, full_url)
                # Identify the specimen resources referred by the current ServiceRequest through the specimen array 
                # and add them labels, in structured or pdf format.    
                specimen_array = resource['specimen']
                for specimen in specimen_array:
                    specimen_url = specimen['reference']
                    specimen_idx = self.find_resource_idx(data['entry'], specimen_url)
                    specimen = data['entry'][specimen_idx]['resource']
                    if specimen_url not in specimen_with_label:
                        self.process_specimen_add_label(specimen, specimen_url)
            #elif resource_type == "Specimen":
            #    self.process_specimen_add_label(resource, full_url)
            
            elif resource_type == "AllergyIntolerance":
                # Go on, this resource is not necessary in the response messages
                continue

            else:
                # Generic FHIR resource
                self.resourcesList.append(GenericFHIRresource(fullUrl=full_url, resourceContent=resource))

    # This is the main method for processing a check-in/out message and the other notification messages
    def process_check_in_out(self, data, responseTaskStatus = "accepted"):
        # Reset instance variables for each new message
        self.__init__()
        
        for entry in data['entry']:
            resource = entry['resource']
            full_url = entry['fullUrl']
            resource_type = resource['resourceType']

            # Process different resource types
            if resource_type == "MessageHeader":
                status = self.process_message_header(resource, full_url)
                if not status:
                    raise ValueError("An error occurred while processing the MessageHeader resource")

            #elif resource_type == "Encounter": # Deprecated 30/01/2024
            #    self.encounterReference = full_url
            #    self.resourcesList.append(GenericFHIRresource(fullUrl=full_url, resourceContent=resource))
            elif resource_type == "ServiceRequest":
                # Add the current full_url to the list of the service request 
                self.serviceRequestReferenceList.append(full_url)
                # Save the current intent to the list  
                self.serviceRequestIntent.append(resource['intent'])
                # Check if the current service request was added by the filler. If that's the case, add the PlacerOrderNumber ID to the response
                if resource['intent'] == 'order-filler' or resource['intent'] == 'filler-order':
                    self.add_placer_identifier(resource)                
                # Add the current ServiceRequest resource to the message
                self.resourcesList.append(GenericFHIRresource(fullUrl=full_url, resourceContent=resource))
            elif resource_type == "Task":
                # Go on, this resource will be replaced with a new Task resource
                continue
            else:
                # Generic FHIR resource
                self.resourcesList.append(GenericFHIRresource(fullUrl=full_url, resourceContent=resource))
        # Add new Task resources
        self.generate_task_resources(responseTaskStatus)  
    
    # This is the main method for processing a cancellation message
    def process_cancellation_request(self, data = None):
        # Reset instance variables for each new message
        self.__init__()
        
        for entry in data['entry']:
            resource = entry['resource']
            full_url = entry['fullUrl']
            resource_type = resource['resourceType']

            # Process different resource types
            if resource_type == "MessageHeader":
                status = self.process_message_header(resource, full_url)
                if not status:
                    raise ValueError("An error occurred while processing the MessageHeader resource")

                # Extract the link to the Encounter resource
                for ref in resource['focus']:
                    if 'Encounter' in ref['reference']:
                        self.encounterReference = ref['reference']
                        continue

            #elif resource_type == "Encounter": # Save EncounterReference in order to link it to the ServiceRequest
            #    self.encounterReference = full_url
            #    self.resourcesList.append(GenericFHIRresource(fullUrl=full_url, resourceContent=resource))

            elif resource_type == "ServiceRequest":
                # Save the current intent to the list  
                self.serviceRequestIntent.append(resource['intent'])
                self.serviceRequestReferenceList.append(full_url)
                self.resourcesList.append(GenericFHIRresource(fullUrl=full_url, resourceContent=resource))

            #elif resource_type == "Specimen":
                # self.process_specimen_add_label(resource, full_url)
            
            elif resource_type == "AllergyIntolerance":
                # Go on, this resource is not necessary in the response messages
                continue

            else:
                # Generic FHIR resource
                self.resourcesList.append(GenericFHIRresource(fullUrl=full_url, resourceContent=resource))

    # This is the main method for processing a cancellation message
    def process_modification_request(self, data = None):
        # Reset instance variables for each new message
        self.__init__()
        
        for entry in data['entry']:
            resource = entry['resource']
            full_url = entry['fullUrl']
            resource_type = resource['resourceType']

            # Process different resource types
            if resource_type == "MessageHeader":
                status = self.process_message_header(resource,full_url)
                if not status:
                    raise ValueError("An error occurred while processing the MessageHeader resource")

                # Extract the link to the Encounter resource
                for ref in resource['focus']:
                    if 'Encounter' in ref['reference']:
                        self.encounterReference = ref['reference']
                        continue

            #elif resource_type == "Encounter": # Save EncounterReference in order to link it to the ServiceRequest
            #    self.encounterReference = full_url
            #    self.resourcesList.append(GenericFHIRresource(fullUrl=full_url, resourceContent=resource))

            elif resource_type == "ServiceRequest":
                # add to the list just the modified service requests and not the older one, referred in the replaces property
                if 'replaces' in resource.keys():
                    self.serviceRequestReferenceList.append(full_url)
                    self.serviceRequestIntent.append(resource['intent'])
                # However, add both the resources to the bundle
                self.resourcesList.append(GenericFHIRresource(fullUrl=full_url, resourceContent=resource))

            #elif resource_type == "Specimen":
                # self.process_specimen_add_label(resource, full_url)
            
            elif resource_type == "AllergyIntolerance":
                # Go on, this resource is not necessary in the response messages
                continue

            else:
                # Generic FHIR resource
                self.resourcesList.append(GenericFHIRresource(fullUrl=full_url, resourceContent=resource))

    # This is the main method for processing the results
    def process_results_and_reports(self, data, responseTaskStatus = "accepted"):
        # Reset instance variables for each new message
        self.__init__()
        
        for entry in data['entry']:
            resource = entry['resource']
            full_url = entry['fullUrl']
            resource_type = resource['resourceType']

            # Process different resource types
            if resource_type == "MessageHeader":
                # Identify the message code to send back the correct one
                message_code = resource['eventCoding']['code']
                parts = message_code.split('^')
                message_code_prefix = parts[0]
                message_code_suffix = parts[1]
                if message_code_suffix == "T02":
                    message_code_suffix = "T06"
                status = self.process_message_header(resource, full_url, message_code_prefix, message_code_suffix)
                if not status:
                    raise ValueError("An error occurred while processing the MessageHeader resource")

            elif resource_type == "DiagnosticReport":
                # Add the current full_url to the list of the service request
                self.diagnostic_report_reference_list.append(full_url)
                # Add the current ServiceRequest resource to the message
                self.resourcesList.append(GenericFHIRresource(fullUrl=full_url, resourceContent=resource))
            elif resource_type == "Task":
                # Go on, this resource will be replaced with a new Task resource
                continue
            else:
                # Generic FHIR resource
                self.resourcesList.append(GenericFHIRresource(fullUrl=full_url, resourceContent=resource))
        # Add new Task resources
        self.generate_task_for_report(responseTaskStatus)  

    def process_message_header(self, resource, full_url, response_code = "ORL", response_code_number = "", destination_omr_lab_code = ""):
        try:
            # Extract information from MessageHeader resource
            request_message_code = resource['eventCoding']["code"]
            request_code_number = request_message_code[-3:]
            # Calculate response_code_number
            if response_code_number == "":
                if response_code == "ACK":  
                    response_code_number = f"{request_code_number[0:]}"
                else:
                    response_code_number = f"{request_code_number[0]}{int(request_code_number[1:]) + 1}"
            # Calculate new message code
            new_message_code = f"{response_code}^{response_code_number}"
            new_display_code = f"{response_code}^{response_code_number}^{response_code}_{response_code_number}"
            message_header = MessageHeader(new_message_code, new_display_code)
            # Extract filler lab information and add MessageHeader to resources list
            fillerLab = message_header.ExtractMessageHeaderInfo(resource, initFocus=1, destination_omr_lab_code = destination_omr_lab_code)
            # check if the function returned an error
            if fillerLab == None:
                raise ValueError("Error in the extraction of the filler lab information")
            else: 
                self.fillerLab = fillerLab
            self.resourcesList.append(message_header)
            return True
        except Exception as e:
            print(f"Error processing MessageHeader: {str(e)}")
            return False


    def process_service_request_for_new_request(self, resource, full_url):
        # Process ServiceRequest resource
        self.serviceRequestReferenceList.append(full_url)
        service_request = ServiceRequest(fullUrl=full_url, resourceContent=resource)

        # Create and link the Organizations resources if not already done
        if not self.organizationResourcesWereCreated:
            self.orgL1 = OrganizationL1(self.fillerLab['L1'])
            orgL1FillerReference = self.orgL1.fullUrl
            self.orgL2 = OrganizationL2(self.fillerLab['L2'], orgL1FillerReference)
            orgL2FillerReference = self.orgL2.fullUrl
            self.orgL3 = OrganizationL3(self.fillerLab['L3'], orgL2FillerReference)
            orgL3FillerReference = self.orgL3.fullUrl
            self.orgL4 = OrganizationL4(self.fillerLab['L4'], orgL3FillerReference)
            orgL4FillerReference = self.orgL4.fullUrl
            self.orgOMR = OrganizationCodiceLabOMR(self.fillerLab['CodiceLaboratorioOMR'], orgL4FillerReference)
            self.performerReference = self.orgOMR.fullUrl
            self.organizationResourcesWereCreated = True

        # Link performer in the service request and add to resources list
        service_request.addPerformer(self.performerReference)
        self.resourcesList.append(service_request)

        # If the Encounter is not linked, create a reference
        if 'encounter' not in service_request.resource.keys():
            if self.encounterReference: 
                # If a reference to the Encounter was previously found
                service_request.resource['encounter'] = {
                    "reference": f"{self.encounterReference}",
                    "display": "Informazioni Richiesta Lab"
                }

    def process_specimen_add_label(self, resource, full_url):
        # Process Specimen resource
        #if self.serviceRequestReferenceList:
            specimen = Specimen(fullUrl=full_url, resourceContent=resource)
            
            # Add a random decision for pdfLabel with 50% chance
            pdfLabel = random.choice([True, False])

            # Add pdf label or structured data label
            if pdfLabel:
                pdfIdentifier = specimen.addPDF()
            else: 
                specimen.addLabels()
                for service_URL in self.serviceRequestReferenceList:
                    for curr_resource in self.resourcesList:
                        # Look for a service request
                        if curr_resource.fullUrl == service_URL:
                            curr_resource.addServiceTypeLabels()
                
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

            # extract current service request intent
            curr_intent = self.serviceRequestIntent[idx]
            
            # initialize task resource
            task = Task(task_status, service_request_full_url, curr_intent) #, self.encounterReference) Deprecated encounterReference 30/01/2024
            
            # Add a rejection note
            if task_status == "rejected":
                rejection_note = "This is an example of rejection note"
                task.addNotes(rejection_note)
            # Add a reference to the new Task resource in MessageHeader.focus
            task_reference = {"reference": task.fullUrl}
            self.resourcesList[0].resource['focus'].append(task_reference)
            self.resourcesList.insert(1, task)

    def generate_task_for_report(self, task_statuses):
        # Generate Task resources for each accepted service request and add to resources list
        for idx, full_url in enumerate(self.diagnostic_report_reference_list):
            # Extract task status
            if type(task_statuses) is list:
                task_status = task_statuses[idx]
            elif type(task_statuses) is str:
                task_status = task_statuses
            
            # initialize task resource
            task = Task(task_status, full_url)
            
            # Add a rejection note
            if task_status == "rejected":
                rejection_note = "This is an example of rejection note"
                task.addNotes(rejection_note)
                
            # Add a reference to the new Task resource in MessageHeader.focus
            task_reference = {"reference": task.fullUrl}
            self.resourcesList[0].resource['focus'].append(task_reference)
            self.resourcesList.insert(1, task)

    def add_placer_identifier(self, resource):
        placer_order_number_assigned = False

        # Check if the placer order number is defined
        for identifier in resource.get('identifier', []):
            if identifier.get('system') == 'https://fhir.siss.regione.lombardia.it/sid/PlacerOrderNumber':
                placer_order_number_assigned = True
                break

        # If not, assign a new placer order number
        if not placer_order_number_assigned:
            placer_order_number = str(uuid.uuid4())
            new_identifier = {'value': placer_order_number,
                                'system': 'https://fhir.siss.regione.lombardia.it/sid/PlacerOrderNumber'}
            resource.setdefault('identifier', []).append(new_identifier)

    def append_organization_resources(self):
        # Append Organization resources at the end of the list if created
        if self.organizationResourcesWereCreated:
            self.resourcesList.append(self.orgL1)
            self.resourcesList.append(self.orgL2)
            self.resourcesList.append(self.orgL3)
            self.resourcesList.append(self.orgL4)
            self.resourcesList.append(self.orgOMR)

    def create_bundle_object(self, profile):
        # Create a Bundle object with the headers
        """
        Create a Bundle object with the headers.

        This method takes a profile as an argument and creates a Bundle object with the
        resources in the instance variable 'resourcesList'. The Bundle object is then
        converted to JSON and returned.

        Parameters
        ----------
        profile : str
            The profile of the Bundle resource.

        Returns
        -------
        dict
            A dictionary representing the Bundle resource in JSON format.
        """
        bundle = Bundle(self.resourcesList, profile)
        return json.loads(bundle.to_json())

    def process_message_for_ack(self, data):
        # Reset instance variables for each new message
        """
        Process a positive acknowledgment (ACK) message.

        This method processes a given FHIR message to generate an ACK response. It
        resets the instance variables, processes the MessageHeader resource to
        update its response code, and adds an 'response' property indicating the
        acceptance.

        Parameters
        ----------
        data : dict
            The JSON representation of the FHIR message to be processed.

        Returns
        -------
        None
        """
        try: 
            self.__init__()
            
            # extract the assigner before the loop
            assigner_omr_lab_code = self.find_assigner_OMR_lab_code(data['entry'])
            
            # Loop all over the resources
            for entry in data['entry']:
                resource = entry['resource']
                full_url = entry['fullUrl']
                resource_type = resource['resourceType']

                # Process the MessageHeader resource
                if resource_type == "MessageHeader":
                    # Identify the message code to send back the correct one
                    message_code = resource['eventCoding']['code']
                    parts = message_code.split('^')
                    message_code_prefix = parts[0]
                    message_code_suffix = parts[1]
                    message_header_id = resource['id']
                    # Update the MessageHeader resource
                    status = self.process_message_header(resource, full_url, response_code="ACK", response_code_number=message_code_suffix, destination_omr_lab_code = assigner_omr_lab_code)
                    if not status:
                        raise ValueError("An error occurred while processing the MessageHeader resource")
                    # Remove the 'focus' property from the MessageHeader resource
                    self.resourcesList[0].resource.pop('focus', None)
                    # Add the response property to the MessageHeader resource
                    self.resourcesList[0].resource['response'] = {
                        "identifier": message_header_id,
                        "code": "ok"
                    }
                    break
            return True
        except Exception as e:
            print(f"Error processing the message: {str(e)}")
            return False

    def process_message_for_nack(self, data, error_code = "fatal-error", diagnostics = "Generic Error Description"):
        # Reset instance variables for each new message
        """
        Process a negative acknowledgment (NACK) message.

        This method processes a given FHIR message to generate a NACK response. It
        resets the instance variables, processes the MessageHeader resource to
        update its response code, and adds an OperationOutcome resource indicating
        the error detail.

        Parameters
        ----------
        data : dict
            The JSON representation of the FHIR message to be processed.
        error_code : str, optional
            The error code to be set in the MessageHeader response (default is "fatal-error").
        diagnostics : str, optional
            The diagnostics message to be included in the OperationOutcome resource 
            (default is "Generic Error Description").

        Returns
        -------
        None
        """
        self.__init__()
        
        # Loop all over the resources
        for entry in data['entry']:
            resource = entry['resource']
            full_url = entry['fullUrl']
            resource_type = resource['resourceType']

            # Process the MessageHeader resource
            if resource_type == "MessageHeader":
                # Identify the message code to send back the correct one
                message_code = resource['eventCoding']['code']
                parts = message_code.split('^')
                message_code_prefix = parts[0]
                message_code_suffix = parts[1]
                message_header_id = resource['id']
                # Update the MessageHeader resource
                status = self.process_message_header(resource, full_url, response_code="ACK", response_code_number=message_code_suffix)
                if not status:
                    raise ValueError("An error occurred while processing the MessageHeader resource")

                # Remove the 'focus' property from the MessageHeader resource
                self.resourcesList[0].resource.pop('focus', None)
                # Add the response property to the MessageHeader resource
                self.resourcesList[0].resource['response'] = {
                    "identifier": message_header_id,
                    "code": error_code
                }
                break
        
        # Add an operation outcome resource
        operation_outcome = OperationOutcome()
        operation_outcome.addIssue(diagnostics)
        # Add a reference to the OperationOutcome resource in MessageHeader.response
        self.resourcesList[0].resource['response']['details'] = [
            {
                "reference": operation_outcome.fullUrl
            }
        ]
        # Add the OperationOutcome resource at the end of the list of the response message
        self.resourcesList.append(operation_outcome)
        
    def find_resource_idx(self, resources, full_url):
        """
        Find the index of a resource in a list of resources based on its full URL.

        Parameters:
            resources (List[Resource]): A list of resources to search through.
            full_url (str): The full URL of the resource to find.

        Returns:
            int: The index of the resource in the list, or -1 if it is not found.
        """
        for idx, resource in enumerate(resources):
            if resource['fullUrl'] == full_url:
                return idx
            
    def find_assigner_OMR_lab_code(self, resources):
        """
        Find the assigner OMR lab code looking to the Organization resource referred by the Encounter in the assigner property.

        Parameters:
            resources (List[Resource]): A list of resources to search through.

        Returns:
            str: The assigner OMR lab code, or None if it is not found.
        """
        try: 
            for resource in resources:
                if resource['resource']['resourceType'] == "Encounter":
                    for identifier in resource['resource']['identifier']:
                        Organization_url = identifier['assigner'].get('reference', None)
                        continue
            
            if Organization_url:
                idx = self.find_resource_idx(resources, Organization_url)
                organization = resources[idx]['resource']
                identifier = organization['identifier'][0]
                if identifier.get('system') == 'https://fhir.siss.regione.lombardia.it/sid/codiceLaboratorioOMR':
                    omr_lab_code = identifier.get('value', None)
                    return omr_lab_code
        except Exception as e:
            print(f"Error while extracting the assigner OMR lab code: {str(e)}")
            return None
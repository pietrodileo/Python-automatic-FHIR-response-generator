import json
from messageHeader import MessageHeader
from bundle import Bundle
from genericFHIRresource import GenericFHIRresource
from task import Task
from serviceRequest import ServiceRequest
from organization import OrganizationL1, OrganizationL2
from specimen import Specimen

class FillerLaboratory:
    def fillerLabAcceptsAllRequest(self, data):
        # Extract resources from the data
        resourcesList = []
        serviceRequestReferenceList = []
        organizationResourcesWereCreated = False
        encounterReference = None

        # Process incoming message
        for entry in data['entry']:
            resource = entry['resource']
            fullUrl = entry['fullUrl']
            resourceType = resource['resourceType']

            if resourceType == "MessageHeader":
                # Create a MessageHeader object
                messageHeader = MessageHeader("O21 OML", "Accettazione prestazione")
                # Extract information from the resource and assign it to the object
                fillerLab = messageHeader.ExtractMessageHeaderInfo(resource, initFocus = 1)
                # Add the resource to the list of headers
                resourcesList.append(messageHeader)

            elif resourceType == "Encounter":
                encounterReference = fullUrl
                resourcesList.append(GenericFHIRresource(fullUrl=fullUrl, resourceContent=resource))

            elif resourceType == "ServiceRequest":
                # Add the reference to the list
                serviceRequestReferenceList.append(fullUrl)
                # Create a ServiceRequest object
                serviceRequest = ServiceRequest(fullUrl=fullUrl, resourceContent=resource)

                # If at least one service request is being accepted,
                # create the resources OrganizationL1 and OrganizationL2
                # of the filler laboratory and link them in the service request
                if not organizationResourcesWereCreated:
                    orgL1 = OrganizationL1(fillerLab['L1'])
                    orgL1FillerReference = orgL1.fullUrl
                    orgL2 = OrganizationL2(fillerLab['L2'], orgL1FillerReference)
                    performerReference = orgL2.fullUrl
                    organizationResourcesWereCreated = True
                # Link performer in the service request
                serviceRequest.AddPerformer(performerReference)
                resourcesList.append(serviceRequest)

            elif resourceType == "Specimen":
                # Add the labels to the Specimen resources
                if serviceRequestReferenceList:
                    specimen = Specimen(fullUrl=fullUrl, resourceContent=resource)
                    specimen.AddLabels()
                    resourcesList.append(specimen)

            else:
                # Add other resources
                resourcesList.append(GenericFHIRresource(fullUrl=fullUrl, resourceContent=resource))

        # Generate Task resources (only here I can ensure that both serviceRequestFullUrls and encounterReference were found)
        taskStatus = "accepted"
        for serviceRequestFullUrl in serviceRequestReferenceList:
            task = Task(taskStatus, serviceRequestFullUrl, encounterReference)
            # insert the Task Url inside the focus property of the Message Header
            taskReference = {
                "reference": task.fullUrl
            }
            resourcesList[0].resource['focus'].append(taskReference)
            # Insert the Task resource after the MessageHeader
            resourcesList.insert(1, task)

        # Append Organization resources at the end of the list
        if organizationResourcesWereCreated:
            resourcesList.append(orgL1)
            resourcesList.append(orgL2)

        # Create a Bundle object with the headers
        bundle = Bundle(resourcesList)

        # Convert the object to a JSON string and return it
        return json.loads(bundle.to_json())  # Convert to dict for compatibility with Flask jsonify


    def fillerSendsPositiveACK(self, data):
        # Extract resources from the data
        resourcesList = []

        # Process incoming message
        for entry in data['entry']:
            resource = entry['resource']
            #fullUrl = entry['fullUrl']
            resourceType = resource['resourceType']

            if resourceType == "MessageHeader":
                # Create a MessageHeader object
                messageHeader = MessageHeader("O21 ACK", "ACK")
                # Extract information from the resource and assign it to the object
                messageHeader.ExtractMessageHeaderInfo(resource, initFocus = 0)
                # Add the resource to the list of headers
                resourcesList.append(messageHeader)

            else:
                continue

        # Create a Bundle object with the headers
        bundle = Bundle(resourcesList)

        # Convert the object to a JSON string and return it
        return json.loads(bundle.to_json())  # Convert to dict for compatibility with Flask jsonify

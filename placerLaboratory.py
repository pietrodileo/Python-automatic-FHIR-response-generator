import json
from messageHeader import MessageHeader
from bundle import Bundle
from genericFHIRresource import GenericFHIRresource
from task import Task

class PlacerLaboratory:
    def placerSendsPositiveACK(self, data):
        # Extract resources from the data
        resourcesList = []

        # Process incoming message
        for entry in data['entry']:
            resource = entry['resource']
            #fullUrl = entry['fullUrl']
            resourceType = resource['resourceType']

            if resourceType == "MessageHeader":
                # Extract request message code
                requestMessageCode = resource['eventCoding']["code"]
                requestCodeNumber = requestMessageCode[-3:]
                
                # Create a message code for the response
                responseCode = "ACK"
                newMessageCode = f"{responseCode}^{requestCodeNumber}"
                newDisplayCode = f"{responseCode}^{requestCodeNumber}^{responseCode}_{requestCodeNumber}"

                # Create a MessageHeader object
                messageHeader = MessageHeader(newMessageCode, newDisplayCode)

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

    def sendsCheckInResponse(self, data, responseTaskStatus = "accepted"):
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
                # Extract request message code
                requestMessageCode = resource['eventCoding']["code"]
                requestCodeNumber = requestMessageCode[-3:]
                
                # Create a message code for the response
                responseCodeNumber = f"{requestCodeNumber[0]}{int(requestCodeNumber[1:])+1}"
                responseCode = "ORL"
                newMessageCode = f"{responseCode}^{responseCodeNumber}"
                newDisplayCode = f"{responseCode}^{responseCodeNumber}^{responseCode}_{responseCodeNumber}"

                # Create a MessageHeader object
                messageHeader = MessageHeader(newMessageCode, newDisplayCode)
                # Extract information from the resource and assign it to the object
                fillerLab = messageHeader.ExtractMessageHeaderInfo(resource, initFocus = 1)
                # Add the resource to the list of headers
                resourcesList.append(messageHeader)

            elif resourceType == "Task":
                # extract Task resource
                task = GenericFHIRresource(fullUrl=fullUrl, resourceContent=resource)
                # replace Task status
                task.resource['status'] = responseTaskStatus
                # Add the resource to the list of headers
                resourcesList.append(task)
                # add the Task Url inside the focus property of the Message Header
                taskReference = {
                    "reference": fullUrl
                }
                resourcesList[0].resource['focus'].append(taskReference)
            else:
                # Add other resources
                resourcesList.append(GenericFHIRresource(fullUrl=fullUrl, resourceContent=resource))

        # Create a Bundle object with the headers
        bundle = Bundle(resourcesList)

        # Convert the object to a JSON string and return it
        return json.loads(bundle.to_json())  

    def sendsCheckInConfirmation(self, data):
        return self.sendsCheckInResponse(data, "accepted")
        
    def sendsCheckInRejection(self, data):
        return self.sendsCheckInResponse(data, "rejected")
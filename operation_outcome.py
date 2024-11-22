import json
import uuid
from genericFHIRresource import GenericFHIRresource

class OperationOutcome(GenericFHIRresource):
    def __init__(self):
        # Create an OperationOutcome resource associated with the linked service request
        opOut_uid = str(uuid.uuid4())
        fullUrl = "OperationOutcome/" + opOut_uid
        self.fullUrl = fullUrl
        self.resource = {
            "resourceType": "OperationOutcome",
            "id": opOut_uid
        }
        
    def addIssue(self, diagnostics = "Generic Error Description"):
        # If it does not exist, create a new entry
        if 'issue' not in self.resource:
            self.resource['issue'] = []
        # Add the issue to the OperationOutcome resource
        new_issue = {
            "severity":"error",
            "code":"invalid",
            "details":{
                "text": diagnostics
            },
            "diagnostics": diagnostics
        }
        self.resource['issue'].append(new_issue)
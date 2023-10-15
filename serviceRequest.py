import json
import uuid
from genericFHIRresource import GenericFHIRresource

class ServiceRequest(GenericFHIRresource):
    def __init__(self, fullUrl, resourceContent):
        self.fullUrl = fullUrl
        # Update the service request object with an existing resource
        self.resource = resourceContent
        # Declare a filler UID
        sr_filler_uid = str(uuid.uuid4()) 
        # Modify the identifier
        self.resource['identifier'].append(
            {
                "system": "https://fhir.siss.regione.lombardia.it/sid/FillerOrderNumber",
                "value": sr_filler_uid
            }
        )
        
    def AddPerformer(self, performerReference):
        self.resource['performer'] =  [
            {
                "reference": performerReference
            }
        ]        
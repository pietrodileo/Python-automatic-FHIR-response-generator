import json
import uuid
from genericFHIRresource import GenericFHIRresource
from datetime import datetime

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
        
    def addPerformer(self, performerReference):
        self.resource['performer'] =  [
            {
                "reference": performerReference
            }
        ]   
        
    def addOccurrencePeriodStart(self):
        # create a datetime string in format "2022-11-16T14:59:37+01:00"
        dt = datetime.now()
        # Formatta la stringa nel formato richiesto
        datetime_string = dt.strftime("%Y-%m-%dT%H:%M:%S%z")
        self.resource['authoredOn'] = datetime_string
        self.resource['occurrencePeriod'] = { "start": datetime_string }        
        
    def addServiceTypeLabels(self):
        self.resource['extension'] =  [
            {
                "url": "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabServiceRequestTipoPrestazione",
                "valueString": "LAB-TipoPrestazione"
            }
        ]   

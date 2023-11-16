import json
import uuid
from genericFHIRresource import GenericFHIRresource

class Task(GenericFHIRresource):
    def __init__(self, taskStatus, serviceRequestReference, encounterReference):
        # Create a Task resource associated to the linked service request  
        task_uid = str(uuid.uuid4()) 
        fullUrl = "Task/" + task_uid
        self.fullUrl = fullUrl
        self.resource = {
            "resourceType": "Task",
            "id": task_uid,
            "meta": {
                "profile": [
                    "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabTaskStatoRichiesta"
                ],
                "versionId": "1"
            },
            "focus": {
                "reference": serviceRequestReference
            },
            "status": taskStatus,
            "intent": "order",
            #"encounter": {
            #    "reference": encounterReference
            #}
        }
    
    def add_notes(self, note_text):
        # Add a property to the task resource
        self.resource['note'] = [ 
            {
                "text": note_text
            }
        ]
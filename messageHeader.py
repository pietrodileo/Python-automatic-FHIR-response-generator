import json
import uuid
from genericFHIRresource import GenericFHIRresource
import os

class MessageHeader(GenericFHIRresource):
    def __init__(self, codiceMH, displayMH):
        # Create an UUID for the resource
        mh_uid = str(uuid.uuid4()) 
        fullUrl = "MessageHeader/" + mh_uid
        self.fullUrl = fullUrl
        self.resource = {
            "resourceType": "MessageHeader",
            "id": mh_uid,
            "meta": {
                "profile": [
                    "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabMessageHeader"
                ],
                "versionId": "1"
            },
            "eventCoding": {
                "system": "https://fhir.siss.regione.lombardia.it/ValueSet/CodiceEventoMessageHeader",
                "code": codiceMH,
                "display": displayMH
            },
            "destination": {
                "name": "OMR",
                "software": "Reti di laboratori",
                "endpoint": "localhost:52773/fhir/retilab/Omr"
            }
        }
                
    def ExtractMessageHeaderInfo(self, resource):
        # Extract the source code        
        codiceApplicativoSorgente = resource['destination']['name']
        
        # Open a json containing the data of all the laboratories
        my_dir = os.path.dirname(__file__)
        json_file_path = os.path.join(my_dir, 'CensimentoEnti.json')        
        with open(json_file_path, 'r') as file:
            json_censimento = json.load(file)
        
        # Find the information about the filler laboratory
        fillerLab = next((lab for lab in json_censimento if lab["CodiceApplicativo"] == codiceApplicativoSorgente), 0)

        # Assign the extracted parameters to the object
        self.resource['source'] = {
            "name": fillerLab['CodiceApplicativo'],
            "software": fillerLab['NomeStruttura'] + " - " + fillerLab['NomeLaboratorio'],
            #"endpoint": resource['destination']['endpoint']
            "endpoint": fillerLab['Endpoint'] 
        }
        self.resource['response'] = {
            "identifier": resource['id'],
            "code": "ok"
        }
        
        # Initialize the focus property
        self.resource['focus'] = []
        
        return fillerLab
    

import json
import uuid
from genericFHIRresource import GenericFHIRresource
import os
import datetime

class MessageHeader(GenericFHIRresource):
    def __init__(self, codiceMH, displayMH):
        # Create an UUID for the resource
        mh_uid = str(uuid.uuid4())
        fullUrl = "MessageHeader/" + mh_uid
        # Get the current UTC time
        now = datetime.datetime.utcnow()
        # Format the timestamp in ISO 8601 format
        timestamp = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        # Define JSON message
        self.fullUrl = fullUrl
        self.resource = {
            "resourceType": "MessageHeader",
            "id": mh_uid,
            "meta": {
                "profile": [
                    "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabMessageHeader"
                ],
                "versionId": "1",
                "lastUpdated": timestamp
            },
            "eventCoding": {
                "system": "https://fhir.siss.regione.lombardia.it/ValueSet/CodiceEventoMessageHeader",
                "code": codiceMH,
                "display": displayMH
            },
            "destination": [
                    {
                    "name": "OMR",
                    "software": "Reti di laboratori",
                    "endpoint": "localhost:52773/fhir/retilab/Omr"
                }
            ]
        }

    def ExtractMessageHeaderInfo(self, resource, initFocus, destination_omr_lab_code = ""):
        try: 
            # Load a json containing the data of all the laboratories
            my_dir = os.path.dirname(__file__)
            json_file_path = os.path.join(my_dir, 'CensimentoEnti.json')
            with open(json_file_path, 'r') as file:
                json_censimento = json.load(file)

            if destination_omr_lab_code != "":
                # use the destination_omr_lab_code to extract the information from the CensimentoEnti.json file
                destinationLab = [lab for lab in json_censimento if (lab["CodiceLaboratorioOMR"]) == destination_omr_lab_code]
            else:
                # Extract the source code
                destination = resource.get('destination', None)
                if destination == None:
                    raise KeyError("destination is missing in the MessageHeader.")
                else: 
                    destination_name = destination[0].get('software', None)
                    if destination_name == None:
                        raise KeyError("destination_name is missing in the destination.")
                # Find the information about the filler laboratory
                destinationLab = [lab for lab in json_censimento if (lab["NomeStruttura"]+" - "+lab["NomeLaboratorio"]) == destination_name]

            # Check if the destination laboratory was found
            if not destinationLab:
                raise ValueError("It was impossible to find the destination laboratory in the CensimentoEnti.json file.")
            else:
                destinationLab = destinationLab[0]
            
            # Assign the extracted parameters to the object
            self.resource['source'] = {
                "name": destinationLab['CodiceApplicativo'],
                "software": destinationLab['NomeStruttura'] + " - " + destinationLab['NomeLaboratorio'],
                #"endpoint": resource['destination']['endpoint']
                "endpoint": destinationLab['Endpoint']
            }
            self.resource['response'] = {
                "identifier": resource['id'],
                "code": "ok"
            }

            if initFocus:
                # Initialize the focus property
                self.resource['focus'] = []

            return destinationLab
        
        except Exception as e:
            print(f"Error while extracting info from MessageHeader: {str(e)}")
            return None
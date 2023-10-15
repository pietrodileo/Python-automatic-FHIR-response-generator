import json
import uuid
from genericFHIRresource import GenericFHIRresource

class Specimen(GenericFHIRresource):
    def __init__(self, fullUrl, resourceContent):
        self.fullUrl = fullUrl
        # Update the service request object with an existing resource
        self.resource = resourceContent
        
    def AddLabels(self):
        # Modify the identifier
        self.resource['extension'] = []
        self.resource['extension'].append(                
            {
                "url": "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabSpecimenIstruzioniEtichette",
                "extension": [
                    {
                        "url": "identificativoNumeroEtichetta",
                        "valueString": "TBD"
                    },
                    {
                        "url": "numeroRigaEtichetta",
                        "valueInteger": "TBD"
                    },
                    {
                        "url": "codiceEtichetta",
                        "valueString": "TBD"
                    },
                    {
                        "url": "categoriaEtichetta",
                        "valueString": "TBD"
                    },
                    {
                        "url": "contenutoTipoRigaEtichetta",
                        "valueCodeableConcept": {
                            "coding": [
                                {
                                    "system": "TBD",
                                    "code": "TBD",
                                    "display": "TBD"
                                }
                            ]
                        }
                    },
                    {
                        "url": "indicazioniFormattazione",
                        "valueString": "TBD"
                    },
                    {
                        "url": "numeroCopie",
                        "valueInteger": "TBD"
                    },
                    {
                        "url": "ampiezzaBarcode",
                        "valueQuantity": {
                            "value": 3,
                            "unit": "ch"
                        }
                    },
                    {
                        "url": "altezzaBarcode",
                        "valueString": "TBD"
                    },
                    {
                        "url": "dimensioneEffettivaBarcode",
                        "valueString": "TBD"
                    },
                    {
                        "url": "tipoBarcode",
                        "valueString": "TBD"
                    },
                    {
                        "url": "fillerPattern",
                        "valueString": "TBD"
                    },
                    {
                        "url": "fillerSide",
                        "valueString": "TBD"
                    },
                    {
                        "url": "bordaturaBarcode",
                        "valueString": "TBD"
                    },
                    {
                        "url": "codiceCampione",
                        "valueString": "TBD"
                    },
                    {
                        "url": "descrizioneEtichetta",
                        "valueString": "TBD"
                    }
                ]
            }
        )

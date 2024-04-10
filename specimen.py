import json
import uuid
from genericFHIRresource import GenericFHIRresource

class Specimen(GenericFHIRresource):
    def __init__(self, fullUrl, resourceContent):
        self.fullUrl = fullUrl
        # Update the object with an existing resource
        self.resource = resourceContent
        # il profile va corretto con "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabSpecimenCampioneDaPrelevareIstruzioniEtichette
    
    def addPDF(self):
        pdfIdentifier = str(uuid.uuid4())
        specimenIdentifier = "SpecimenIdentifier" #str(uuid.uuid4())
        self.resource['note'] = [
            {
                "text": "campione fragile"
            }
        ]
        self.resource['extension'] = [
            {
                "url": "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabSpecimenEtichettaPDF",
                "valueReference": {
                    "reference": "Binary/"+pdfIdentifier
                }
            }
        ]
        self.resource['identifier'] = [
            {
                "system": "https://fhir.siss.regione.lombardia.it/sid/SpecimenIdentifier",
                "value": specimenIdentifier
            }
        ]
        return pdfIdentifier
    
    def addLabels(self):
        specimenIdentifier = "SpecimenIdentifier" #str(uuid.uuid4())
        # Add label and label information
        self.resource['identifier'] = [
            {
                "system": "https://fhir.siss.regione.lombardia.it/sid/SpecimenIdentifier",
                "value": specimenIdentifier
            }
        ]
        self.resource['note'] = [
            {
                "text": "campione fragile"
            }
        ]
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

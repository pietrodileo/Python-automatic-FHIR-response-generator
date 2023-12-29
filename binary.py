import json
import uuid
from genericFHIRresource import GenericFHIRresource

class BinaryData(GenericFHIRresource):
    def __init__(self, pdfIdentifier):
        with open("pdfEncodedBase64Example.txt", "r") as input_file:
            pdfEncodedBase64Example = input_file.read()
            self.fullUrl = "Binary/"+pdfIdentifier
            self.resource = {
                "resourceType": "Binary",
                "id": pdfIdentifier,
                "meta": {
                    "versionId": "1",
                    "profile":  [
                        "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabBinaryDocumentoPDFEncodedBase64"
                    ]
                },
                "contentType": "application/pdf",
                "data": pdfEncodedBase64Example
            }
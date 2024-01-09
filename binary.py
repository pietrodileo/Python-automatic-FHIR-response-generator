import os
from genericFHIRresource import GenericFHIRresource

class BinaryData(GenericFHIRresource):
    def __init__(self, pdfIdentifier):
        # Define filepath (for deploy)
        filename = "pdfEncodedBase64Example.txt"
        this_directory = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(this_directory, filename)   
        
        # Open file and create a Binary resource
        with open(filepath, "r") as input_file:
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
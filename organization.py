import json
import uuid
from genericFHIRresource import GenericFHIRresource

class Organization(GenericFHIRresource):
    def __init__(self):
        # Create an Organization resource associated with the linked service request
        org_uid = str(uuid.uuid4())
        fullUrl = "Organization/" + org_uid
        self.fullUrl = fullUrl
        self.resource = {
            "resourceType": "Organization",
            "id": org_uid,
        }

class OrganizationL1(Organization):
    def __init__(self, L1):
        # Call the method __init__ of the parent class (Organization)
        super().__init__()

        resource = {
            "meta": {
                "profile": [
                    "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabOrganizationL1"
                ]
            },
            "identifier": [
                {
                    "system": "https://fhir.siss.regione.lombardia.it/sid/codiceIdentificativoEnte",
                    "value": L1
                }
            ],
            "name": "Denominazione dell'ente L1"
        }
        
        # Update the resource
        self.resource.update(resource)

class OrganizationL2(Organization):
    def __init__(self, L2, OrgL1reference):
        # Call the method __init__ of the parent class (Organization)
        super().__init__()

        resource = {
            "meta": {
                "profile": [
                    "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabOrganizationL2"
                ]
            },
            "identifier": [
                {
                    "system": "https://fhir.siss.regione.lombardia.it/sid/codiceMinisterialePresidio",
                    "value": L2
                }
            ],
            "partOf": {
                    "reference": OrgL1reference
            },
            "name": "Denominazione dell'ente L2"
        }

        # Update the resource
        self.resource.update(resource)

class OrganizationL3(Organization):
    def __init__(self, L3, OrgL2reference):
        # Call the method __init__ of the parent class (Organization)
        super().__init__()

        resource = {
            "meta": {
                "profile": [
                    "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabOrganizationL3"
                ]
            },
            "identifier": [
                {
                    "system": "https://fhir.siss.regione.lombardia.it/sid/codiceMinisterialeReparto",
                    "value": L3
                }
            ],
            "partOf": {
                    "reference": OrgL2reference
            },
            "name": "Denominazione dell'ente L3"
        }

        # Update the resource
        self.resource.update(resource)
        
class OrganizationL4(Organization):
    def __init__(self, L4, OrgL3reference):
        # Call the method __init__ of the parent class (Organization)
        super().__init__()

        resource = {
            "meta": {
                "profile": [
                    "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabOrganizationL4"
                ]
            },
            "identifier": [
                {
                    "system": "https://fhir.siss.regione.lombardia.it/sid/codiceMinisterialeAmbulatorio",
                    "value": L4
                }
            ],
            "partOf": {
                    "reference": OrgL3reference
            },
            "name": "Denominazione dell'ente L4"
        }

        # Update the resource
        self.resource.update(resource)
        
class OrganizationCodiceLabOMR(Organization):
    def __init__(self, CodiceLabOMR, OrgLReference):
        # Call the method __init__ of the parent class (Organization)
        super().__init__()

        resource = {
            "meta": {
                "profile": [
                    "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabOrganizationLaboratorio"
                ]
            },
            "identifier": [
                {
                    "system": "https://fhir.siss.regione.lombardia.it/sid/codiceLaboratorioOMR",
                    "value": CodiceLabOMR
                }
            ],
            "partOf": {
                    "reference": OrgLReference
            },
            "name": "Laboratorio di analisi"
        }

        # Update the resource
        self.resource.update(resource)
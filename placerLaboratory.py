from laboratory import Laboratory

class PlacerLaboratory(Laboratory):
    def __init__(self):
        super().__init__()

    def placerSendsPositiveACK(self, data):
        profile = "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabACK"
        # Send back a positive ACK
        self.process_message_for_ack(data)
        return self.create_bundle_object(profile)
    
    def placerSendsCheckInOutResponse(self, data, responseTaskStatus = "accepted"):
        profile = "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabBundleRispostaCheckInOut"
        self.process_check_in_out(data, responseTaskStatus)
        return self.create_bundle_object(profile)
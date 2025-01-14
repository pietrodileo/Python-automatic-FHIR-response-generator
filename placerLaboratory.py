from laboratory import Laboratory

class PlacerLaboratory(Laboratory):
    def __init__(self):
        super().__init__()
        self.rejectRequest = False

    # Placer methods
    def placerSendsPositiveACK(self, data):
        try:
            profile = "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabACK"
            # Send back a positive ACK
            status = self.process_message_for_ack(data)
            if not status:
                raise Exception("Error processing the message.")
            return self.create_bundle_object(profile)
        except Exception as e:
            print(f"{str(e)}")
            return None
    
    def placerSendsCheckInOutResponse(self, data, responseTaskStatus = "accepted"):
        profile = "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabBundleRispostaCheckInOut"
        if self.rejectRequest:
            responseTaskStatus = "rejected"
        self.process_check_in_out(data, responseTaskStatus)
        return self.create_bundle_object(profile)
    
    def placerManageResultsAndReports(self, data, responseTaskStatus = "accepted"):
        profile = "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabBundleRispostaACK"
        if self.rejectRequest:
            self.process_message_for_nack(data)
        else: 
            self.process_message_for_ack(data)
        return self.create_bundle_object(profile)
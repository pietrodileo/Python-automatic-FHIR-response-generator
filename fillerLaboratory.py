import random
from laboratory import Laboratory

class FillerLaboratory(Laboratory):
    def __init__(self):
        super().__init__()
        # Flag per rifiutare le richieste ricevute
        self.rejectRequest = False

    # Filler lab methods
    def fillerLabAcceptsAllRequest(self, data, responseTaskStatus = "accepted"):
        profile = "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabBundleRispostaNuovaRichiesta"
        if self.rejectRequest:
            responseTaskStatus = "rejected"
        # Process the message, generate tasks, append organization resources, and create a bundle
        self.process_new_request(data)
        self.generate_task_resources(responseTaskStatus)  # Set task_status to "accepted"
        self.append_organization_resources()
        return self.create_bundle_object(profile)

    def fillerLabRejectsAllRequest(self, data, responseTaskStatus = "rejected"):
        profile = "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabBundleRispostaNuovaRichiesta"
        # Process the message, generate tasks, append organization resources, and create a bundle
        self.process_new_request(data)
        self.generate_task_resources(responseTaskStatus)  # Set task_status to "rejected"
        self.append_organization_resources()
        return self.create_bundle_object(profile)

    def fillerLabAcceptsRandomRequests(self, data):
        profile = "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabBundleRispostaNuovaRichiesta"
        # Process the message, generate tasks with a randomly chosen task_status,
        # append organization resources, and create a bundle
        self.process_new_request(data)
        nReq = len(self.serviceRequestReferenceList)
        # Randomly choose between "accepted" and "rejected" status
        random_statuses = [random.choice(["accepted", "rejected"]) for _ in range(nReq)]
        # generate task resources
        self.generate_task_resources(random_statuses)
        self.append_organization_resources()
        return self.create_bundle_object(profile)

    def fillerSendsPositiveACK(self, data):
        profile = "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabACK"
        # Send back a positive ACK
        self.process_message_for_ack(data)
        return self.create_bundle_object(profile)
    
    def fillerSendsCancellationResponse(self,data, responseTaskStatus = "accepted"):
        profile = "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabBundleRispostaNotifica"
        if self.rejectRequest:
            responseTaskStatus = "rejected"
        # Process the message, generate tasks, append organization resources, and create a bundle
        self.process_cancellation_request(data)
        self.generate_task_resources(responseTaskStatus)  # Set task_status to "accepted"
        #self.append_organization_resources()
        return self.create_bundle_object(profile)

    def fillerSendsModificationResponse(self,data, responseTaskStatus = "accepted"):
        profile = "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabBundleRispostaNotifica"
        if self.rejectRequest:
            responseTaskStatus = "rejected"
        # Process the message, generate tasks, append organization resources, and create a bundle
        self.process_modification_request(data)
        self.generate_task_resources(responseTaskStatus) 
        #self.append_organization_resources()
        return self.create_bundle_object(profile)

    def fillerSendsCheckInOutResponse(self, data, responseTaskStatus = "accepted"):
        if self.rejectRequest:
            responseTaskStatus = "rejected"
        return self.process_check_in_out(data, responseTaskStatus)
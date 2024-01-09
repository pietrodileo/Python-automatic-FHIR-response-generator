from laboratory import Laboratory

class FillerLaboratory(Laboratory):
    def __init__(self):
        super().__init__()

    def fillerLabAcceptsAllRequest(self, data):
        profile = "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabBundleRispostaNuovaRichiesta"
        # Process the message, generate tasks, append organization resources, and create a bundle
        self.process_message(data)
        self.generate_task_resources("accepted")  # Set task_status to "accepted"
        self.append_organization_resources()
        return self.create_bundle_object(profile)

    def fillerLabRejectsAllRequest(self, data):
        profile = "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabBundleRispostaNuovaRichiesta"
        # Process the message, generate tasks, append organization resources, and create a bundle
        self.process_message(data)
        self.generate_task_resources("rejected")  # Set task_status to "rejected"
        self.append_organization_resources()
        return self.create_bundle_object(profile)

    def fillerLabAcceptsRandomRequests(self, data):
        profile = "https://fhir.siss.regione.lombardia.it/StructureDefinition/ReteLabBundleRispostaNuovaRichiesta"
        # Process the message, generate tasks with a randomly chosen task_status,
        # append organization resources, and create a bundle
        self.process_message(data)
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
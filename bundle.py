import uuid
import datetime
import json
from genericFHIRresource import GenericFHIRresource

class Bundle(GenericFHIRresource):
    def __init__(self, resources):
        # Create an UUID for the resource
        bundle_uid = str(uuid.uuid4())
        # Get the current UTC time
        now = datetime.datetime.utcnow()
        # Format the timestamp in ISO 8601 format
        timestamp = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        # Construct the bundle
        self.resourceType = "Bundle"
        self.id = bundle_uid
        self.type = "message"
        self.timestamp = timestamp
        self.entry = []
        for resource in resources:
            self.entry.append({
                "fullUrl": resource.fullUrl,
                "resource": resource.resource
            })

    def to_json(self):
        ordered_dict = {
            "resourceType": self.resourceType,
            "id": self.id,
            "type": self.type,
            "timestamp": self.timestamp,
            "entry": self.entry
        }

        return json.dumps(ordered_dict, indent=4)

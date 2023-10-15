import json

class GenericFHIRresource:
    def __init__(self, fullUrl, resourceContent):
        # Create an UUID for the resource
        self.fullUrl = fullUrl
        self.resource = resourceContent
    
    def to_json(self):
        return json.dumps(self.__dict__, indent=4)

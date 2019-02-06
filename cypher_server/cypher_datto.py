from message_response import MessageResponse


class CypherDatto(object):
    def __init__(self, module, url):
        super(CypherDatto, self).__init__()
        self.url = url
        self.intergrate_module(module)

    def intergrate_module(self, module):
        self.module = module
        self.name = module.name
        self.key_type = module.key_type
        self.description = module.description
        self.example = module.example

    def decrypt(self, message, key):
        decrypted_output = None
        if(self.key_type == "none"):
            decrypted_output = self.module.decrypt(message)
        else:
            decrypted_output = self.module.decrypt(key, message)
        return MessageResponse(decrypted_output)

    def encrypt(self, message, key):
        encrypted_output = None
        if(self.key_type == "none"):
            encrypted_output = self.module.encrypt(message)
        else:
            encrypted_output = self.module.encrypt(key, message)
        return MessageResponse(encrypted_output)

    def serialize(self):
        return {
            "name": self.name,
            "keyType": self.key_type,
            "description": self.description,
            "example": self.example,
            "url": self.url
        }

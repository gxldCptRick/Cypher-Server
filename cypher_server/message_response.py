class MessageResponse(object):
    def __init__(self, message):
        super(MessageResponse, self).__init__()
        self.message = message

    def serialize(self):
        return {
            "message": self.message
        }

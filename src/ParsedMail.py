import email

class ParsedMail:
    def __init__(self, header: email.message.Message, body):
        self.header = header
        self.body = body

#import libs
import win32com.client
from email.parser import HeaderParser
import email

class Input:
    def __init__(self, **kwargs):
        self.outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        self.message = self.outlook.OpenSharedItem(r"C:\Users\Ben\OneDrive - Ordina\emailanalyser\testmails\test.msg")
        self.file = open(r"C:\Users\Ben\OneDrive - Ordina\emailanalyser\testmails\test6.eml", encoding="ISO-8859-1")
        self.headermessage = email.message_from_file(self.file)
        self.file.close()
        self.parser = email.parser.HeaderParser()
        self.header = self.parser.parsestr(self.headermessage.as_string())
        
    def printMessage(self):
        print (self.message.SenderName)
        print (self.message.SenderName)
        print (self.message.SenderEmailAddress)
        print (self.message.SentOn)
        print (self.message.To)
        print (self.message.CC)
        print (self.message.BCC)
        print (self.message.Subject)
        print (self.message.Body)
        
    def printHeader(self):
        for h in self.header.items():
            print (h)
        
input = Input()
input.printMessage()
input.printHeader()



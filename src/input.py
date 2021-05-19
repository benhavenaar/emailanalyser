#import libs
import win32com.client
from email.parser import HeaderParser
import email
import re

#classes
class Input:
    #class init variables
    def __init__(self, **kwargs):
        self.file = None
        self.headermessage = None
        self.parser = None
        self.header = None
        self.emailArray = []
        # self.ipAddressRegex = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        self.ipAddressRegex = re.compile(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')
        self.duplicateIPAddresses = {}
         
    def deconstructEmail(self, emailPath):
        self.file = open(emailPath, encoding="ISO-8859-1")
        self.headermessage = email.message_from_file(self.file)
        self.file.close()
        self.parser = email.parser.HeaderParser()
        self.header = self.parser.parsestr(self.headermessage.as_string())
   
    #Append ip addresses found in the email header/body to self.emailArray.
    def findIPAddress(self, emailPath):
        self.deconstructEmail(emailPath)
        for line in self.header.items():
            if self.ipAddressRegex.search(line[1]) == None:
                pass
            else:
                ipAddressValue = tuple(self.ipAddressRegex.findall(line[1]))
                for ipAddressValueSplit in ipAddressValue:
                    if ipAddressValueSplit in self.duplicateIPAddresses:
                        ipNumber = self.duplicateIPAddresses[ipAddressValueSplit]
                    else:
                        self.emailArray.append(ipAddressValueSplit)
                        self.duplicateIPAddresses[ipAddressValueSplit] = ipNumber = len(self.emailArray)-1
        # set([self.emailArray])
        return self.emailArray
        
        
# input = Input()
# # print (input.header)
# input.findIPAddress()
# print(type(input.header))
# # print(input.header.items())
# input.findIPAddress()
# print(input.emailArray)



#import libs
import win32com.client
from email.parser import HeaderParser
import email
import re

#classes
class InputFile:
    #class init variables
    def __init__(self, **kwargs):
        self.file = None
        self.headermessage = None
        self.parser = None
        self.header = None
        self.emailArray = []
        # self.ipAddressRegex = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        self.ipAddressRegex = re.compile(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')
         
    def deconstructEmail(self, emailPath):
        self.file = open(emailPath, encoding="ISO-8859-1")
        self.headermessage = email.message_from_file(self.file)
        self.file.close()
        self.parser = email.parser.HeaderParser()
        self.header = self.parser.parsestr(self.headermessage.as_string())
   
    #Append ip addresses found in the email header/body to self.emailArray. The for and if/else loop in the first Else part is used to filter out duplicates. 
    #First the value found is set to a tuple, then the items will be added iterated over (if multiple ip's in one line exist), then it's added to the duplicateIPAddresses
    #Afterwards if it isn't found in the duplicate list it will be added to self.emailArray. 
    def findIPAddress(self, emailPath):
        self.deconstructEmail(emailPath)
        duplicateIPAddresses = {}
        for line in self.header.items():
            if self.ipAddressRegex.search(line[1]) == None:
                pass
            else:
                ipAddressValue = self.ipAddressRegex.findall(line[1])
                for ipAddressValueSplit in ipAddressValue:
                    if ipAddressValueSplit in duplicateIPAddresses:
                        ipNumber = duplicateIPAddresses[ipAddressValueSplit]
                    else:
                        self.emailArray.append(ipAddressValueSplit)
                        duplicateIPAddresses[ipAddressValueSplit] = ipNumber = len(self.emailArray)-1
        return self.emailArray
        
        
# input = Input()
# # print (input.header)
# input.findIPAddress()
# print(type(input.header))
# # print(input.header.items())
# input.findIPAddress()
# print(input.emailArray)



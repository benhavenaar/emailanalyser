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
        self.emailMessage = None
        self.bodyMessage = None
        self.headerParser = None
        self.bodyParser = None
        self.header = None
        self.body = None
        self.ipAddressHeaderArray = []
        self.urlHeaderArray = []
        self.urlBodyArray = []
        # self.ipAddressRegex = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        self.ipAddressRegex = re.compile(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')
        self.urlRegex = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
         
    def deconstructEmail(self, emailPath):
        self.file = open(emailPath, encoding="ISO-8859-1")
        self.emailMessage = email.message_from_file(self.file)
        self.file.close()
        self.headerParser = email.parser.HeaderParser()
        self.header = self.headerParser.parsestr(self.emailMessage.as_string())
        for payload in self.emailMessage.get_payload():
            try:
                self.body = payload.get_payload()
            except AttributeError:
                self.body = self.emailMessage.get_payload()
 
    #Append ip addresses found in the email header/body to self.emailArray. The for and if/else loop in the first Else part is used to filter out duplicates. 
    #First the value found is set to a tuple, then the items will be added iterated over (if multiple ip's in one line exist), then it's added to the duplicateIPAddresses
    #Afterwards if it isn't found in the duplicate list it will be added to self.emailArray. 
    def findIPAddressInHeader(self, emailPath):
        self.deconstructEmail(emailPath)
        ipAddressArray = self.findContentInHeader(self.ipAddressRegex, self.ipAddressHeaderArray, self.header.items())
        return ipAddressArray
    
    def findURLInHeader(self, emailPath):
        self.deconstructEmail(emailPath)
        urlHeaderArray = self.findContentInHeader(self.urlRegex, self.urlHeaderArray, self.header.items())
        return urlHeaderArray
        
    def findURLInBody(self, emailPath):
        urlBodyArray = self.findContentInHeader(self.urlRegex, self.urlBodyArray, self.body)
        return urlBodyArray
        
    def findContentInHeader(self, regexFilter, contentArray, content):
        duplicateItems = {}
        for line in content:
            for item in range(len(line)):
                if regexFilter.search(line[item]) == None:
                    pass
                else:
                    contentValue = regexFilter.findall(line[item])
                    for contentValueSplit in contentValue:
                        if contentValueSplit in duplicateItems:
                            contentNumber = duplicateItems[contentValueSplit]
                        else:
                            contentArray.append(contentValueSplit)
                            duplicateItems[contentValueSplit] = contentNumber = len(contentArray)-1
        return contentArray
        
# input = Input()
# # print (input.header)
# input.findIPAddress()
# print(type(input.header))
# # print(input.header.items())
# input.findIPAddress()
# print(input.emailArray)



#import libs
import win32com.client
from email.parser import HeaderParser
import email
import re

class Input:
    def __init__(self, **kwargs):
        self.file = open(r"..\testmails\test5.eml", encoding="ISO-8859-1")
        self.headermessage = email.message_from_file(self.file)
        self.file.close()
        self.parser = email.parser.HeaderParser()
        self.header = self.parser.parsestr(self.headermessage.as_string())
        self.emailArray = []
        self.ipAddressRegex = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        
    def printHeader(self):
        for h in self.header.items():
            print (h)
            
    def findIPAddress(self):
        # self.emailArray.append(item for item in self.header.items() if self.ipAddressRegex in item)
        for line in self.header.items():
            # if line[1].search(self.ipAddressRegex):
                # print (line)
            if self.ipAddressRegex.search(line[1]) == None:
                pass
            else:
                self.emailArray.append(self.ipAddressRegex.search(line[1]))
        
input = Input()
# print (input.header)
input.findIPAddress()
print(type(input.header))
# print(input.header.items())
input.findIPAddress()
print(input.emailArray)



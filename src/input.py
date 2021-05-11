#import libs
import win32com.client
from email.parser import HeaderParser
import email
import re

#classes
class Input:
    #class init variables
    def __init__(self, **kwargs):
        self.file = open(r"..\testmails\test5.eml", encoding="ISO-8859-1")
        self.headermessage = email.message_from_file(self.file)
        self.file.close()
        self.parser = email.parser.HeaderParser()
        self.header = self.parser.parsestr(self.headermessage.as_string())
        self.emailArray = []
        self.ipAddressRegex = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        
    
    #Append ip addresses found in the email header/body to self.emailArray. 
    def findIPAddress(self):
        for line in self.header.items():
            print (line)
            if self.ipAddressRegex.search(line[1]) == None:
                pass
            else:
                self.emailArray.append(self.ipAddressRegex.findall(line[1])) #use line[1] as it's the 2nd element of the tuple that contains the values
        
        
input = Input()
# print (input.header)
input.findIPAddress()
print(type(input.header))
# print(input.header.items())
input.findIPAddress()
print(input.emailArray)



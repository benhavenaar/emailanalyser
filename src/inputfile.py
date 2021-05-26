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
        self.urlRegex = re.compile(r'(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))')
         
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
        self.body = self.body.replace("=\n", "")
        # print(self.body)
 
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
        self.deconstructEmail(emailPath)
        urlBodyArray = self.findContentInBody(self.urlRegex, self.urlBodyArray, self.body)
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
        
    def findContentInBody(self, regexFilter, contentArray, content):
        duplicateItems = {}
        contentValue = regexFilter.findall(content)
        for contentValueSplit in contentValue:
            if contentValueSplit in duplicateItems:
                contentNumber = duplicateItems[contentValueSplit]
            else:
                contentArray.append(contentValueSplit)
                duplicateItems[contentValueSplit] = contentNumber = len(contentArray)-1
        return contentArray
        # return contentArray
        
# input = Input()
# # print (input.header)
# input.findIPAddress()
# print(type(input.header))
# # print(input.header.items())
# input.findIPAddress()
# print(input.emailArray)



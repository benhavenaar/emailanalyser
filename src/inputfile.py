#import libs
import win32com.client
from email.parser import HeaderParser
import email
from email import policy
import re
import base64
import os

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
        self.bodyTest = None
        self.attachments = None
        self.outputString = "output"
        self.outputCount = 0
        self.headerDict = {}
        self.ipAddressHeaderArray = []
        self.urlHeaderArray = []
        self.urlBodyArray = []
        self.filterArray = ['.gif', '.png', '.jpg'] #extend this array if you want to filter more useless URL extentions
        self.ipAddressRegex = re.compile(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')
        self.urlRegex = re.compile(r'(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))')
         
    def deconstructEmail(self, emailPath):
        self.file = open(emailPath, encoding="ISO-8859-1")
        self.emailMessage = email.message_from_file(self.file, policy=policy.default)
        self.file.close()
        self.headerParser = email.parser.HeaderParser()
        self.header = self.headerParser.parsestr(self.emailMessage.as_string())
        # if self.emailMessage.is_multipart():  
            # for payload in self.emailMessage.get_payload():
                # try:
                    # self.body = payload.get_payload()
                    # if type(self.body) == list:
                        # self.body = payload.get_payload()
                # except AttributeError:
                    # self.body = self.emailMessage.get_payload()
        # else:
            # self.body = self.emailMessage.get_payload()
        self.body = self.emailMessage.get_body()
        # try:
        try: 
            self.body = self.body.get_content()
        except KeyError:
            self.body = self.body.get_payload()
            if type(self.body) == list:
                self.bodyTest = [payload for payload in self.body if "image" not in str(payload["Content-Type"])]
            if self.emailMessage.is_multipart():  
                for payload in self.bodyTest:
                    try:
                        self.body = payload.get_payload()
                        if type(self.body) == list:
                            self.body = payload.get_payload()
                    except AttributeError:
                        self.body = self.emailMessage.get_payload()
            else:
                self.body = self.emailMessage.get_payload()
        
        if type(self.body) == list:
            self.body = self.body[0].get_content()
        print(self.body)
        # print(self.body)
        # print(self.emailMessage.items())
        # if self.emailMessage["Content-Transfer-Encoding"] == "base64":
            # print('hallo')
            # self.body = self.body.encode('ascii')
            # self.body = base64.b64decode(self.body)
            # self.body = self.body.decode('ascii')
        self.convertToDict(self.header.items(), self.headerDict)
    
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
        
    def findURLInBody(self, emailPath, urlBodyArray = []):
        self.deconstructEmail(emailPath)
        urlBodyArray = self.findContentInBody(self.urlRegex, self.body)        
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
        
    def findContentInBody(self, regexFilter, content, contentArray = []):
        contentArray.clear()
        duplicateItems = {}
        # print(content)
        contentValue = regexFilter.findall(content)
        for contentValueSplit in contentValue:
            if contentValueSplit in duplicateItems:
                contentNumber = duplicateItems[contentValueSplit]
            else:
                contentArray.append(contentValueSplit)
                duplicateItems[contentValueSplit] = contentNumber = len(contentArray)-1
        # print('filtering images entries with .png')
        for filter in self.filterArray:
            contentArray = [item for item in contentArray if filter not in item]
       
        return contentArray
    
    def getAttachments(self):
        try:
            for attachment in self.emailMessage.iter_attachments():
                outputFileName = attachment.get_filename()
                if outputFileName:
                    with open(os.path.join(self.outputString, outputFileName), "wb") as of:
                        of.write(attachment.get_payload(decode=True))
                        self.outputCount += 1
            if self.outputCount == 0:
                print("No attachment found for file {}".format(self.file))
        except IOError:
            print("Problem with {} or one of its attachments.".format(self.file))
    
    def convertToDict(self, tuple, dict):
        for a, b in tuple:
            dict.setdefault(a, []).append(b)
        return dict
        
    def isBase64(self, sb):
        try:
            if isinstance(sb, str):
                sb_bytes = bytes(sb, 'ascii')
            elif isinstance(sb, bytes):
                sb_bytes = sb
            else:
                raise ValueError("Argument must be string or bytes")
            return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
        except Exception:
            return False

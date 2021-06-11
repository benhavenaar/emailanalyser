#import libs
import win32com.client
from email.parser import HeaderParser
import email
from email import policy
import re
import base64
import os
import itertools

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
        self.headerDict = {}
        self.ipAddressHeaderArray = []
        self.urlHeaderArray = []
        self.urlBodyArray = []
        self.filterArray = ['.gif', '.png', '.jpg'] #extend this array if you want to filter more useless URL extentions
        self.signatureFilterList = ['received-spf', 'authentication-results', 'dkim-signature', 'arc-authentication-results', 'x-google-dkim-signature']
        self.ipAddressRegex = re.compile(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')
        self.urlRegex = re.compile(r'(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))')
         
    def deconstructEmail(self, emailPath):
        """Deconstructs the email and splits it into header, body, and attachment.
        Currently get_contant() of email library will be used, if it can't be used because of a KeyError, payload will be loaded
        Loading the payload means it is party of a multipart and needs to be deconstructed down. The HTML text part is fetched and
        set to the self.body. This way the email can be read/URLs can be found within the string. 
        Because of this, the email content doesn't need to be decoded from base64 as the email library handles this part.
        
        """
        self.file = open(emailPath, encoding="ISO-8859-1")
        self.emailMessage = email.message_from_file(self.file, policy=policy.default)
        self.file.close()
        self.headerParser = email.parser.HeaderParser()
        self.header = self.headerParser.parsestr(self.emailMessage.as_string())
        self.body = self.emailMessage.get_body()
        try: 
            self.body = self.body.get_content() #Try to get body content
        except KeyError: 
            self.body = self.body.get_payload()
            if type(self.body) == list:
                self.bodyTest = [payload for payload in self.body if "image" not in str(payload["Content-Type"])]
            if self.emailMessage.is_multipart():
                print(len(self.bodyTest))
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
            for item in self.body:
                if "html" in str(item["Content-Type"]):
                    self.body = item.get_content()
           
        self.convertToDict(self.header.items(), self.headerDict)
    
    
    def findIPAddressInHeader(self, emailPath):
        """Append ip addresses found in the email header/body to self.emailArray. The for and if/else loop in the first Else part is used to filter out duplicates. 
        First the value found is set to a tuple, then the items will be added iterated over (if multiple ip's in one line exist), then it's added to the duplicateIPAddresses
        Afterwards if it isn't found in the duplicate list it will be added to self.emailArray. 
        
        """
        self.deconstructEmail(emailPath)
        ipAddressArray = self.findContentInHeader(self.ipAddressRegex, self.ipAddressHeaderArray, self.header.items())
        return ipAddressArray
    
    def findURLInHeader(self, emailPath):
        """Same concept as IPaddress finder. It will send the regex filter along with the values to the content finder
        """
        self.deconstructEmail(emailPath)
        urlHeaderArray = self.findContentInHeader(self.urlRegex, self.urlHeaderArray, self.header.items())
        return urlHeaderArray
        
    def findURLInBody(self, emailPath, urlBodyArray = []):
        """Same concept as IPaddress finder. It will send the regex filter along with the values to the content finder.
        A filter will be applied to this list. If you want to whitelist domains (such as google), extend this list.
        """
        self.deconstructEmail(emailPath)
        urlBodyArray = self.findContentInBody(self.urlRegex, self.body)        
        return urlBodyArray
        
    def getSignatureList(self, emailPath, signatureListArray = []):
        signatureListArray.clear()
        file = open(emailPath, encoding="ISO-8859-1")
        emailMessage = email.message_from_file(file, policy=policy.default)
        file.close()
        for key, value in emailMessage.items():
            if key.lower() in self.signatureFilterList:
                signatureListArray.append((key, value))
            if key.lower() == 'authentication-results':
                signatureListArray.clear()
                signatureListArray.append((key, value))
                # break
                
        
        print(signatureListArray)
    
    def findContentInHeader(self, regexFilter, contentArray, content):
        """Find content in header based on regex filter. Mainly used to find IP and signatures
        """
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
        """Finds the content in the body. Atm only used for finding URLs in the body.
        This function can be expanded to search the body for useful strings such as "bitcoin", "payment", etc. to flag it
        """
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
    
    def getAttachments(self, emailPath, outputCount = 0, attachmentArray = []):
        """Attachment finder. Under construction.
        Parameters:
            emailPath (os path): Path to the location of the email file
            
        Returns:
            saves attachment to file
        """
        attachmentArray.clear()
        file = open(emailPath, encoding="ISO-8859-1")
        emailMessage = email.message_from_file(file, policy=policy.default)
        file.close()
        try:
            for attachment in emailMessage.iter_attachments():
                outputFileName = attachment.get_filename()
                if outputFileName:
                    attachmentArray.append('attachment_'+outputFileName)
                    with open(os.path.join('attachments',self.uniqueFile("attachment", outputFileName)), "wb") as of:
                        of.write(attachment.get_payload(decode=True))
                        outputCount += 1
            if outputCount == 0:
                print("No attachment found for file {}".format(file))
        except TypeError as e:
            print("Problem with {} or one of its attachments. Reason: {}".format(file, e))
        
        return attachmentArray
        
    def uniqueFile(self, baseName, outputName):
        """Check if the file already exists in the folder. For attachments it's probably better to overwrite files than to keep downloading them.
        The same function exists in output.py, there this function does work. To fix it, only "attachment/" needs to be added to 
        while os.path.exists(actualName) -> os.path.exists("attachment/"+actualName)
        
        Parameters:
            baseName (str): basename for the attachment that needs to be saved
            outputName (str): name of the attachment
            
        Returns:
            actualName (str): the name of the file that needs to be saved.
        """
        actualName = "%s_%s" % (baseName, outputName)
        c = itertools.count()
        while os.path.exists(actualName):
            actualName = "%s_%d_%s" % (baseName, next(c), outputName)
        return actualName
    
    def convertToDict(self, tuple, dict):
        """A Tuple list of dicts, this is made into a dict in order to parse through the content of the dict based on keys and values
        """
        for a, b in tuple:
            dict.setdefault(a, []).append(b)
        return dict
        
    def isBase64(self, sb):
        """Deprecated function. Used to check whether the content is base64 or not.
        Currently the email library decodes the content of the email.
        """
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

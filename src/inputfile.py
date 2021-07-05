# import libs
from email.parser import HeaderParser
import email
from email import policy
import re
import base64
import os
import itertools

# classes
from ParsedMail import ParsedMail


class InputFile:
    # class init variables
    def __init__(self, **kwargs):
        # Services
        self.headerParser = email.parser.HeaderParser()

        # Configuration
        self.ignoredFiles = ['.gif', '.png', '.jpg']  # extend this array if you want to filter more useless URL extentions
        self.signatureFilterList = ['received-spf', 'authentication-results', 'dkim-signature', 'arc-authentication-results', 'x-google-dkim-signature']
        self.ipAddressRegex = re.compile(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')
        self.urlRegex = re.compile(r'(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))')

    def deconstructEmail(self, emailPath):
        """Deconstructs the email and splits it into header, body, and attachment.
        Currently get_content() of email library will be used, if it can't be used because of a KeyError, payload will be loaded
        Loading the payload means it is party of a multipart and needs to be deconstructed down. The HTML text part is fetched and
        set to the self.body. This way the email can be read/URLs can be found within the string.
        Because of this, the email content doesn't need to be decoded from base64 as the email library handles this part.

        """
        emailMessage = self.getEmailFromFile(emailPath);
        header = self.headerParser.parsestr(emailMessage.as_string())
        body = emailMessage.get_body()
        bodyList = []
        
        try:
            body = body.get_content()  # Try to get body content
        except KeyError:
            body = emailMessage.get_payload()
            body_payloads = []
            if type(body) == list:
                body_payloads = [payload for payload in body if "image" not in str(payload["Content-Type"])]

            if emailMessage.is_multipart():
                for part in emailMessage.walk():
                    if "html" in str(part["Content-Type"]):
                        bodyList.append(part.get_content())
                if bodyList:
                    body = ' '.join(bodyList)
                '''for payload in body_payloads:
                    try:
                        # TODO: If multiple payload's are found only the last one will assigned to body
                        body = payload.get_payload()
                    except AttributeError:
                        body = emailMessage.get_payload()'''
        if type(body) == list:
            for item in body:
                if "html" in str(item["Content-Type"]):
                    body = item.get_content()
        yes = ParsedMail(header, body)
        return ParsedMail(header, body)

    def findIPAddressInHeader(self, emailPath):
        """Append ip addresses found in the email header/body to self.emailArray. The for and if/else loop in the first Else part is used to filter out duplicates.
        First the value found is set to a tuple, then the items will be added iterated over (if multiple ip's in one line exist), then it's added to the duplicateIPAddresses
        Afterwards if it isn't found in the duplicate list it will be added to self.emailArray.

        """
        mail = self.deconstructEmail(emailPath)
        return self.findContentInHeader(self.ipAddressRegex, mail.header.items())

    def findURLInHeader(self, emailPath):
        """Same concept as IPaddress finder. It will send the regex filter along with the values to the content finder
        """
        mail = self.deconstructEmail(emailPath)
        return self.findContentInHeader(self.urlRegex, mail.header.items())

    def findURLInBody(self, emailPath):
        """Same concept as IPaddress finder. It will send the regex filter along with the values to the content finder.
        A filter will be applied to this list. If you want to whitelist domains (such as google), extend this list.
        """
        mail = self.deconstructEmail(emailPath)
        return self.findContentInBody(self.urlRegex, mail.body)

    def getSignatureList(self, emailPath):
        emailMessage = self.getEmailFromFile(emailPath)
        signatures = []

        for key, value in emailMessage.items():
            if key.lower() in self.signatureFilterList:
                signatures.append((key, str(value)))
            if key.lower() == 'authentication-results':
                signatures.clear()
                signatures.append((key, str(value)))
                break

        return self.convertToDict(signatures)

    def findContentInHeader(self, regexFilter, content):
        """Find content in header based on regex filter. Mainly used to find IP and signatures
        """
        contentThatMatchesProvidedRegex = []
        duplicateItems = {}

        for line in content:
            for item in range(len(line)):
                if regexFilter.search(line[item]) == None:
                    pass
                else:
                    regexMatches = regexFilter.findall(line[item])
                    for contentValueSplit in regexMatches:
                        if contentValueSplit in duplicateItems:
                            contentNumber = duplicateItems[contentValueSplit]
                        else:
                            contentThatMatchesProvidedRegex.append(contentValueSplit)
                            duplicateItems[contentValueSplit] = contentNumber = len(contentThatMatchesProvidedRegex) - 1

        return contentThatMatchesProvidedRegex

    def findContentInBody(self, regexFilter, content):
        """Finds the content in the body. Atm only used for finding URLs in the body.
        This function can be expanded to search the body for useful strings such as "bitcoin", "payment", etc. to flag it
        """
        contentArray = []
        duplicateItems = {}
        # print(content)
        contentValue = regexFilter.findall(content)
        for contentValueSplit in contentValue:
            if contentValueSplit in duplicateItems:
                contentNumber = duplicateItems[contentValueSplit]
            else:
                contentArray.append(contentValueSplit)
                duplicateItems[contentValueSplit] = contentNumber = len(contentArray) - 1
        print('Filtering images entries.')
        for filter in self.ignoredFiles:
            contentArray = [item for item in contentArray if filter not in item]

        return contentArray

    def getAttachments(self, emailPath):
        """Attachment finder. Under construction.
        Parameters:
            emailPath (os path): Path to the location of the email file

        Returns:
            saves attachment to file
        """
        outputCount = 0
        attachmentArray = []
        emailMessage = self.getEmailFromFile(emailPath)

        try:
            for attachment in emailMessage.iter_attachments():
                outputFileName = attachment.get_filename()
                if outputFileName:
                    attachmentArray.append('attachment_' + outputFileName)
                    with open(os.path.join('attachments', self.uniqueFile("attachment", outputFileName)), "wb") as of:
                        of.write(attachment.get_payload(decode=True))
                        outputCount += 1
            if outputCount == 0:
                print("No attachment found for file {}".format(emailPath))
        except TypeError as e:
            print("Problem with {} or one of its attachments. Reason: {}".format(emailPath, e))

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

    def getEmailFromFile(self, emailPath):
        file = open(emailPath, encoding="ISO-8859-1")
        emailMessage = email.message_from_file(file, policy=policy.default)
        file.close()

        return emailMessage

    def convertToDict(self, tuple):
        """A Tuple list of dicts, this is made into a dict in order to parse through the content of the dict based on keys and values
        """
        dictFromTuple = {}

        for a, b in tuple:
            dictFromTuple.setdefault(a, []).append(b)
        return dictFromTuple

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

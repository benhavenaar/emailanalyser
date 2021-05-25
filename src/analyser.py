#import libs
import requests
import json

class Analyser:
    def __init__(self):
        self.ipAddressResults = []
        self.urlResults = []
        self.attachmentResults = []
        self.url = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
#variables

#functions
    def analyseIP(self, ipAddressList):
        params = {'apikey':'4e5a399bbe79351e8f6533bde32337824bdba3e263e204d8a52849efbdd75e56','ip':ipAddressList[0]}
        response = requests.get(self.url, params=params)
        return response.json()['country']
        
    def analyseURL(self, urlList):
        return self.urlResults
    
    def analyseAttachments(self, attachmentList):
        return self.attachmentResults
        
    def jsonPrint(self, obj):
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)
#loop


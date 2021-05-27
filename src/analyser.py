#import libs
import requests
import json
import base64

class Analyser:
    def __init__(self):
        self.ipAddressResults = []
        self.urlResults = []
        self.attachmentResults = []
        self.url = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
        self.urlAnalysis = 'https://www.virustotal.com/api/v3/urls/'
        self.headers = {"x-apikey": '4e5a399bbe79351e8f6533bde32337824bdba3e263e204d8a52849efbdd75e56'}
#variables

#functions
    def analyseIP(self, ipAddressList):
        params = {'apikey':'4e5a399bbe79351e8f6533bde32337824bdba3e263e204d8a52849efbdd75e56','ip':ipAddressList[0]}
        response = requests.get(self.url, params=params)
        return response.json()['country']
        
    def analyseURL(self, urlList):
        url_id = base64.urlsafe_b64encode(urlList[0].encode()).decode().strip("=")
        print(self.urlAnalysis+url_id)
        response = requests.get(self.urlAnalysis+url_id, headers=self.headers)
        print(response)
        result = json.loads(response.text)
        print(result)
        return result
    
    def analyseAttachments(self, attachmentList):
        return self.attachmentResults
        
    def jsonPrint(self, obj):
        text = json.dumps(obj, sort_keys=True, indent=4)
        # print(text)
#loop


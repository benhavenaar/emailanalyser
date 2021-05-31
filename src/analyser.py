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
    #AnalyseIP will be deprecated, information extracted from IP addresses doesn't deem to be worth checking.
    def analyseIP(self, ipAddressList):
        params = {'apikey':'4e5a399bbe79351e8f6533bde32337824bdba3e263e204d8a52849efbdd75e56','ip':ipAddressList[0]}
        response = requests.get(self.url, params=params)
        return response.json()['country']
     
    #function to analyse URLs, it encodes the url in the list to a base64 code and pastes it to the virustotal api url for it to scan it.
    #The returned response is sent back to the object that called this function.    
    def analyseURL(self, urlList):
        try:
            url_id = base64.urlsafe_b64encode(urlList[0].encode()).decode().strip("=")
            response = requests.get(self.urlAnalysis+url_id, headers=self.headers)
            print(response)
            result = json.loads(response.text)
            result = self.extractUsefulData(result)
            return result
        except IndexError:
            print("Error: No URL found in body of email")
    
    def analyseAttachments(self, attachmentList):
        return self.attachmentResults
    
    #json respone text is a cluttered dict, this function helps to make it more readible. Will be deprecated once final project is done.
    def jsonPrint(self, obj):
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)
    
    #the json response is filled with a lot of data, the most useful keys+values out of the dictionary are extracted here.
    def extractUsefulData(self, response):
        newDict = {} 
        newDict['last_analysis_stats'] = response['data']['attributes']['last_analysis_stats']
        newDict['last_final_url'] = response['data']['attributes']['last_final_url']
        return(newDict)



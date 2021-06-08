#import libs
import requests
import constants
import json
import base64
import errors
import time

class Analyser:
    def __init__(self):
        self.ipAddressResults = []
        self.urlResults = []
        self.attachmentResults = []
        self.APIKey = constants.VT_API_KEY
        self.url = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
        self.urlAnalysis = 'https://www.virustotal.com/api/v3/urls'
        self.headers = {"x-apikey": self.APIKey, "Accept": "application/json"}
        self.VirusTotalApiError = errors.VirusTotalApiError
#variables
    

#functions

    #AnalyseIP will be deprecated, information extracted from IP addresses doesn't deem to be worth checking.
    def analyseIP(self, ipAddressList):
        params = {'apikey': self.APIKey,'ip':ipAddressList[0]}
        response = requests.get(self.url, params=params)
        return response.json()['country']
     
    #function to analyse URLs, it encodes the url in the list to a base64 code and pastes it to the virustotal api url for it to scan it.
    #The returned response is sent back to the object that called this function.    
    # def analyseURL(self, urlList):
        # try:
            # url_id = base64.urlsafe_b64encode(urlList[0].encode()).decode().strip("=")
            # response = requests.get(self.urlAnalysis+url_id, headers=self.headers)
            # print(response)
            # result = json.loads(response.text)
            # result = self.extractUsefulData(result)
            # return result
        # except IndexError:
            # print("Error: No URL found in body of email")
    
    def analyseURL(self, urlList, timeout=None):
        resultList = []
        for url in urlList:
            # print("Trying to scan: ", url)
            try:
                response = requests.post(self.urlAnalysis, 
                                         headers=self.headers, 
                                         data={"url":url}, 
                                         timeout=timeout)
        
                if response.status_code == 429:
                    raise Exception("API request quota reach, please wait...")
                if response.status_code != 200:
                    self._raise_exception(response)
                
                url_id = base64.b64encode(url.encode())
                print("trying to scan: ", self.urlAnalysis + '/{}'.format(url_id.decode().replace('=', '')))
                response = requests.get(self.urlAnalysis + '/{}'.format(url_id.decode().replace('=', '')),
                                        headers = self.headers,
                                        timeout=timeout)
                                        
                if response.status_code != 200: 
                    self._raise_exception(response)
                    
                while not response.json()['data']['attributes']['last_analysis_results']:
                    response = requests.get(self.urlAnalysis + '/{}'.format(url_id.decode().replace('=', '')),
                                            headers=self.headers,
                                            timeout=timeout)
                    print("waiting for response")
                    time.sleep(3)
                
                result = json.loads(response.text)
                resultList.append(self.extractUsefulData(result))
                # print(resultList)
                
            except requests.exceptions.RequestException as error:
                print(error)
                # exit(1)
            
            except IndexError:
                print("Error: No URL found in body of email")
                
        return resultList
                
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
        
    def _raise_exception(self, response):
    # https://developers.virustotal.com/v3.0/reference#errors
        raise self.VirusTotalApiError(response.text)



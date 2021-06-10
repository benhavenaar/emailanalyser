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
        """Deprecated function. IP addresses hold no interesting value for the user.
        This function retrieves the country of the IP address/report
        
        Parameters:
            ipAddressList (list): IP addresses to scan
            
        Returns: 
            country of origin in the form of a string
        """
        params = {'apikey': self.APIKey,'ip':ipAddressList[0]}
        response = requests.get(self.url, params=params)
        return response.json()['country']
     
    #function to analyse URLs, it encodes the url in the list to a base64 code and pastes it to the virustotal api url for it to scan it.
    #The returned response is sent back to the object that called this function.    
    def analyseURL(self, urlList, timeout=None):
        """Retrieve information about URLs. If the URL was scanned before it will return the results immediatly.
        If the URL isn't found in the VT database it will scan it. Results may take a few seconds to return. The program will wait for these results
        Multithreading might solve some issue to not wait too long on results.
        
        Parameters:
            urlList (list): URLs to scan
            timeout (float, optional): The amount of time in seconds the request should wait before timing out.
            
        Returns:
            A list with dicts of the scan results
        """
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
                
                url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
                print("\n-----------------------------------\n","trying to scan: ", url)
                response = requests.get(self.urlAnalysis + '/' + url_id,
                                        headers = self.headers,
                                        timeout=timeout)
                                        
                if response.status_code != 200: 
                    self._raise_exception(response)
                 
                while not response.json()['data']['attributes']['last_analysis_results']:
                    response = requests.get(self.urlAnalysis + '/' + url_id,
                                            headers=self.headers,
                                            timeout=timeout)
                    print("Waiting for API response...")
                    time.sleep(3)
                
                result = json.loads(response.text)
                resultList.append(self.extractUsefulData(result))
                print(self.extractUsefulData(result))
                
            except requests.exceptions.RequestException as error:
                print(error)
                exit(1)
            
            except IndexError:
                print("Error: No URL found in body of email")
        
        res_list = []
        for i in range(len(resultList)):
            if resultList[i] not in resultList[i + 1:]:
                res_list.append(resultList[i])
        return res_list
                
    def analyseAttachments(self, attachmentList):
        """
        
        Parameters:
            attachmentList (list or str): list of attachments or a single string if only one attachment is found
                
        Returns:
            Scan results of the scanned attachment
        """
        # return self.attachmentResults
        pass
    
    #json respone text is a cluttered dict, this function helps to make it more readible. Will be deprecated once final project is done.
    def jsonPrint(self, obj):
        """Response text is cluttered, this function will make the output more readable. 
        
        Parameters:
            obj (json): json response dict
            
        Returns:
            dict of scan results. Currenlty it prints the results
        """
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)
    
    #the json response is filled with a lot of data, the most useful keys+values out of the dictionary are extracted here.
    def extractUsefulData(self, response):
        """Response text is filled with a lot of data. Only last_analysis_stats and last_final_url are extracted.
        There's more useful data inside this response, check out https://developers.virustotal.com/v3.0/reference#url-object for more information
        
        Parameter:
            response (json): json response which is extracted for its useful data
            
        Returns:
            Dict of useful response data.
        """
        newDict = {} 
        newDict['last_analysis_stats'] = response['data']['attributes']['last_analysis_stats']
        newDict['last_final_url'] = response['data']['attributes']['last_final_url']
        return(newDict)
        
    def _raise_exception(self, response):
        """Function to raise an exception using the error messages returned by the API.
        https://developers.virustotal.com/v3.0/reference#errors
        Parameters:
            response (dict) Reponse containing the error returned by the API.
        """
        raise self.VirusTotalApiError(response.text)



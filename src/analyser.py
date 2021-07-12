#import libs
import requests
import constants
import json
import base64
import errors
import time
import os

class Analyser:
    def __init__(self):
        self.ipAddressResults = []
        self.urlResults = []
        self.attachmentResults = []
        self.APIKey = constants.VT_API_KEY
        self.url = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
        self.fileURL = 'https://www.virustotal.com/api/v3/files'
        self.urlAnalysis = 'https://www.virustotal.com/api/v3/urls'
        self.getAnalysisURL = 'https://www.virustotal.com/api/v3/analyses'
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
    def analyseURL(self, url, timeout=None, newDict = {}, clearDict = False):
        """Retrieve information about URLs. If the URL was scanned before it will return the results immediatly.
        If the URL isn't found in the VT database it will scan it. Results may take a few seconds to return. The program will wait for these results
        Multithreading might solve some issue to not wait too long on results.
        
        Parameters:
            urlList (list): URLs to scan
            timeout (float, optional): The amount of time in seconds the request should wait before timing out.
            
        Returns:
            A list with dicts of the scan results
        """
        if clearDict:
            newDict = newDict.clear()
            newDict = {}
        try:
            response = requests.post(self.urlAnalysis, 
                                     headers=self.headers, 
                                     data={"url":url}, 
                                     timeout=timeout)
    
            if response.status_code == 429:
                raise Exception("API request quota reached, please wait...")
            if response.status_code != 200:
                self._raise_exception(response)
            
            url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
            print("\n-----------------------------------\n","Trying to scan: \n", url, '\n')
            response = requests.get(self.urlAnalysis + '/' + url_id,
                                    headers = self.headers,
                                    timeout=timeout)
                                    
            while response.status_code != 200:
                response = requests.get(self.urlAnalysis + '/' + url_id,
                                    headers = self.headers,
                                    timeout=timeout)
            #if response.status_code != 200: 
            #    self._raise_exception(response)
             
            while not response.json()['data']['attributes']['last_analysis_results']:
                response = requests.get(self.urlAnalysis + '/' + url_id,
                                        headers=self.headers,
                                        timeout=timeout)
                print("Waiting for API response...")
                time.sleep(3)
            
            result = json.loads(response.text)
            newDict[response.json()['data']['attributes']['last_final_url']] = response.json()['data']['attributes']['last_analysis_stats']
            self.jsonPrint(self.extractUsefulData(result))
            
        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)
        
        except IndexError:
            print("Error: No URL found in body of email")
        
        return newDict
                
    def analyseAttachments(self, attachmentList, attachmentIDList = [], timeout=None):
        """
        
        Parameters:
            attachmentList (list or str): list of attachments or a single string if only one attachment is found
                
        Returns:
            Scan results of the scanned attachment
        """
        attachmentIDList.clear()
        for attachment in attachmentList: 
            attachment = 'attachments/' + attachment
            if not os.path.isfile(attachment):
                raise Exception("File not found.")
            
            file_size = os.path.getsize(attachment)
            
            if file_size < 33554432:
                with open(attachment, 'rb') as f:
                    data = {'file': f.read()}
                    
                    try:
                        response = requests.post(self.fileURL, 
                                                headers = self.headers,
                                                files   = data,
                                                timeout = timeout)
                                            
                        if response.status_code != 200:
                            self._raise_exception(response)
                         
                        attachmentIDList.append(response.json()['data']['id'])
                        
                    except requests.exceptions.RequestException as error:
                        print(error)
                        exit(1)
                        
            if file_size >= 33554432:
                with open(attachment, 'rb') as f:
                    data = {'file': f.read()}
                    
                    try:
                        response = requests.get(self.fileURL + '/upload_url',
                                                headers = self.headers,
                                                timeout = timeout)
                                                
                        if response.status_code != 200:
                            self._raise_exception(response)
                            
                        upload_url = response.json()['data']
                        
                        response = response.post(upload_url,
                                                 headers = self.headers,
                                                 files   = data,
                                                 timeout = timeout)
                                                 
                        if response.status_code != 200:
                            self._raise_exception(response)
                        
                        attachmentIDList.append(response.json()['data']['id'])
                        
                    except requests.exception.RequestException as error:
                        print(error)
                        exit(1)
        
        print(attachmentIDList)
        return attachmentIDList
        
    def getInfoAttachments(self, attachmentIDList, timeout = None, attachmentScanResultList = {}):
        attachmentScanResultList.clear()
        for attachmentID in attachmentIDList:
            try:
                response = requests.get(self.getAnalysisURL + '/{}'.format(attachmentID),
                                        headers = self.headers,
                                        timeout = timeout)
                                        
                if response.status_code != 200:
                    self._raise_exception(response)
               
                attachmentScanResultList['file_'+attachmentID] = response.json()['data']['attributes']['stats']

                
            except requests.exceptions.RequestException as error:
                print(error)
                exit(1)
        
        print(attachmentScanResultList)
        return attachmentScanResultList
    

    def jsonPrint(self, obj):
        """Response text is cluttered, this function will make the output more readable. 
        
        Parameters:
            obj (json): json response dict
            
        Returns:
            dict of scan results. Currenlty it prints the results
        """
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)
    

    def extractUsefulData(self, response):
        """Response text is filled with a lot of data. Only last_analysis_stats and last_final_url are extracted.
        There's more useful data inside this response, check out https://developers.virustotal.com/v3.0/reference#url-object for more information
        
        Parameter:
            response (json): json response which is extracted for its useful data
            
        Returns:
            Dict of useful response data.
        """
        newDict = {} 
        newDict[response['data']['attributes']['last_final_url']] = response['data']['attributes']['last_analysis_stats']
        return(newDict)
        
    def _raise_exception(self, response):
        """Function to raise an exception using the error messages returned by the API.
        https://developers.virustotal.com/v3.0/reference#errors
        Parameters:
            response (dict) Reponse containing the error returned by the API.
        """
        raise self.VirusTotalApiError(response.text)



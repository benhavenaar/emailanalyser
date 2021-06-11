#import libs
import time
import os
import itertools
import csv
import pandas as pd
#Output should contain the following information:
# - Scanned email name/path
# - SPF/DKIM/DMARC signature results
# - URL + results
# - Attachments + results
# dummy_data_list = [
    # {
        # "last_analysis_stats": {
            # "harmless": 76,
            # "malicious": 1,
            # "suspicious": 2,
            # "timeout": 0,
            # "undetected": 9
        # },
        # "last_final_url": "http://hotna.cc/lpage.php"
    # },
    # {
        # "last_analysis_stats": {
            # "harmless": 76,
            # "malicious": 1,
            # "suspicious": 2,
            # "timeout": 0,
            # "undetected": 9
        # },
        # "last_final_url": "http://hotna.cc/lpage.php"
    # },
    # {
        # "last_analysis_stats": {
            # "harmless": 77,
            # "malicious": 1,
            # "suspicious": 2,
            # "timeout": 0,
            # "undetected": 8
        # },
        # "last_final_url": "http://hotna.cc/lpage.php"
    # },
    # {
        # "last_analysis_stats": {
            # "harmless": 76,
            # "malicious": 1,
            # "suspicious": 2,
            # "timeout": 0,
            # "undetected": 9
        # },
        # "last_final_url": "http://hotna.cc/lpage.php"
    # },
    # {
        # "last_analysis_stats": {
            # "harmless": 77,
            # "malicious": 1,
            # "suspicious": 2,
            # "timeout": 0,
            # "undetected": 8
        # },
        # "last_final_url": "http://hotna.cc/lpage.php"
    # },
    # {
        # "last_analysis_stats": {
            # "harmless": 76,
            # "malicious": 1,
            # "suspicious": 2,
            # "timeout": 0,
            # "undetected": 9
        # },
        # "last_final_url": "http://hotna.cc/tri.php?nmly=1106&lo=122_2159056847"
    # },
    # {
        # "last_analysis_stats": {
            # "harmless": 76,
            # "malicious": 1,
            # "suspicious": 2,
            # "timeout": 0,
            # "undetected": 9
        # },
        # "last_final_url": "http://hotna.cc/imgs.php?2t3uv=1106&ymamw4=122_2159056847"
    # }
# ]

dummy_data_list2 = {'url1': {'harmless': 50, 'malicious': 1, 'suspicious': 34, 'undetected': 8, 'timeout': 0},
                    'url2': {'harmless': 103, 'malicious': 2, 'suspicious': 0, 'undetected': 8, 'timeout': 0},
                    'url3': {'harmless': 5, 'malicious': 1, 'suspicious': 6, 'undetected': 8, 'timeout': 0},
                    'url4': {'harmless': 9, 'malicious': 3, 'suspicious': 0, 'undetected': 8, 'timeout': 0}}

dummy_data_list3 = {'https://poules.com/nl/lobby?utm_source=poules.com&utm_medium=email&utm_campaign=july2020': {'harmless': 79, 'malicious': 0, 'suspicious': 0, 'undetected': 9, 'timeout': 0}, 
                    'https://poules.com/nl/email-voorkeuren/175263/3ca84ce2e060aaa78dedf4402f856f46': {'harmless': 79, 'malicious': 0, 'suspicious': 0, 'undetected': 9, 'timeout': 0}}

class Output:
    def __init__(self): 
        self.textFile = None
     
    def writeToCSV(self, scanResultList, fileName):
        df = pd.DataFrame(data=scanResultList).T
        df.to_excel(os.path.join('scanresults', self.uniqueFile('scanresult', fileName, 'xlsx')))
       
     
    def writeScanResults(self, scanResultList, emailName):
        with open(os.path.join('scanresults',self.uniqueFile("scan_results",emailName, "txt")), "w") as f:
            f.write("Scan results of {}\n--------------------------------------------------\n".format(emailName))
            for i in scanResultList:
                for key, value in i.items():
                    f.write("{} = {}\n".format(str(key), str(value)))
                f.write('\n')
            
    def uniqueFile(self, baseName, emailName, ext):
        actualName = "%s_%s.%s" % (baseName, emailName, ext)
        c = itertools.count()
        while os.path.exists('scanresults/'+actualName):
            actualName = "%s_%s (%d).%s" % (baseName, emailName, next(c), ext)
        return actualName   

# outputTest = Output()
# outputTest.writeScanResults(dummy_data_list, "test")

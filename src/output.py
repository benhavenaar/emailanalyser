#import libs
import time
import os
import itertools
#Output should contain the following information:
# - Scanned email name/path
# - SPF/DKIM/DMARC signature results
# - URL + results
# - Attachments + results
dummy_data_list = [
    {
        "last_analysis_stats": {
            "harmless": 76,
            "malicious": 1,
            "suspicious": 2,
            "timeout": 0,
            "undetected": 9
        },
        "last_final_url": "http://hotna.cc/lpage.php"
    },
    {
        "last_analysis_stats": {
            "harmless": 76,
            "malicious": 1,
            "suspicious": 2,
            "timeout": 0,
            "undetected": 9
        },
        "last_final_url": "http://hotna.cc/lpage.php"
    },
    {
        "last_analysis_stats": {
            "harmless": 77,
            "malicious": 1,
            "suspicious": 2,
            "timeout": 0,
            "undetected": 8
        },
        "last_final_url": "http://hotna.cc/lpage.php"
    },
    {
        "last_analysis_stats": {
            "harmless": 76,
            "malicious": 1,
            "suspicious": 2,
            "timeout": 0,
            "undetected": 9
        },
        "last_final_url": "http://hotna.cc/lpage.php"
    },
    {
        "last_analysis_stats": {
            "harmless": 77,
            "malicious": 1,
            "suspicious": 2,
            "timeout": 0,
            "undetected": 8
        },
        "last_final_url": "http://hotna.cc/lpage.php"
    },
    {
        "last_analysis_stats": {
            "harmless": 76,
            "malicious": 1,
            "suspicious": 2,
            "timeout": 0,
            "undetected": 9
        },
        "last_final_url": "http://hotna.cc/tri.php?nmly=1106&lo=122_2159056847"
    },
    {
        "last_analysis_stats": {
            "harmless": 76,
            "malicious": 1,
            "suspicious": 2,
            "timeout": 0,
            "undetected": 9
        },
        "last_final_url": "http://hotna.cc/imgs.php?2t3uv=1106&ymamw4=122_2159056847"
    }
]

class Output:
    def __init__(self): 
        self.textFile = None
        
    def writeScanResults(self, scanResultList):
        with open(self.unique_file("scan_results", "txt"), "w") as f:
            for i in scanResultList:
                f.write(str(i))
                f.write('\n')
            
    def unique_file(self, basename, ext):
        actualname = "%s.%s" % (basename, ext)
        c = itertools.count()
        while os.path.exists(actualname):
            actualname = "%s (%d).%s" % (basename, next(c), ext)
        return actualname   
# res_list = []
# for i in range(len(dummy_data_list)):
    # if dummy_data_list[i] not in dummy_data_list[i + 1:]:
        # res_list.append(dummy_data_list[i])
# print(dummy_data_list)
# print(res_list)
outputTest = Output()
outputTest.writeScanResults(dummy_data_list)

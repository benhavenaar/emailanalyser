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

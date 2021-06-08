#import libs
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
        
    def parseScanResults(self, scanResultList):
        pass


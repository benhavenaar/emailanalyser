#import libs
import time
import os
import itertools
import csv
import pandas as pd
import openpyxl as op
#Output should contain the following information:
# - Scanned email name/path
# - SPF/DKIM/DMARC signature results
# - URL + results
# - Attachments + results

class Output:
    def __init__(self): 
        self.textFile = None
     
    def writeToCSV(self, scanResultList, signatureDict, fileName):
        fileName = self.uniqueFile('scanresult', fileName, 'xlsx')
        df = pd.DataFrame(data=scanResultList).T
        df = df.sort_values(by=['malicious', 'suspicious'], ascending=False)
        df.to_excel(os.path.join('scanresults', fileName))
        appendData = op.load_workbook(os.path.join('scanresults', fileName))
        appendDataSheet = appendData.get_sheet_by_name('Sheet1')
        for key, value in signatureDict.items():
            for item in str(value).split(';'):
                appendDataSheet.append([key, item])
        appendData.save(os.path.join('scanresults', fileName))
        appendData.close()
     
    def writeScanResults(self, scanResultList, emailName):
        """Deprecated function. Writes scan results to .txt file. Data is now written to xlsx
        """
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


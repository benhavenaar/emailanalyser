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
     
    def writeToCSV(self, scanResultList, signatureDict, fileName, append=False):
        if not append:
            fileName = self.uniqueFile('scanresult', fileName, 'xlsx')
        else:
            fileName = 'temporary_result_' + fileName + '.xlsx'
        df = pd.DataFrame(data=scanResultList).T
        try: 
            df = df.sort_values(by=['malicious', 'suspicious'], ascending=False)
        except:
            pass
        df.to_excel(os.path.join('scanresults', fileName))
        appendData = op.load_workbook(os.path.join('scanresults', fileName))
        appendDataSheet = appendData.get_sheet_by_name('Sheet1')
        for key, value in signatureDict.items():
            for item in str(value).split(';'):
                appendDataSheet.append([key, item])
        appendData.save(os.path.join('scanresults', fileName))
        appendData.close() 
            
    def uniqueFile(self, baseName, emailName, ext):
        actualName = "%s_%s.%s" % (baseName, emailName, ext)
        c = itertools.count()
        while os.path.exists(os.path.join('scanresults', actualName)):
            actualName = "%s_%s (%d).%s" % (baseName, emailName, next(c), ext)
        return actualName   
        
    def temporaryWriteToCSV(self, result, fileName):
        fileName = fileName + '.csv'
        df = pd.DataFrame(data=result).T
        try:
            df = df.sort_values(by=['malicious', 'suspicious'], ascending=False)
        except:
            pass
        df.to_csv(os.path.join('scanresults', fileName), mode='a', index = False, header=None)
        

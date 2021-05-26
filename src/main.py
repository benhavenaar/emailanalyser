from inputfile import InputFile
from analyser import Analyser
import tkinter as tk
from tkinter import filedialog

#open file dialog
root = tk.Tk()
root.withdraw()
emailFilePath = filedialog.askopenfilename()

#Input object
inputFile = InputFile()
emailArray = inputFile.findIPAddressInHeader(emailFilePath)
# urlArray = inputFile.findURLInHeader(emailFilePath)
urlBodyArray = inputFile.findURLInBody(emailFilePath)
print (emailArray)
# print (urlArray)
print (urlBodyArray)
# test = input("press something to continue")
# analyser = Analyser()
# analyser.jsonPrint(analyser.analyseIP(emailArray))

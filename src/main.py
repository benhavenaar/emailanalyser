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
emailArray = inputFile.findIPAddress(emailFilePath)
print (emailArray)

test = input("press something to continue")
analyser = Analyser()
analyser.jsonPrint(analyser.analyseIP(emailArray))

# analyser = Analyser()
# analyser.analyseIP(['138.128.150.133'])
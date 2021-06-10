from inputfile import InputFile
from analyser import Analyser
from output import Output
import tkinter as tk
from tkinter import filedialog
import os

#open file dialog
root = tk.Tk()
root.withdraw()

#functions
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

#Input object
inputFile = InputFile()
analyser = Analyser()
output = Output()
clearConsole()
print("\n-----------------------------------")
print("/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/")
print("-----------------------------------")
print("----Ordina Email Analyser Tool-----")
print("-----------------------------------")
print("/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/")
while True:
    print("-----------------------------------\n")
    print("1. Analyse email")
    print("2. Exit\n")
    option = input("Select an option...\n")
    if option == '1':
        try:
            emailFilePath = filedialog.askopenfilename()
            emailFilePathList = emailFilePath.split('/')
            emailName = emailFilePathList[-1]
        except FileNotFoundError:
            print("File not found, please try again.")
            emailFilePath = filedialog.askopenfilename()
        # emailArray = inputFile.findIPAddressInHeader(emailFilePath)
        urlBodyArray = inputFile.findURLInBody(emailFilePath)
        print(urlBodyArray)
        inputFile.getAttachments(emailFilePath)
        # scanResults = analyser.analyseURL(urlBodyArray)
        # output.writeScanResults(scanResults, emailName)
    elif option == '2':
        exit()
    else:
        ("Invalid option, please try again.\n")
# print (emailArray)
# print (urlArray)
print (urlBodyArray)
# test = input("press something to continue")
# analyser.jsonPrint(inputFile.headerDict)

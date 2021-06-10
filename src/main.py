from inputfile import InputFile
from analyser import Analyser
from output import Output
import tkinter as tk
from tkinter import filedialog
import os, shutil

#open file dialog
root = tk.Tk()
root.withdraw()

#variables
attachmentFolder = 'attachments'

#functions
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)
    
def deleteDownloadedAttachments():
    for filename in os.listdir(attachmentFolder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete {}. Reason: {}'.format(file_path, e))

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
        scanResults = analyser.analyseURL(urlBodyArray)
        output.writeScanResults(scanResults, emailName)
    elif option == '2':
        deleteDownloadedAttachments()
        exit()
    else:
        ("Invalid option, please try again.\n")
# print (emailArray)
# print (urlArray)
print (urlBodyArray)
# test = input("press something to continue")
# analyser.jsonPrint(inputFile.headerDict)

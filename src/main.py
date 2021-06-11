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
    """Function that clears the command line. It checks whether the user uses Windows before issuing a command
    """
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)
    
def deleteDownloadedAttachments():
    """Deletes all files from the attachments folder. This is to ensure any malware leaves the system
    before the prototype is closed. Possible add this whenever the prototype is started as well at a later point in time.
    
    Parameters:
        None
        
    Returns:
        Nothing, files get deleted from ./attachments
    """
    for filename in os.listdir(attachmentFolder):
        file_path = os.path.join(attachmentFolder, filename)
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
    print("2. Exit and delete attachments\n")
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
        attachmentArray = inputFile.getAttachments(emailFilePath) #send attachmentArray to analyser.py in order to analyse this list
        # if attachmentArray:
            # attachmentIDList = analyser.analyseAttachments(attachmentArray) #fill in details of analyseAttachments function in analyser.py
            # analyser.getInfoAttachments(attachmentIDList) 
        # scanResults = analyser.analyseURL(urlBodyArray)
        # output.writeScanResults(scanResults, emailName)
        inputFile.getSignatureList(emailFilePath)
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

from inputfile import InputFile
from analyser import Analyser
import tkinter as tk
from tkinter import filedialog

#open file dialog
root = tk.Tk()
root.withdraw()


#Input object
inputFile = InputFile()
analyser = Analyser()
print("\n-----------------------------------")
print("Ordina Email Analyser Tool")
print("-----------------------------------\n")
while True:
    print("1. Analyse email")
    print("2. Exit\n")
    option = input("Select an option...\n")
    if option == '1':
        try:
            emailFilePath = filedialog.askopenfilename()
        except FileNotFoundError:
            print("File not found, please try again.")
            emailFilePath = filedialog.askopenfilename()
        emailArray = inputFile.findIPAddressInHeader(emailFilePath)
        urlBodyArray = inputFile.findURLInBody(emailFilePath)
        print(urlBodyArray)
        analyser.jsonPrint(analyser.analyseURL(urlBodyArray))
    elif option == '2':
        exit()
    else:
        option = input("Invalid option, please try again.")
print (emailArray)
# print (urlArray)
print (urlBodyArray)
# test = input("press something to continue")

# analyser.jsonPrint(inputFile.headerDict)


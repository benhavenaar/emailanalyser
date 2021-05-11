from input import Input
import tkinter as tk
from tkinter import filedialog

#open file dialog
root = tk.Tk()
root.withdraw()
emailFilePath = filedialog.askopenfilename()

#Input object
input = Input()
emailArray = input.findIPAddress(emailFilePath)
print (emailArray)

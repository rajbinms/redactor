import tkinter as tk
from functools import partial
from os import path
import fileRedact as fr

# redact text from file
def redactFile():
    filepath= e1.get() # Get file path from user input
    warning1.config(text = "") # Clear all warnings on UI
    # Check if file path has been entered by the user and if it is a file
    if filepath:
        if path.isfile(filepath):
            # redact text that has been highlighted between a '#' character
            key = fr.redact(filepath) #redacts and retruns the key
            key_back.delete(1.0,'end')  # clear all previous keys
            key_back.update()
            key_back.insert(1.0,key) # display the key on UI for user to store
            warning1.config(text = "") # Clear all warnings on UI
        else:
            warning1.config(text = "Is not a file")
    else:
        warning1.config(text = "Please enter file path")

# replace redacted text from file
def unredactFile():
    filepath= e2.get() # Get file path from user input
    key = e3.get() # Get key value from user to undo the redaction
    warning2.config(text = "")
    # Check if file path has been entered by the user and if it is a file
    if filepath:
        if path.isfile(filepath):
            print("file is true: ", filepath)
            # Check if key is entered by the user
            if key:
                decode_key = fr.set_key(key) # restructure key for a 1 by 2 list
                # check if key structure matches requirement
                if len(decode_key)==2:
                    # undo redaction and create a new file of unredacted text
                    fr.release(filepath,decode_key) 
                    warning1.config(text = "")
                else:
                    warning2.config(text = "Error in key")
            else:
                warning2.config(text = "Please enter Key")
        else:
            warning2.config(text = "Is not a file")
    else:
        warning2.config(text = "Please ? file path")
    

window = tk.Tk()
window.title("Redact Documents")
window.geometry("600x500")

title = tk.Label(window,text="Redact Sensitive Information")
title.grid(row=0,column=0,columnspan=7)

# variables for user inputs
e1 = tk.StringVar()
e2 = tk.StringVar()
e3 = tk.StringVar()


# redaction input UI -----
l1 = tk.Label(window,text="File path")
l1.grid(row=1,column=0,columnspan=3)


enrty1 = tk.Entry(window,width = 40, textvariable = e1)
enrty1.grid(row=1, column =3, columnspan=2)


b1 = tk.Button(window,text = "Redact",width=12,command = redactFile)
b1.grid(row=1,column=5, columnspan=1)

keylabel = tk.Label(window,text="Please store Key for decoding")
keylabel.grid(row=2,column=3,columnspan=3)

key_back = tk.Text(window, fg="blue", bg = "white", height =2, width = 20)
key_back.grid(row=2,column=5,columnspan=1)

warning1 = tk.Label(window,text="", fg="red")
warning1.grid(row=3,column=0,columnspan=7)

# Undo redaction input UI -----
title2 = tk.Label(window,text="Open Redacted text")
title2.grid(row=4,column=0,columnspan=7)

l2 = tk.Label(window,text="File path")
l2.grid(row=5,column=0,columnspan=3)

enrty2 = tk.Entry(window,width = 40, textvariable = e2)
enrty2.grid(row=5, column =3, columnspan=2)

l3 = tk.Label(window,text="Key")
l3.grid(row=6,column=0,columnspan=3)
enrty3 = tk.Entry(window,width = 40, textvariable = e3)
enrty3.grid(row=6, column =3, columnspan=2)


b2 = tk.Button(window,text = "Clear Redaction",width=12,command = unredactFile)
b2.grid(row=6,column=5, columnspan=1)


warning2 = tk.Label(window,text="", fg="red")
warning2.grid(row=7,column=0,columnspan=7)


window.resizable(True,True)
window.mainloop()
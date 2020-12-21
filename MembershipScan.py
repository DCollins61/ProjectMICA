import os
import csv
import sqlite3 as lite
from tkinter import *
import tkinter as tk
import tkinter.messagebox as tkm


def menu():
    
    
    con = lite.connect('member_data.db')
    input()
    with con:
        cur = con.cursor()
        cursor = cur.execute("SELECT * from Members;")
        num = len(cur.fetchall())
        cur.close()

   
    def closeWindow():
        exit()

    root = Tk()

    root.geometry('250x200')
    root.title("Membership Menu")

    varNumMembers = StringVar()
    varNumMembers.set(num)

    textNumMembers = Label(root, text = "Number of current members:").pack()
    numMembers = Label(root,textvariable = varNumMembers).pack()

    scanBTN = tk.Button(root, text="Automatic Entry", width = '15', state = tk.DISABLED, command = scanCard)
    manualBTN = tk.Button(root, text="Manual Entry", width = '15', command = manualAdd)
    exitBTN = tk.Button(root, text="Exit", width = '15', command = closeWindow)

    scanBTN.pack(pady=5)
    manualBTN.pack(pady=5)
    exitBTN.pack(pady=5)
    
    root.mainloop()


#Creates a form for manual entries
def manualAdd():

    def submit(event):
        firstInput = firstNameEntry.get()
        lastInput = lastNameEntry.get()
        licenseInput = licenseNoEntry.get()
        stateInput = stateEntry.get()

        entries = [firstInput, lastInput, licenseInput, stateInput]

        dataBase(entries)

        root.destroy()

        return

    root = Tk()

    firstNameVar = tk.StringVar()
    lastNameVar = tk.StringVar()
    licenseNoVar = tk.StringVar()
    stateVar = tk.StringVar()

    root.geometry('500x500')
    root.title("Membership Registration Form")
    label_0 = Label(root, text="Membership Registration",width=20,font=("bold", 20))
    label_0.place(x=90,y=53)
    firstName = Label(root, text="First Name",width=20,font=("bold", 10))
    firstName.place(x=80,y=130)
    firstNameEntry = Entry(root, textvariable = firstNameVar)
    firstNameEntry.place(x=240,y=130)


    lastName = Label(root, text="Last Name",width=20,font=("bold", 10))
    lastName.place(x=68,y=180)
    lastNameEntry = Entry(root, textvariable = lastNameVar)
    lastNameEntry.place(x=240,y=180)

    licenseNo = Label(root, text="License No.",width=20,font=("bold", 10))
    licenseNo.place(x=70,y=230)
    licenseNoEntry = Entry(root, textvariable = licenseNoVar)
    licenseNoEntry.place(x=240,y=230)

    state = Label(root, text="State (Abbreviation)",width=20,font=("bold", 10))
    state.place(x=70,y=280)
    stateEntry = Entry(root, textvariable = stateVar)
    stateEntry.place(x=240,y=280)

    submitBTN = Button(root, text='Submit',width=20,bg='brown',fg='white')
    submitBTN.place(x=180,y=380)
    submitBTN.bind("<Button-1>", submit)

    # it is use for display the registration form on the window
    root.mainloop()
    
    return

# Reads the input from the scanner into a temporary .txt file.
def scanCard():

    top = Toplevel()
    #Message(top, text="Scan Now", padx = 20, pady = 20).pack()

    text = Text(top).pack()

    top.after(30000, top.destroy)

    with open("scan.txt", 'a') as results_file:
        sentinel = 'ZAA' # ends when this string is seen (last string in file)
        for line in iter(input, sentinel):
            results_file.write(line)
            results_file.write('\n')
    readFile()

    return

# Searches for specific data then adds that data     
def readFile():
    to_store = []    
    with open("scan.txt", 'r') as fin:
        for lns in fin:
            #Prefixes may not be the same for each state
            if lns.startswith("DAQ"):
               to_store.append(lns)
            elif lns.startswith("DAC"):
               to_store.append(lns)
            elif lns.startswith("DCS"):
                to_store.append(lns)
            elif lns.startswith("DAJ"):
                to_store.append(lns)
    fin.close()
    os.remove("scan.txt")
    slimDown(to_store)

    return

#Removes the prefixes and newline character from each piece of data
def slimDown(data):
    index = 0
    for each in data:
        noPrefix = each[3:] #Only keep the data after the third character
        noNewLine = noPrefix.rstrip() #Remove the newline character
        data[index] = noNewLine
        index += 1
    #Orders the data to match the output
    swapPositions(data, 0, 2)
    swapPositions(data, 1, 3)
    input() #Clears the input buffer
    #writeData(data)
    dataBase(data)

    return   

#Writes the wanted data from slimDown() into a .csv
#Uncomment the call in slimDown to enable
def writeData(data):
    with open("data.csv", 'a') as csvFile:
        write = csv.writer(csvFile)
        write.writerow(data)
    csvFile.close()
    
    return

#Sourced from geeksforgeeks.org; generic swap function
def swapPositions(list, pos1, pos2): 
      
    # popping both the elements from list 
    first_ele = list.pop(pos1)    
    second_ele = list.pop(pos2-1) 
     
    # inserting in each others positions 
    list.insert(pos1, second_ele)   
    list.insert(pos2, first_ele)   
      
    return list
#Creates a SQLite3 database
def dataBase(data):
    con = lite.connect('member_data.db')

    with con:
        cur = con.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS Members (first TEXT, last TEXT, number INTEGER, state TEXT);")
        cur.execute("INSERT INTO Members VALUES (?, ?, ?, ?);", (data[0], data[1], data[2], data[3]))

        cur.execute("SELECT * FROM Members")
        results = cur.fetchall()

    return

menu()
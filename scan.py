import os
import csv
import sqlite3 as lite

# Reads the input from the scanner into a temporary .txt file.
def scanCard():
    print("Awaiting input...")
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
    data.append(input("Scan a drink: "))
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

        cur.execute("CREATE TABLE IF NOT EXISTS Members (first TEXT, last TEXT, number INTEGER, state TEXT, drink TEXT);")
        cur.execute("INSERT INTO Members VALUES (?, ?, ?, ?, ?);", (data[0], data[1], data[2], data[3], data[4]))

        cur.execute("SELECT * FROM Members")
        results = cur.fetchall()
        #print(results)
    #scanCard() #Uncomment to enable continuous scans

scanCard()


# IO.py
import csv
import datetime
from fuzzywuzzy import fuzz

fileName = 'data.csv'

# Read the whole list to a formatted string
def readAll():
    returnString = "---The shooping List--- \n"
    with open (fileName, mode='r') as data_file:
        dta_reader = csv.reader(data_file,delimiter=',')
        lineCount = 1
        for row in dta_reader:
            returnString = returnString + str(row[0]) + '---added at-----' + str(row[1]) + '\n'
        return returnString

# Write an item in need to buy to the end of file
# If already exit a close copy, do nothing
def writeOBJ(name):
    existingName = searchOBJ(name)
    if (existingName =='None'or fuzz.ratio(existingName,name)!=100):
        curr_time = datetime.date.today()
        name = name.lower()
        with open (fileName,mode='a') as data_file:
            dta_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            dta_writer.writerow([name,curr_time])

# Loop through database to find potential match from an object
# If no close match found, return "None"
def searchOBJ(name):
    dtaList = []
    name = name.lower()
    with open (fileName,mode='r') as data_file:
        dta_reader = csv.reader(data_file,delimiter=',')
        for row in dta_reader:
            if (len(row)==0):
                continue
            dtaList.append((row[0],fuzz.partial_ratio(row[0],name),row[1]))
    if (len(dtaList)==0):
        return "None"
    dtaList.sort(key= lambda x:x[1])
    if (dtaList[0][1]>=90):
        return dtaList[0][0]
    else:
        return "None"

# Delete an entry (prequisite:name is an exacat entry)
def deleteOBJ(name):
    dtaList = []
    with open (fileName,mode='r') as data_file:
        dta_reader = csv.reader(data_file,delimiter=',')
        for row in dta_reader:
            if (len(row)==0):
                continue
            elif (row[0]==name):
                pass
            else:
                dtaList.append((row[0],row[1]))
    with open (fileName,mode='w') as data_file:
        dta_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for item in dtaList:
            dta_writer.writerow([item[0],item[1]])

#Delete all entry 
def newList():
    with open(fileName,mode='w+') as data_file:
        pass



if __name__ == "__main__":
    print(readAll())
    writeOBJ("apple")
    writeOBJ("apple1")
    print (searchOBJ("apple"))
    deleteOBJ("apple")
    print (searchOBJ("apple"))

"""
Title:      Extract Data from Nord Pool
Author:     Aleksander B. Jakobsen
Created:    Wed Jan 29 10:35:57 2020

"""

###Extract CORRECT data from the server


import datetime 
import urllib.request
import csv
def extractDayAhead():
    
    #Find current year
    now = datetime.datetime.now()
    year = now.year
    
    #Find current weeknumber
    weekNumber = datetime.datetime.today().isocalendar()[1]
   
    #If the weekNumber needs a zero in front 
    if (weekNumber < 10):
        weekNumber = '0' + str(weekNumber)
    #If the weekNumber does not need a 0 in front
    else:
        weekNumber = str(weekNumber)
        
    #For server acsess
    year = str(year) #Convert year to a string
    yearNumber= str(year[:-2]) #Extract the current year number 

    #The correct file in the FTP server
    baseUrl = #NOTE: the url is removed. This url is condifential and was given for project use only.
    weeklyFileName = baseUrl + yearNumber + weekNumber + '.sdv'
    
    #print(weeklyFileName)
    
    #Retrieve data from server and save in a .csv file 
    weeklyFile = urllib.request.urlretrieve(weeklyFileName,"weeklyData.csv") 
  
    #Create a new csv that contains the data nicely sorted and readable for future use
    info = []
    columns = "City, Date, 00-01, 01-02, 02-03, 03-04, 04-05, 05-06, 06-07, 07-08, 08-09, 09-10, 10-11, 11-12, 12-13, 13-14, 14-15, 15-16, 16-17, 17-18, 18-19, 19-20, 20-21, 21-22, 22-23, 23-24"
    # Open a new csv file
    with open('dayAheadKristiansand.csv','w+') as dayAhead:
        
        #Write a nice header in the file
        dayAhead.write(columns + '\n')
        #Extract the wanted data from the downloaded file
        with open('weeklyData.csv' ,encoding="utf8",errors='ignore') as csvfile:
            dataReader = csv.reader(csvfile,delimiter=";")
            #Iterate through the rows in the downloaded file
            for row in dataReader:
                #Check for day ahead prices (marked as D in file) for Kristiansand
                if ('Kristiansand' in row and row[1] == 'D'):
                    #Append the wanted row to a temporary matrix
                    info.append(row)
        #Run through the information that has been deemed interesting            
        for i in info:
            for j in i:
                #Create a temporary string of data of interest
                tempString = ''
                for j in range(7,32,1):
                    if str(i[j]): 
                        #Make it nice and writable
                        tempString += str(i[j]).replace(',','.') + ','
            #Write the desired data to the new file
        
            dayAhead.write(i[6]+','+i[5] +','+tempString+ '\n')
        
    
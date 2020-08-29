
"""
Title:      Find relevant prices
Author:     Aleksander B. Jakobsen
Created:    Wed Jan 29 17:15:36 2020


"""

import os
import csv
import numpy as np
import datetime
import time
import sys
            
def extractFromCsv():
    #Find the current working directory and correct file
    root = os.getcwd()
    print("This is the root", root)
    #absPath = root + '/com/pcf/dayAheadKristiansand.csv'
    absPath = root + '\dayAheadKristiansand.csv'
    
    #Open the file, seperate the values by commas.
    with open(absPath,'r') as prices:
        reader = csv.reader(prices,delimiter=',')
        #Create a row counter to eliminate the header
        rowCount = 0
        pricesVector = []
        for row in reader:
            if (rowCount >= 1):
                #Append the prices to a vector
                for i in range(2,len(row)-1):
                    pricesVector.append(float(row[i]))
            rowCount += 1
        

    #Check how many days and entries per day    
    sumDays = rowCount - 1 #-1 to account for header
    sumPricesPerDay = int(len(pricesVector)/sumDays)
    print("sumDays:",sumDays)    
    #If there are 24 price entries in a day:
    if sumPricesPerDay == 24:
        #Then the time interval between each price is 3600 seconds
        timeInterval = 3600
    else:
        print("Not correct amount of prices per day, look into files")    
        
        
    #Get current monday
    today = datetime.datetime.today()
    monday = today - datetime.timedelta(days=today.weekday())
    mondayStr = str(monday)
    year = mondayStr[:4]
    month=mondayStr[5:7]
    day = mondayStr[8:10]
    #print("Year:",year,"Month:",month,"Day:",day)
    year = int(year)
    month=int(month)
    day=int(day)
    
    
    #Create time vector
    #Get current monday as a timestamp
    baseTime = int(datetime.datetime.timestamp(datetime.datetime(year,month,day))) + time.altzone-time.timezone
    #Get the total amount of time, in seconds
    totalAmountOfSeconds = sumDays*sumPricesPerDay*timeInterval
    #Create a list of timestamps for every hour
    dateList = np.asarray([baseTime + x for x in range(0, totalAmountOfSeconds,timeInterval)]).astype(int)    
    #Get current day
    todayDateTime = str(datetime.datetime.now())
    todayDate = todayDateTime[:10] + " 12:00:00.000000" #prices ahead of in time after noon extraction
    #Get current day as timestamp
    todayDateTimestamp = datetime.datetime.timestamp(datetime.datetime.strptime(todayDate, '%Y-%m-%d %H:%M:%S.%f'))
    #print(todayDateTimestamp)  
      
    #Search for the right date in dateList
    indexOfRightTimestamp = np.asarray(list(np.where(todayDateTimestamp - dateList[:] <= timeInterval)))
    
    
    #Check if there actually are any correct timestamps
    try:
        if indexOfRightTimestamp.any() == False:
            raise ValueError
    except ValueError:
        sys.exit('Timestamps doesnt match')
    
    
    #Extract the first timestamp
    indexOfRightTimestamp = indexOfRightTimestamp[0,0]
    #print(indexOfRightTimestamp)
    
    #How many prices are in front of the timestamp
    numberOfPricesAhead = len(dateList) - indexOfRightTimestamp
    

    #Create a vector of the prices ahead in time
    pricesVector = pricesVector[indexOfRightTimestamp:indexOfRightTimestamp+numberOfPricesAhead]
    print(pricesVector)
    print(int(len(pricesVector)))
    #Create a list of timestamps for that period of prices
    timeStampOfActualPeriod = dateList[indexOfRightTimestamp:indexOfRightTimestamp+numberOfPricesAhead]
    
    
    resolutionPerDay = sumPricesPerDay + 12 

    return pricesVector, timeInterval, resolutionPerDay, timeStampOfActualPeriod
    

extractFromCsv()

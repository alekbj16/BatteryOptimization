# -*- coding: utf-8 -*-
"""
Title:      Various year analysis
Author:     Aleksander B. Jakobsen
Created:    Wed May 13 18:36:58 2020


"""

from __future__ import division
import numpy as np
from com.readInSwitchVectorFromActualPeriod import readInSwitchVectorFromActualPeriod
from com.pcf.extractDataFromCorrectCsv import extractFromCsv
from com.pcf.extractDayAhead import extractDayAhead
from opt.optimization import optimization
from com.pcf.returnAllPricesYearly import returnAllPricesYearly
import csv
#from opt.glpk import glpk
#from opt.glpk2 import glpk
import matplotlib.pyplot as plt
import time
import os
import sys
import random
from matplotlib import style
import statistics

#Optimal capacity to power ratio
capToPow = 6

#Years 20XX(ending) that will be researched
years = [10,11,12,13,14,15,16,17,18,19]
#years = [10] 


yearlyEarnings = []
meanSDdayAhead = []
earningsCapacity = []

#Set battery parameters
EelMax = 3.416*6                          #kWh
SOC = 0.3           #- starting SOC for simulation purposes
SOCinit = SOC*EelMax                    #kWh
powerChange = 1                         #x-times greater output power
upperBoundary = 0.9*EelMax              #kWh
lowerBoundary = 0.1*EelMax              #kWh
U0 = 52.5                                 #V/DC
I0=58.8    
#Find the current
#I0 = (EelMax*1000)/(U0*capToPow) #Amps/DC

#Rest of parameters
eta_in = 0.99                       #-
eta_out = 0.99                          #-
eta_bat = 0.99                          #-
linearLosses = ((U0*I0)*((1-eta_bat)/2)) #kWh

#Simulate for all the years
for i in range(0,len(years)):
    
    #Start every yearly simulation with a clean battery state
    uFix=[]
    state = ([EelMax, SOCinit, powerChange, upperBoundary, lowerBoundary, U0, I0, eta_in, eta_out, linearLosses, uFix]) 
    
    #Get prices for the respecitve year
    psuedoCosts, timeInterval, sumPrices, timeStampofActualPeriod = returnAllPricesYearly(years[i])
    
    #Account for MWh to kWh
    for l in range (0,len(psuedoCosts)):
        psuedoCosts[l] = psuedoCosts[l]/1000
        
    resolutionPerDay = int(24)
    simTime = int(resolutionPerDay*1.5) #Simulation time
    timeInterval = 3600 #Time in seconds
    
    #Every year starts with same SOC
    initialSOC = SOCinit
    
    #Days to simulate
    sumDays = int(len(psuedoCosts)/24)
    #sumDays = 10
    dailyEarnings = [0]*sumDays
    
    #Empty string
    tmpStr = ','
    totalEarnings = 0
    earningsVector = [] #earning for each day of the year
    dailyStandardDeviations = []
    
    #Daily simulations so to not crack my RAM
    for i in range(1,sumDays):
        
        #Set the daily state
        state = ([EelMax, SOCinit, powerChange, upperBoundary, lowerBoundary, U0, I0, eta_in, eta_out, linearLosses, uFix])
            
        #Generate daily price vector
        j = i-1
        lowerValue = int((resolutionPerDay/2 + 1) + resolutionPerDay*j) #Start at noon
        upperValue = int((resolutionPerDay/2 + 1) + simTime + resolutionPerDay*j) #End at midnight next day
        dailyVector = psuedoCosts[lowerValue:upperValue]
        #print(dailyVector)
        #Execute optimization based on "daily" price vector
        u, SOCcalc, ACPower, uChargeVector, uDischargeVector = optimization(simTime, timeInterval,dailyVector,state)
        
        #The next simulated day should be initialized with the SOC where this one ends
        SOCinit = SOCcalc[25]*EelMax #might be one off
        #Earning calulations based on only 24hrs
        prices = np.array(dailyVector[:24])
        dailyEarnings[j] = np.array(ACPower[:24]).dot(prices).T 
        tmpStr += (str(dailyEarnings[j])+',')
        totalEarnings += dailyEarnings[j] 
        earningsVector.append(dailyEarnings[j])
    
        #Standard deviation day-ahead price
        sDeviationDayAhead = statistics.stdev(prices)
        dailyStandardDeviations.append(sDeviationDayAhead)
    
    #Append the total earnings to list of yearly earning
    yearlyEarnings.append(totalEarnings)
    
    #Find the mean of the daily standard deviations of a year
    meanSDeviationDayAhead = statistics.mean(dailyStandardDeviations)
    
    #Append it for future comparison
    meanSDdayAhead.append(meanSDeviationDayAhead)
    
#What are the yearly earnings per capacity     
for l in range (0,len(yearlyEarnings)):
    earningsCapacity.append((yearlyEarnings[l])/(EelMax))
    earningsCapacity[l] = -earningsCapacity[l] #account for negative 
    
    
print("Finished!")
#Create figure
plt.figure(1)
plt.clf
plt.plot(meanSDdayAhead,earningsCapacity,'o',markerfacecolor='blue', markersize=4)
plt.ylim(0,9)
plt.xlim(0.01,0.04)
plt.ylabel('Earnings/Capacity (NOK/kWh/y)')
plt.xlabel('Mean standard deviation of daily day-ahead prices (NOK/kWh)')

n = [2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
for i, txt in enumerate(n):
    plt.annotate(txt, (meanSDdayAhead[i], earningsCapacity[i]))

plt.show()

#More statistics
from scipy.stats import pearsonr
corr = pearsonr(meanSDdayAhead,earningsCapacity)
print("Pearsons correlation: ",corr)    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
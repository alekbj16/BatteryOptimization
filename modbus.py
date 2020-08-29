# -*- coding: utf-8 -*-
"""
Title:      Set active modbus power value
Author:     Aleksander B. Jakobsen
Created:    Sat May 16 18:12:36 2020
"""

import sys
from pymodbus3.client.sync import ModbusTcpClient
from readInSwitchVector import readInSwitchVector
from readInSwitchVectorFromActualPeriod import readInSwitchVectorFromActualPeriod
import time

def switchVectorToOutput():
    
    #Get timestamp, switchvector and timeinterval
    timeStamp, switchVector, timeInterval = readInSwitchVector()

    #Get the actual switchvector
    u = readInSwitchVectorFromActualPeriod(timeStamp,timeInterval)

    #Establish connection 
    try:
        c = ModbusTcpClient(host="192.168.1.5",port=502)
        c.connect()
        print("Connection sucsessful!")
    except ValueError:
        print("Error connecting")
    
    
    #Set active power control
    setActive = c.write_registers(40151,[0,hex(802),unit=3])
    
    #Current time
    now = time.time()
    x = 0
    
    #Find first greater timestamp (meaning next hour)
    for i in range(0,len(timeStamp)):
        if timeStamp[i] > now:
            x = i
            break
        
    #Finding u-value
    value = u[x]
    
    #DC max-value 
    PDC = 52.5*58.8 #Note, must be changed for various cap-to-pow ratios
    
    #Current opreating DC power
    power = PDC * value
    setPower = hex(power)
    
    #Send to system
    controlPower = c.write_registers(40149,[0,setPower],unit=3)
    
    #Check if set
    check = c.read_holding_registers(40149,2,unit=3)
    checkValue = check.registers[1]
    
    
    if (checkValue == setPower):
        print("System power set to correct value. Take a break and enjoy some coffee")
        
    else: 
        print("You've messed up, make some coffee and get back at it")

    #Close the connection 
    c.close()
    

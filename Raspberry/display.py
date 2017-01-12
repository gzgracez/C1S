#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime

apiKey = "638e3a40768577cc14440e93f78f7085"
lcd = Adafruit_CharLCD()
customerID = "58000d58360f81f104543d82"

lcd.begin(16, 1)

counter = 0

def getCheckingBalance(customerID):
    accounts = getAccounts(customerID)
    checking = 0
    for i in accounts:
        if i["type"].lower() == "checking":
            checking += i["balance"]
    return checking

def getSavingsBalance(customerID):
    accounts = getAccounts(customerID)
    savings = 0
    for i in accounts:
        if i["type"].lower() == "savings":
            savings += i["balance"]
    return savings

def getCreditCardBalance(customerID):
    accounts = getAccounts(customerID)
    credit = 0
    for i in accounts:
        if i["type"].lower() == "credit card":
            credit += i["balance"]
    return credit

def getBalance():
    if counter == 0:
        counter = 1
        return getSavingsBalance(customerID)
    elif counter == 1:
        counter = 2
        return getCheckingBalance(customerID)
    else:
        counter =  0
        return getCreditCardBalance(customerID)

def getAccount():
    if counter == 0:
        return "Savings"
    elif counter == 1:
        return "Checking"
    elif counter == 2:
        return "Credit"

while True:
    lcd.clear()
    lcd.message(getAccount())
    lcd.message('Balance: %d' % getBalance())
    sleep(10)

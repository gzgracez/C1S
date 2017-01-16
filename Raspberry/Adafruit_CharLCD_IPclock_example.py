#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
import json
from time import sleep, strftime
from datetime import datetime
import requests

apiKey = "638e3a40768577cc14440e93f78f7085"
lcd = Adafruit_CharLCD()
customerID = "58000d58360f81f104543d82"
cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
counter = 0

lcd.begin(16, 1)

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

def getAccounts(customerID):
    accountsUrl = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerID, apiKey)
    accountsResponse = requests.get(accountsUrl)
    if accountsResponse.status_code == 200:
        accounts = json.loads(accountsResponse.text)
        return accounts
    else:
        return None

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
    global counter
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
    global counter
    if counter == 0:
        return "Savings"
    elif counter == 1:
        return "Checking"
    elif counter == 2:
        return "Credit"

while 1:
    lcd.clear()
    ipaddr = run_cmd(cmd)
    lcd.message(getAccount() + "\n")
    x = getBalance()
    lcd.message('Balance: %s' % str(x))
    sleep(5)

from flask import Flask
from flask import render_template
import requests
import json
import sys
sys.path.append('../Alexa')
from helpers import getAccounts, getAccountAndBalance, getCheckingBalance, getTotalBalance
# import ../AlexaSkill/helpers.py

app = Flask(__name__)

API_KEY = "638e3a40768577cc14440e93f78f7085"
BASE_NESSIE_URL = "http://api.reimaginebanking.com/"
customerID = "58000d58360f81f104543d82" #TODO: change this because this is zuck

@app.route('/')
def home():
    return render_template("home.html")

@app.route("/accounts")
def listAccounts():
    result = getAccountAndBalance(customerID)
    ab = []
    for key in result:
        account = result[key]
        ab.append({"type": account[0], "balance": account[1]})
    #li = [{"type": "hi", "balance": 20}, {"type": "bi", "balance": 200}]
    return render_template("listAccounts.html", customers=ab,
        checkingTotal = getCheckingBalance(customerID),
        totalBalance = getTotalBalance(customerID))

    # go through nessie APi
    # list accounts and balancee

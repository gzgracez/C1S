from flask import Flask
from flask import render_template
import requests
import json
app = Flask(__name__)

API_KEY = "638e3a40768577cc14440e93f78f7085"
BASE_NESSIE_URL = "http://api.reimaginebanking.com/"

@app.route('/')
def home():
    return render_template("home.html")

@app.route("/accounts")
def listAccounts():
    #TODO: replace bottom code with helper.py
	accountsUrl = 'http://api.reimaginebanking.com/accounts?key={}'.format(API_KEY)
	accountsResponse = requests.get(accountsUrl)
	if accountsResponse.status_code == 200:
		accounts = json.loads(accountsResponse.text)
    #li = [{"type": "hi", "balance": 20}, {"type": "bi", "balance": 200}]
    return render_template("listAccounts.html", customers=li)
    # go through nessie APi
    # list accounts and balancee

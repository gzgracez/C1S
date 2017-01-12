from flask import Flask, render_template, session, redirect, request, flash, url_for
import requests
import json
import sys
import os
sys.path.append('../Alexa')
from helpers import getAccounts, getAccountAndBalance, getCheckingBalance, getTotalBalance
# import ../AlexaSkill/helpers.py

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = os.urandom(12)

API_KEY = "638e3a40768577cc14440e93f78f7085"
BASE_NESSIE_URL = "http://api.reimaginebanking.com/"
customerID = "58000d58360f81f104543d82" #TODO: change this because this is zuck

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for("login"))
    else:
        return render_template("home.html")

@app.route('/login', methods=["GET", 'POST'])
def login():
    if request.method == "POST" and request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        return redirect(url_for("home"))
    else:
        flash("Try again")
        return render_template("login.html")

@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect("/")

@app.route("/accounts")
def listAccounts():
    if not session.get('logged_in'):
        flash("Not logged in!")
        return redirect(url_for("login"))
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

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

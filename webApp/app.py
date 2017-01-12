from flask import Flask
from flask import render_template
app = Flask(__name__)

API_KEY = "638e3a40768577cc14440e93f78f7085"

@app.route('/')
def home():
    return render_template("home.html")

@app.route("/accounts")
def listAccounts():
    li = [{"type": "hi", "balance": 20}, {"type": "bi", "balance": 200}]
    return render_template("listAccounts.html", customers=li)
    # go through nessie APi
    # list accounts and balancee

import requests
import json

apiKey = "638e3a40768577cc14440e93f78f7085"

def getAccounts():
	accountsUrl = 'http://api.reimaginebanking.com/accounts?key={}'.format(apiKey)
	accountsResponse = requests.get(accountsUrl)
	if accountsResponse.status_code == 200:
		accounts = json.loads(accountsResponse.text)
	return accounts

def getTotalBalance():
	accounts = getAccounts()
	current = 0
	for i in accounts:
		if i["type"].lower() == "credit card":
			current -= i["balance"]
		elif i["type"].lower() == "checking":
			current += i["balance"]
		else:
			continue
	return current

if __name__=="__main__":
    print getTotalBalance()
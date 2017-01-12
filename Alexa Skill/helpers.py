import requests
import json

apiKey = "638e3a40768577cc14440e93f78f7085"

def getAccounts(customerID):
	accountsUrl = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerID, apiKey)
	accountsResponse = requests.get(accountsUrl)
	if accountsResponse.status_code == 200:
		accounts = json.loads(accountsResponse.text)
		return accounts
	else:
		return None

def getTotalBalance(customerID):
	accounts = getAccounts(customerID)
	current = 0
	for i in accounts:
		if i["type"].lower() == "credit card":
			current -= i["balance"]
		elif i["type"].lower() == "checking":
			current += i["balance"]
		else:
			continue
	return current

def getPurchases(customerID):
	accounts = getAccounts(customerID)
	for i in accounts:
		accountID = i["_id"]
		purchasesUrl = 'http://api.reimaginebanking.com/accounts/{}/purchases?key={}'.format(accountID, apiKey)
		purchasesResponse = requests.get(purchasesUrl)
		print json.dumps(i)

if __name__=="__main__":
    print getPurchases("58000d58360f81f104543d82")
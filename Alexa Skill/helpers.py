import requests
import json

apiKey = "638e3a40768577cc14440e93f78f7085"

# returns array of accounts
def getAccounts(customerID):
	accountsUrl = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerID, apiKey)
	accountsResponse = requests.get(accountsUrl)
	if accountsResponse.status_code == 200:
		accounts = json.loads(accountsResponse.text)
		return accounts
	else:
		return None

# [{accountID, [account name, balance]}]
def getAccountAndBalance(customerID):
	accounts = getAccounts(customerID)
	ab = {}
	for i in accounts:
		ab[i["_id"]] = [i["nickname"], i["balance"]]
	return ab

# returns integer of current balance (checking - credit card)
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
		if purchasesResponse.status_code == 200:
			purchases = json.loads(purchasesResponse.text)
			print purchases
		else:
			return None

if __name__=="__main__":
    # print getPurchases("58000d58360f81f104543d82")
    print json.dumps(getAccountAndBalance("58000d58360f81f104543d82"), indent = 2)
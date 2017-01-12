import requests
import json
import datetime

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

# returns a dictionary: {accountID, [account name, balance]}
def getAccountAndBalance(customerID):
    accounts = getAccounts(customerID)
    ab = {}
    for i in accounts:
        ab[i["_id"]] = [i["nickname"], i["balance"]]
    return ab

# returns integer of current checking balance
def getCheckingBalance(customerID):
    accounts = getAccounts(customerID)
    checking = 0
    for i in accounts:
        if i["type"].lower() == "checking":
            checking += i["balance"]
    return checking

# returns integer of current credit card balance
def getCreditCardBalance(customerID):
    accounts = getAccounts(customerID)
    credit = 0
    for i in accounts:
        if i["type"].lower() == "credit card":
            credit += i["balance"]
    return credit

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

# returns a dictionary of all purchases: {purchaseID, [merchantID, purchaseDate, amount]}
def getPurchases(customerID):
    accounts = getAccounts(customerID)
    for i in accounts:
        accountID = i["_id"]
        purchasesUrl = 'http://api.reimaginebanking.com/accounts/{}/purchases?key={}'.format(accountID, apiKey)
        purchases = {}
        purchasesResponse = requests.get(purchasesUrl)
        if purchasesResponse.status_code == 200:
            purchasesJSON = json.loads(purchasesResponse.text)
            for i in purchasesJSON:
                if i["medium"].lower() == "balance":
                    purchases[i["_id"]] = [i["merchant_id"], i["purchase_date"], i["amount"]]
            return purchases
        else:
            return None

def getCategoryTotalforDOW(customerID, category, day):
    total = 0
    count = 0
    purchases = getPurchases(customerID)
    for i in purchases:
        merchantID = purchases[i][0]
        merchantUrl = 'http://api.reimaginebanking.com/merchants/{}?key={}'.format(merchantID, apiKey)
        merchantResponse = requests.get(merchantUrl)
        if merchantResponse.status_code == 200:
            merchantJSON = json.loads(merchantResponse.text)
            categories = merchantJSON["category"]
            cat = ""
            if len(categories) < 0:
                cat = "misc"
            else:
                cat = categories[0]
            dow = datetime.datetime.strptime(purchases[i][1], '%Y-%m-%d').date().weekday()
            if dow == day and cat == category:
                total += purchases[i][2]
                count += 1
        else:
            continue
    return [total, count]

# calculate suggested spending for a category for today
def calculateSuggested(customerID, category, dow):
    total = getCategoryTotalforDOW(customerID, category, dow)
    avg = total[0] / total[1]
    currentBalance = getTotalBalance(customerID)
    if avg > currentBalance:
        total = getTotalBalance(customerID)
        fraction = total[0] / total
        return fraction * total
    else:
        return avg

if __name__=="__main__":
    print (calculateSuggested("58000d58360f81f104543d82", "food", 3))

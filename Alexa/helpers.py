import requests
import json
import datetime
import pymysql
import sys
#rds settings
rds_host  = "allskill-db.cbzix5fu8xra.us-east-1.rds.amazonaws.com"
name = "allskill"
password = "noskill123"
db_name = "allskill"

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5, port=3306)
except Exception as e:
    print("ERROR: Unexpected error: Could not connect to MySql instance. \nError: {error}".format(error=e))
    sys.exit()

print("SUCCESS: Connection to RDS mysql instance succeeded")

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

# returns integer of actual balance (checking - credit card - allocations)
def getActualBalance(customerID):
    accounts = getAccounts(customerID)
    current = 0
    for i in accounts:
        if i["type"].lower() == "credit card":
            current -= i["balance"]
        elif i["type"].lower() == "checking":
            current += i["balance"]
        else:
            continue
    allocations = getAllocations(customerID)
    for i in allocations:
        current -= i[1]
    return current

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
                    merchantID = i["merchant_id"]
                    merchantUrl = 'http://api.reimaginebanking.com/merchants/{}?key={}'.format(merchantID, apiKey)
                    if purchasesResponse.status_code == 200:
                        merchantsResponse = requests.get(merchantUrl)
                        merchantJSON = json.loads(merchantsResponse.text)
                        purchases[i["_id"]] = [merchantID, i["purchase_date"], i["amount"], merchantJSON["name"]]
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
            if dow == day and cat.lower() == category.lower():
                total += purchases[i][2]
                count += 1
        else:
            continue
    return [total, count]

def getTotalforDOW(customerID, day):
    total = 0
    count = 0
    purchases = getPurchases(customerID)
    for i in purchases:
        dow = datetime.datetime.strptime(purchases[i][1], '%Y-%m-%d').date().weekday()
        if dow == day:
            total += purchases[i][2]
            count += 1
    return [total, count]

# calculate suggested spending for a category for today
# calculateSuggestedByCategory("58000d58360f81f104543d82", "food", 3)
def calculateSuggestedByCategory(customerID, category, dow):
    total = getCategoryTotalforDOW(customerID, category, dow)
    if total[1] == 0: return None
    avg = total[0] / total[1]
    currentBalance = getTotalBalance(customerID)
    if avg > currentBalance:
        totalBalance = getTotalBalance(customerID)
        fraction = total[0] / totalBalance
        return fraction * totalBalance
    else:
        return avg

# calculate suggested spending overall for today
# calculateSuggestedToday("58000d58360f81f104543d82", 3)
def calculateSuggestedToday(customerID, dow):
    total = getTotalforDOW(customerID, dow)
    if total[1] == 0: return None
    avg = total[0] / total[1]
    currentBalance = getTotalBalance(customerID)
    if avg > currentBalance:
        totalBalance = getTotalBalance(customerID)
        fraction = total[0] / totalBalance
        return fraction * totalBalance
    else:
        return avg

def addAllocation(customerID, category, amount, day):
    with conn.cursor() as cur:
        cur.execute('INSERT into allocations (category, amount, customerID, day) values("{}", {}, "{}", "{}");'.format(category, amount, customerID, day))
        conn.commit()
    return True

def getAllocations(customerID):
    with conn.cursor() as cur:
        cur.execute("select * from allocations where customerID='{}'".format(customerID))
        allocations = []
        for row in cur:
            allocations.append(row)
        return allocations

def getAllocationsDate(customerID, date):
    with conn.cursor() as cur:
        cur.execute("select * from allocations where customerID='{}' and day='{}'".format(customerID, date))
        allocations = []
        for row in cur:
            allocations.append(row)
        return allocations

def deleteAllocations(dateString):
    with conn.cursor() as cur:
        cur.execute("delete from allocations where day < '{}';".format(dateString))
        conn.commit()
        return True

def updateAllocations(customerID):
    with conn.cursor() as cur:
        today = datetime.date.today().strftime('%Y-%m-%d')
        return deleteAllocations(today)

# if __name__=="__main__":
#     print getAllocations("58000d58360f81f104543d82")
    # print calculateSuggestedByCategory("58000d58360f81f104543d82", "gas", 2)
    # print addAllocation("58000d58360f81f104543d82", "food", 20, '2017-1-13')
    # print addAllocation("58000d58360f81f104543d82", "food", 15, '2017-1-13')
    # print addAllocation("58000d58360f81f104543d82", "food", 15, '2017-1-13')
    # print updateAllocations("58000d58360f81f104543d82")
    # print getAllocationsDate("58000d58360f81f104543d82","2017-01-12")
    # print json.dumps(getPurchases("58000d58360f81f104543d82"))


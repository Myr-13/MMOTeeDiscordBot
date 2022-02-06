import json

accounts = {
	
}

ACC_EXP = 0
ACC_LEVEL = 1
ACC_MONEY = 2
ACC_EXPFORUP = 3
ACC_RANK = 4
ACC_LANG = 5
ACC_NAME = 6
ACC_INVENTORY = 7
ACC_HP = 8
ACC_MANA = 9
ACC_SUGGESTIONS_NUM = 10

def CreateAccount(user_id, name):
	Can = True
	for acc in accounts:
		if acc == str(user_id) or acc[ACC_NAME] == name:
			Can = False

	if Can == False:
		return 0

	acc = []

	acc.append(0) # Exp
	acc.append(1) # Level
	acc.append(0) # Money
	acc.append(1000) # ExpForUp
	acc.append("Player") # Rank
	acc.append("eng") # Lang
	acc.append(name)
	acc.append([])
	acc.append(10)
	acc.append(10)
	acc.append(0)

	accounts[str(user_id)] = acc

	print("New account, ID: {}".format(user_id))

	return 1

def GetAccountVar(user_id, var_type):
	user_id = str(user_id)

	try:
		return accounts[user_id][var_type]
	except:
		return -1

def SetAccountVar(user_id, var_type, val):
	user_id = str(user_id)

	try:
		accounts[user_id][var_type] = val

		return 1
	except:
		return 0

def SaveAllAccounts():
	file = open("accounts.json", "w")
	json.dump(accounts, file)
	file.close()

	print("All accounts saved!")

def LoadAllAccounts():
	global accounts

	file = open("accounts.json", "r")
	accounts = json.load(file)
	file.close()

	print("All accounts loaded!")

def CheckLevel(user_id):
	user_id = str(user_id)

	try:
		if (accounts[user_id][ACC_EXP] >= accounts[user_id][ACC_EXPFORUP]):
			accounts[user_id][ACC_EXP] -= accounts[user_id][ACC_EXPFORUP]
			accounts[user_id][ACC_LEVEL] += 1
			accounts[user_id][ACC_EXPFORUP] *= 1.5
			accounts[user_id][ACC_EXPFORUP] = int(accounts[user_id][ACC_EXPFORUP])
	except:
		pass

def ShowTop5():
	a = {}

	l = 0
	for i in accounts:
		l += 1

		a[i] = accounts[i][ACC_LEVEL]

		if l > 5:
			continue

	a = sorted(a.items(), key = lambda kv: kv[1])
	a.reverse()

	return a

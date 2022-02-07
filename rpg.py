from items import *
from economy import *
from random import randint

def CheckDeath(user_id):
	if GetAccountVar(user_id, ACC_HP) <= 0:
		return 1

	return 0

def GetMaxHealth(user_id):
	return 10 + GetAccountVar(user_id, ACC_UPGRADE_HP) * 10

def TakeDamage(user_id, dmg):
	SetAccountVar(user_id, ACC_HP, GetAccountVar(user_id, ACC_HP) - dmg)

	return CheckDeath(user_id)

def EnchantItem(user_id, item):
	if GetItemCount(user_id, ITEM_SOUL) <= 10:
		return "Need more souls!"

	if randint(0, GetItemEnchant(user_id, item) + 1) == GetItemEnchant(user_id, item):
		SetItemEnchant(user_id, item, GetItemEnchant(user_id, item) + 1)

		return "Enchanted sucessfuly!"

def Hunt(user_id):
	dmg = randint(0, 5 - GetAccountVar(user_id, ACC_UPGRADE_DEF))

	item = randint(0, 4)
	if item >= 0 and item <= 2:
		item = ITEM_BEEF
	if item == 3:
		item = ITEM_HEAL_POITON
	if item == 4:
		item = ITEM_SOUL

	getCount = 1 + GetAccountVar(user_id, ACC_UPGRADE_HUNT)

	if TakeDamage(user_id, dmg) == 0:
		GiveItem(user_id, item, getCount)
	else:
		SetAccountVar(user_id, ACC_HP, GetMaxHealth(user_id))

		return "You die while hunt :("

	return "**Hunt:**\nYou get {dmg} damage and you get {item} x{count}".format(dmg = dmg, item = GetItemName(item), count = getCount)

def SellItem(user_id, item, count):
	item_name  = GetItemName(item)
	item_count = SellItems(user_id, item, count)
	item_get   = item_count * Costs[item]
	get_exp    = randint(5, 10) * item_count + GetAccountVar(user_id, ACC_UPGRADE_EXP_BONUS) * 10

	SetAccountVar(user_id, ACC_EXP, GetAccountVar(user_id, ACC_EXP) + get_exp)
	CheckLevel(user_id)

	if item_count > 0:
		return "You sell {name} x{count} and get {get} money, {exp} exp".format(name = item_name, count = item_count, get = item_get, exp = get_exp)
	elif item_count == -1:
		return "You can't sell this item"
	else:
		return "You don't have this item"

def UseItem(user_id, item, count):
	item_count = GetItemCount(user_id, item)

	if (item_count < 1):
		return "You don't have this item"
	if (item_count < count):
		count = item_count

	useable = False
	if item == ITEM_HEAL_POITON:
		useable = True

		hp = GetAccountVar(user_id, ACC_HP)
		if hp < 10:
			SetAccountVar(user_id, ACC_HP, hp + 10 * count)
		else:
			return "Your hp is max"
	if item == ITEM_MANA_POITON:
		useable = True

		mana = GetAccountVar(user_id, ACC_MANA)
		if mana < 10:
			SetAccountVar(user_id, ACC_MANA, mana + 10 * count)
		else:
			return "Your mana is max"

	RemItem(user_id, item, count)

	if useable:
		return "You use {name} x{count}".format(name = GetItemName(item), count = count)
	else:
		return "You can't use it"

def BuyItem(user_id, id, count):
	cost = GetItemBuyCost(Sells[id]) * count

	if GetAccountVar(user_id, ACC_MONEY) < cost:
		return "You need {} money for buy this".format(cost)

	GiveItem(user_id, Sells[id], count)
	SetAccountVar(user_id, ACC_MONEY, GetAccountVar(user_id, ACC_MONEY) - cost)

	return "You buy {name} x{count}".format(name = GetItemName(Sells[id]), count = count)

def GetUpgradeName(id):
	a = ["Health upgrade +10 hp", "Defend upgrade +1 def", "Hunt upgrade +1 hunt item", "Exp upgrade +10 exp"]

	return a[id]

def UpgradeSkill(user_id, id):
	id = ACC_UPGRADE_HP + id

	if GetAccountVar(user_id, ACC_UPGRADE_POINTS) < 1:
		return "You need more upgrade points"
	
	SetAccountVar(user_id, ACC_UPGRADE_POINTS, GetAccountVar(user_id, ACC_UPGRADE_POINTS) - 1)
	SetAccountVar(user_id, id, GetAccountVar(user_id, id) + 1)

	return "You upgrade successful"

def ProcessCommand(user_id, args):
	command = args[0]

	#if (command == "enchant"):
	#	return EnchantItem(user_id, args[1])
	if (command == "hunt"):
		return Hunt(user_id)
	elif (command == "sell"):
		if len(args) < 3:
			return "$rpg sell <item id> <count>"
		else:
			return SellItem(user_id, int(args[1]), int(args[2]))
	elif (command == "item_list"):
		text = ""

		for k in Names:
			text += str(k) + " -> " + Names[k] + "\n"

		return text
	elif (command == "inventory"):
		text = "Your inventory:\n"

		for it in GetAccountVar(user_id, ACC_INVENTORY):
			if it[1] > 0:
				text += "{name} x{count}\n".format(name = GetItemName(it[0]), count = it[1])

		return text
	elif (command == "use"):
		if len(args) < 3:
			return "$rpg use <item id> <count>"
		else:
			return UseItem(user_id, int(args[1]), int(args[2]))
	elif (command == "buy"):
		if len(args) == 1:
			text = ""

			for i in range(len(Sells)):
				text += "{id}. {name} | {money}\n".format(id = i, name = GetItemName(Sells[i]), money = GetItemBuyCost(Sells[i]))

			return text
		elif len(args) == 2:
			return "$rpg buy <buy id> <count>"
		else:
			return BuyItem(user_id, int(args[1]), int(args[2]))
	elif (command == "upgrade"):
		if len(args) == 1:
			text = ""

			text += "You have {} upgrade points\n".format(GetAccountVar(user_id, ACC_UPGRADE_POINTS))
			for i in range(4):
				text += "{id}. {name} | {level} level\n".format(id = i, name = GetUpgradeName(i), level = GetAccountVar(user_id, ACC_UPGRADE_HP + i))

			return text
		elif len(args) >= 2:
			return UpgradeSkill(user_id, int(args[1]))

	else:
		return "Invalid command"

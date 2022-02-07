from economy import *

ITEM_SCRAP       = 0
ITEM_WOOD        = 1
ITEM_BEEF        = 2
ITEM_BONE        = 3
ITEM_COPPER      = 4
ITEM_COPPER_BODY = 5
ITEM_COPPER_FEET = 6
ITEM_HEAL_POITON = 7
ITEM_MANA_POITON = 8
ITEM_SOUL        = 9

Costs = {}
Costs[ITEM_SCRAP]       = 50
Costs[ITEM_WOOD]        = 75
Costs[ITEM_BEEF]        = 100
Costs[ITEM_BONE]        = 200
Costs[ITEM_COPPER]      = 25
Costs[ITEM_HEAL_POITON] = 400
Costs[ITEM_MANA_POITON] = 400

Names = {}
Names[ITEM_SCRAP]       = "Scrap"
Names[ITEM_WOOD]        = "Wood"
Names[ITEM_BEEF]        = "Beef"
Names[ITEM_BONE]        = "Bone"
Names[ITEM_COPPER]      = "Copper ore"
Names[ITEM_COPPER_BODY] = "Copper body"
Names[ITEM_COPPER_FEET] = "Copper feet"
Names[ITEM_HEAL_POITON] = "Heal poiton"
Names[ITEM_MANA_POITON] = "Mana poiton"
Names[ITEM_SOUL]        = "Soul"

Sells = [ITEM_HEAL_POITON, ITEM_MANA_POITON, ITEM_COPPER]

def GiveItem(user_id, item, count):
	inv = GetAccountVar(user_id, ACC_INVENTORY)

	give = True
	for it in inv:
		if it[0] == item:
			it[1] += count

			give = False

	if give:
		inv.append([item, count, 0, 0]) # id, count, setting, enchant

	SetAccountVar(user_id, ACC_INVENTORY, inv)

def GetItemCount(user_id, item):
	inv = GetAccountVar(user_id, ACC_INVENTORY)

	for it in inv:
		if it[0] == item:
			return it[1]

def RemItem(user_id, item, count):
	inv = GetAccountVar(user_id, ACC_INVENTORY)

	for it in inv:
		if it[0] == item:
			it[1] -= count

			if it[1] < 0:
				it[1] = 0

	SetAccountVar(user_id, ACC_INVENTORY, inv)

def SetItemSettings(user_id, item, setting):
	inv = GetAccountVar(user_id, ACC_INVENTORY)

	for it in inv:
		if it[0] == item:
			it[2] = setting

	SetAccountVar(user_id, ACC_INVENTORY, inv)

def GetItemSettings(user_id, item):
	inv = GetAccountVar(user_id, ACC_INVENTORY)

	for it in inv:
		if it[0] == item:
			return it[2]

def SetItemEnchant(user_id, item, enchant):
	inv = GetAccountVar(user_id, ACC_INVENTORY)

	for it in inv:
		if it[0] == item:
			it[3] = enchant

	SetAccountVar(user_id, ACC_INVENTORY, inv)

def GetItemEnchant(user_id, item):
	inv = GetAccountVar(user_id, ACC_INVENTORY)

	for it in inv:
		if it[0] == item:
			return it[3]

def GetItemName(item):
	return Names[item]

def GetItemBuyCost(item):
	return int(Costs[item] * 1.5)

def SellItems(user_id, item, count):
	if GetItemCount(user_id, item) < count:
		count = GetItemCount(user_id, item)

	try:
		SetAccountVar(user_id, ACC_MONEY, GetAccountVar(user_id, ACC_MONEY) + count * Costs[item])
		RemItem(user_id, item, count)
	except:
		return -1

	return count

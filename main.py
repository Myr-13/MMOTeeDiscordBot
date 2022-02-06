import discord as ds
import sys
from discord.utils import get
from localization import *
from economy import *
from rpg import *
'''from mysql.connector import connect, Error

# MySQL
sql_host = "localhost"
sql_user = "root"
sql_password = "root"

sql = connect(host = sql_host, user = sql_user, password = sql_password)
cur = sql.cursor(buffered = True)

cur.execute("use mmotee;")'''

# Discord
client = ds.Client()

@client.event
async def on_ready():
	await client.change_presence(activity = ds.Game("2% Update ($help)"), status = ds.Status.idle)

	print("Logged as {name}".format(name = client.user))

	LoadAllAccounts()

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	user_id = message.author.id
	user_lang = GetAccountVar(user_id, ACC_LANG)
	args = message.content.split(" ")

	# Commands
	if args[0] == "$help":
		emb = ds.Embed(title = "Help info", colour = ds.Color.green())
		#emb.add_field(name = "$client_info", value = "How info about client on server (NOT WORKING)")
		emb.add_field(name = "$new_account", value = Localize(user_lang, "Create new economy account"))
		emb.add_field(name = "$account_info", value = Localize(user_lang, "Show info about account on economy system"))
		emb.add_field(name = "$show_top", value = Localize(user_lang, "Show top of accounts"))
		emb.add_field(name = "$lang", value = Localize(user_lang, "Change lang of bot"))
		emb.add_field(name = "$suggestion", value = Localize(user_lang, "Create suggestion"))
		emb.add_field(name = "$rpg", value = Localize(user_lang, "Mini-game RPG"))

		await message.channel.send(embed = emb)

		return

	'''if args[0] == "$client_info":
		command = "SELECT * FROM tw_users WHERE Nick='{name}';".format(name=args[1])

		cur.execute(command)

		result = cur.fetchall()
		result = ''.join(str(e) for e in result)
		result = result.split(", ")

		emb = ds.Embed(title = "Info about {}".format(args[1]), colour = ds.Color.green())
		emb.add_field(name = "Level:", value = "{}".format(result[5]))
		emb.add_field(name = "Gold: ", value = "{}".format(result[6]))
		emb.add_field(name = "Donate: ", value = "{}".format(result[9]))
		emb.add_field(name = "Killing: ", value = "{}".format(result[18]))

		await message.channel.send(embed = emb)

		return'''

	if args[0] == "$new_account":
		if len(args) == 1:
			await message.channel.send("$new_account <name>")

			return

		if CreateAccount(user_id, args[1]) == 0:
			await message.channel.send(Localize(user_lang, "This account already created!"))

			return

		SaveAllAccounts()

		await message.channel.send(Localize(user_lang, "Your account created!"))

		return

	if args[0] == "$account_info":
		if len(args) == 1:
			level       = GetAccountVar(user_id, ACC_LEVEL)
			exp         = GetAccountVar(user_id, ACC_EXP)
			expneed     = GetAccountVar(user_id, ACC_EXPFORUP)
			money       = GetAccountVar(user_id, ACC_MONEY)
			rank        = GetAccountVar(user_id, ACC_RANK)
			suggestions = GetAccountVar(user_id, ACC_SUGGESTIONS_NUM)
			hp          = GetAccountVar(user_id, ACC_HP)
			mana        = GetAccountVar(user_id, ACC_MANA)

			if (level == -1):
				await message.channel.send(Localize(user_lang, "Can't find this account"))
				return

			emb = ds.Embed(title = Localize(user_lang, "Info of account with name: {}").format(GetAccountVar(user_id, ACC_NAME)), colour = ds.Color.green())
			emb.add_field(name = "Level:", value = "{}".format(level))
			emb.add_field(name = "Exp: ", value = "{exp} / {need}".format(exp = exp, need = expneed))
			emb.add_field(name = "Money: ", value = "{}".format(money))
			emb.add_field(name = "Rank: ", value = "{}".format(rank))
			emb.add_field(name = "Suggestions: ", value = "{}".format(suggestions))
			emb.add_field(name = "Health: ", value = "{}".format(hp))
			emb.add_field(name = "Mana: ", value = "{}".format(mana))

			await message.channel.send(embed = emb)

		else:
			level       = GetAccountVar(args[1], ACC_LEVEL)
			exp         = GetAccountVar(args[1], ACC_EXP)
			expneed     = GetAccountVar(args[1], ACC_EXPFORUP)
			money       = GetAccountVar(args[1], ACC_MONEY)
			rank        = GetAccountVar(args[1], ACC_RANK)
			suggestions = GetAccountVar(args[1], ACC_SUGGESTIONS_NUM)
			hp          = GetAccountVar(args[1], ACC_HP)
			mana        = GetAccountVar(args[1], ACC_MANA)

			if (level == -1):
				await message.channel.send("Can't find this account")
				return

			emb = ds.Embed(title = Localize(user_lang, "Info of account with name: {}").format(GetAccountVar(args[1], ACC_NAME)), colour = ds.Color.green())
			emb.add_field(name = "Level:", value = "{}".format(level))
			emb.add_field(name = "Exp: ", value = "{exp} / {need}".format(exp = exp, need = expneed))
			emb.add_field(name = "Money: ", value = "{}".format(money))
			emb.add_field(name = "Rank: ", value = "{}".format(rank))
			emb.add_field(name = "Suggestions: ", value = "{}".format(suggestions))
			emb.add_field(name = "Health: ", value = "{}".format(hp))
			emb.add_field(name = "Mana: ", value = "{}".format(mana))

			await message.channel.send(embed = emb)

		return

	if args[0] == "$save_accounts":
		if GetAccountVar(user_id, ACC_RANK) != "Admin":
			await message.channel.send(Localize(user_lang, "You are not admin"))
			return
		else:
			SaveAllAccounts()

			await message.channel.send(Localize(user_lang, "All accounts saved"))

		return

	if args[0] == "$load_accounts":
		if GetAccountVar(user_id, ACC_RANK) != "Admin":
			await message.channel.send(Localize(user_lang, "You are not admin"))
			return
		else:
			LoadAllAccounts()

			await message.channel.send(Localize(user_lang, "All accounts loaded"))

		return

	if args[0] == "$shutdown":
		if GetAccountVar(user_id, ACC_RANK) != "Admin":
			await message.channel.send(Localize(user_lang, "You are not admin"))
		else:
			SaveAllAccounts()

			await message.channel.send(Localize(user_lang, "All accounts saved, shuting down..."))

			sys.exit()

		return

	if args[0] == "$show_top":
		a = ShowTop5()

		emb = ds.Embed(title = Localize(user_lang, "Top 5 of accounts"), colour = ds.Color.green())

		for i in range(len(a)):
			j = a[i]

			emb.add_field(name = "#{}. ".format(i + 1), value = "{name}: {lvl} level".format(name = GetAccountVar(j[0], ACC_NAME), lvl = j[1]))

		await message.channel.send(embed = emb)

		return

	if args[0] == "$lang":
		if len(args) > 1:
			if args[1] == "eng" or args[1] == "rus":
				SetAccountVar(user_id, ACC_LANG, args[1])

		return

	if args[0] == "$suggestion":
		text = ""

		for i in range(len(args) - 1):
			text += args[1 + i] + " "

		emb = ds.Embed(title = "New suggestion from {}".format(message.author.name), colour = ds.Color.green())
		emb.add_field(name = "Suggestion:", value = text)
		
		SetAccountVar(user_id, ACC_SUGGESTIONS_NUM, GetAccountVar(user_id, ACC_SUGGESTIONS_NUM) + 1)

		if GetAccountVar(user_id, ACC_RANK) == "Player" and GetAccountVar(user_id, ACC_SUGGESTIONS_NUM) >= 25:
			SetAccountVar(user_id, ACC_RANK, "Creative")

		await message.delete()

		await message.channel.send(embed = emb)

		return

	if args[0] == "$rpg":
		if len(args) == 1:
			await message.channel.send("$rpg <command>\nList of commands: hunt, sell, item_list, inventory, use")

			return

		rpgargs = []
		for i in range(len(args) - 1):
			rpgargs.append(args[i + 1])

		text = ProcessCommand(user_id, rpgargs)

		await message.channel.send(text)

		return

	# Delete message from suggestions
	if message.channel.name == "suggestions":
		await message.delete()

		return

	# Add exp
	SetAccountVar(user_id, ACC_EXP, GetAccountVar(user_id, ACC_EXP) + 10)
	CheckLevel(user_id)

client.run("token")

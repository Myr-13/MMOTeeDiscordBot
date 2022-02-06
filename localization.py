import json

langs = {
	"rus": {
		"This account already created!": "Этот аккаунт уже создан!",
		"Create new economy account": "Создать новый аккаунт в экономический системе",
		"Show info about account on economy system": "Показать информацию о аккаунте в экономической системе",
		"Show top of accounts": "Показать топ аккаунтов",
		"Your account created!": "Твой аккаунт создан!",
		"Info of account with name: {}": "Информация о аккаунте с именем: {}",
		"You are not admin": "Ты не админ",
		"All accounts saved": "Все аккаунты сохранены",
		"Top 5 of accounts": "Топ 5 аккаунтов",
		"Change lang of bot": "Сменить язык бота",
		"Create suggestion": "Создать предложение",
		"All accounts loaded": "Все аккаунты загружены",
		"All accounts saved, shuting down...": "Все аккаунты сохранены, вырубаюсь..."
	}
}

def Localize(lang, string):
	try:
		return langs[lang][string]
	except:
		return string

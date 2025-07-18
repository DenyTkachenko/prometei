from enum import Enum

INCOME_BIRTHDAY_FORMAT = '%d.%m.%Y'
OUT_BIRTHDAY_FORMAT = '%d.%m.%Y'

table_headers_map = {
    "name": "👤 Name",
    "phones": "📞 Phones",
    "email": "📩 Email",
    "birthday": "🎂 Birthday",
    "address": "📍 Address",
    "congratulation_date": "🎉 Congratulation Date",
}

class StreamControlCmd(Enum):
    BACK = "Back"
    FINISH = "Finish"

MODE = "telegram"
TG_TOKEN = "7994558666:AAHfkqLVemKNhkXp2A6GaGzVVibjoE98uhQ"
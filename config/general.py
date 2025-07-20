from enum import Enum

INCOME_BIRTHDAY_FORMAT = '%d.%m.%Y'
OUT_BIRTHDAY_FORMAT = '%d.%m.%Y'

table_headers_map = {
    "Id": "Id",
    "name": "👤 Name",
    "phones": "📞 Phones",
    "emails": "📩 Emails",
    "birthday": "🎂 Birthday",
    "address": "📍 Address",
    "congratulation_date": "🎉 Congratulation Date",
    "title": "💬 Title",
    "description": "📝 Description",
    "tags": "🏷️ Tags",
}

class StreamControlCmd(Enum):
    BACK = "Back"
    FINISH = "Finish"

MODE = "cli"
TG_TOKEN = "7994558666:AAHfkqLVemKNhkXp2A6GaGzVVibjoE98uhQ"
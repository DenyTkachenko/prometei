from prettytable import PrettyTable
from colorama import init, Fore, Style
from views.interfaces import BaseRenderer

init(autoreset=True)

class ContactTableRenderer(BaseRenderer):
    def render(self, records: list[dict]) -> str:
        if not records:
            return Fore.YELLOW + "📭 No contacts found." + Style.RESET_ALL

        headers = records[0].keys()

        colored_headers = [
            Fore.CYAN + Style.BRIGHT + self._emoji_header(field) + Style.RESET_ALL
            for field in headers
        ]

        table = PrettyTable()
        table.field_names = colored_headers

        for record in records:
            row = [record.get(field, "-") for field in headers]
            table.add_row(row)

        return table.get_string()

    def _emoji_header(self, key: str) -> str:

        emoji_map = {
            "name": "👤 Name",
            "phones": "📞 Phones",
            "email": "📩 Email",
            "birthday": "🎂 Birthday",
            "address": "📍 Address",
            "congratulation_date": "🎉 Congratulation Date",
        }
        return emoji_map.get(key, key.capitalize())

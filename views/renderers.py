from prettytable import PrettyTable
from colorama import init, Fore, Style
from views.interfaces import BaseRenderer
from config.general import table_headers_map

init(autoreset=True)

class ContactTableRenderer(BaseRenderer):
    def render(self, records: list[dict]) -> str:
        if not records:
            return Fore.YELLOW + "📭 No contacts found." + Style.RESET_ALL

        headers = records[0].keys()

        colored_headers = [
            Fore.CYAN + Style.BRIGHT + self._header(field) + Style.RESET_ALL
            for field in headers
        ]

        table = PrettyTable()
        table.field_names = colored_headers

        for record in records:
            row = [record.get(field, "-") for field in headers]
            table.add_row(row)

        return table.get_string()

    def _header(self, key: str) -> str:
        return table_headers_map.get(key, key.capitalize())

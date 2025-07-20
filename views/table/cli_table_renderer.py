# renderers/console_table_renderer.py
from prettytable import PrettyTable
from colorama import init, Fore, Style
from views.interfaces import BaseRenderer
from config.general import table_headers_map

init(autoreset=True)

class ConsoleTableRenderer(BaseRenderer):
    def render(self, records: list[dict]) -> str:
        if not records:
            return Fore.YELLOW + "📭 No contacts found." + Style.RESET_ALL

        headers = records[0].keys()
        colored_headers = [
            Fore.CYAN + Style.BRIGHT + table_headers_map.get(f, f.capitalize()) + Style.RESET_ALL
            for f in headers
        ]
        table = PrettyTable()
        table.field_names = colored_headers
        for rec in records:
            table.add_row([rec.get(f, "-") for f in headers])
        return table.get_string()
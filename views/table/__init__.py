from .cli_table_renderer import ConsoleTableRenderer
from .telegram_list_renderer import TelegramListRenderer
from config.general import MODE

if MODE == "telegram":
    TableRenderer = TelegramListRenderer
else:
    TableRenderer = ConsoleTableRenderer
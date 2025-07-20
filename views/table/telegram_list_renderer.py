from views.interfaces import BaseRenderer
from config.general import table_headers_map

class TelegramListRenderer(BaseRenderer):
    def render(self, records: list[dict]) -> str:
        if not records:
            return "🤷‍♂️ No contacts found."

        lines = []
        for rec in records:
            for key, val in rec.items():
                title = table_headers_map.get(key, key.capitalize())
                lines.append(f"{title}: {val or '-'}")
            lines.append("—" * 20)
        return "\n".join(lines[:-1])
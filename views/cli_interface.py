from typing import Tuple
from views.interfaces import BaseInterface

class CLIInterface(BaseInterface):
    """Concrete Interface for command‑line interaction."""

    def send_message(self, user_id: str, text: str) -> None:
        print(text)

    def receive_message(self, prompt: str = "") -> Tuple[str, str]:
        # Prompt on the same line and return what the user typed
        text = input(prompt)
        return "cli", text
from prompt_toolkit import PromptSession

from typing import Tuple
from views.interfaces import BaseInterface

class CLIInterface(BaseInterface):
    """Concrete Interface for command‑line interaction."""
    def __init__(self, prompt_session: PromptSession):
        super().__init__()
        self.prompt_session = prompt_session

    def send_message(self, user_id, text: str) -> None:
        print(text)

    def receive_message(self, user_id, prompt: str = "") -> Tuple[str,str]:
        if not self.prompt_session:
            return "cli", input(prompt)
        return "cli",  self.prompt_session.prompt(prompt)

    #def receive_message(self, prompt: str = "") -> Tuple[str, str]:
        # Prompt on the same line and return what the user typed
    #    text = input(prompt)
    #    return "cli", text
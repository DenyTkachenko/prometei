from prompt_toolkit import PromptSession

from views.interfaces import BaseInterface

class CLIInterface(BaseInterface):
    """Concrete Interface for command‑line interaction."""
    def __init__(self, prompt_session: PromptSession):
        super().__init__()
        self.prompt_session = prompt_session

    def send_message(self, user_id, text: str) -> None:
        print(text)

    def receive_message(self, user_id, prompt: str = "") -> str:
        if not self.prompt_session:
            return input(prompt)
        return self.prompt_session.prompt(prompt)

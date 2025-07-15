from views.interfaces import BaseInterface

class CLIInterface(BaseInterface):
    """Concrete Interface for command‑line interaction."""
    def send_message(self, user_id, text: str) -> None:
        print(text)

    def receive_message(self, user_id, prompt: str = "") -> str:
        # Prompt on the same line and return what the user typed
        return input(prompt)
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
        # Prompt on the same line and return what the user typed
        #Закоментований session_prompt, бо працює лише у терміналі
        #Для дебага та запуска проги у консолі IDE залишаю поки звичайний
        #input(prompt). При переході у роботу в терміналі слід розкоментувати
        #return self.prompt_session.prompt(prompt) щоб інтерпретатор підказував команди
        #return self.prompt_session.prompt(prompt)
        return input(prompt)
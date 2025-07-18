from abc import ABC, abstractmethod
from typing import Tuple

class BaseInterface(ABC):
    @abstractmethod
    def send_message(self, chat_id: str, text: str) -> None:
        pass

    @abstractmethod
    def receive_message(self, prompt: str = "") -> Tuple[str, str]:
        """Blocking call or event-driven, depends on implementation."""
        pass

class BaseRenderer(ABC):
    @abstractmethod
    def render(self, data) -> str:
        pass
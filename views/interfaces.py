from abc import ABC, abstractmethod

class BaseInterface(ABC):
    @abstractmethod
    def send_message(self, chat_id: int, text: str):
        pass

    @abstractmethod
    def receive_message(self):
        """Blocking call or event-driven, depends on implementation."""
        pass
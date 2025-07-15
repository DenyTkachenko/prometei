from abc import ABC, abstractmethod
from typing import  Generic, TypeVar

T = TypeVar("T")

class StorageInterface(ABC, Generic[T]):
    @abstractmethod
    def load(self) -> T:
        pass

    @abstractmethod
    def save(self, data: T) -> None:
        pass
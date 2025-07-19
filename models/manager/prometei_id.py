import uuid
from models.field import Field
from utils.custom_exceptions import PrometeiIDValueException


class PrometeiId(Field):

    def __init__(self, promid: str):
        if not isinstance(promid, str):
            raise PrometeiIDValueException()
        self.promid = promid
        self.promguuid = str(uuid.uuid4())
        super().__init__((self.promid, self.promguuid))

    @property
    def promid(self) -> str:
        return self.__promid

    @promid.setter
    def promid(self, promid: str):
        if not isinstance(promid, str):
            raise PrometeiIDValueException()
        self.__promid = promid

    @property
    def promguuid(self) -> str:
        return self.__promguuid

    @promguuid.setter
    def promguuid(self, promguuid):
        self.__promguuid = promguuid






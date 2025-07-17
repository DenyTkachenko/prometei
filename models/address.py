from models.field import Field

class Address(Field):
    def __init__(self, value):
        normalized = value.strip()
        super().__init__(normalized)
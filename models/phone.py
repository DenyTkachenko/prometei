from models.field import Field
from utils.custom_exceptions import PhoneValueException

class Phone(Field):
  def __init__(self, value):
    if not self.validate(value):
      raise PhoneValueException()
    super().__init__(value)

  @staticmethod
  def validate(value):
    return isinstance(value, str) and value.isdigit() and len(value) == 10

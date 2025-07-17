from models.field import Field
from utils.validators import phone_validator

class Phone(Field):
  def __init__(self, value):
    self.validate(value)
    super().__init__(value)

  @staticmethod
  def validate(value):
    return phone_validator(value)

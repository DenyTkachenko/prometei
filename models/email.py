from models.field import Field
from utils.validators import email_validator

class Email(Field):
  def __init__(self, value):
    self.validate(value)
    super().__init__(value)

  @staticmethod
  def validate(value):
      return email_validator(value)

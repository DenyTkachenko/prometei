from models.field import Field

class Name(Field):
  def __init__(self, value):
    if not value or not value.strip():
      raise ValueError("Name cannot be empty")
    normalized = value.strip().capitalize()
    super().__init__(normalized)
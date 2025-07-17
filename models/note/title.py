from models.field import Field

class Title(Field):
  def __init__(self, value):
    if not value or not value.strip():
      raise ValueError("Title cannot be empty")
    normalized = value.strip()
    super().__init__(normalized)
from models.field import Field

class Description(Field):
  def __init__(self, value):
    if not value or not value.strip():
      raise ValueError("Description cannot be empty")
    super().__init__(value)
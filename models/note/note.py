from models.note.title import Title
from models.note.description import Description
import uuid

class Note:
  def __init__(self, title, description):
    self.title = Title(title)
    self.description = Description(description)
    self.id = uuid.uuid4()

  def __str__(self):
    return f"{self.id} | {self.title.value}: {self.description.value}"
  
  def change_description(self, new_description):
    self.description = Description(new_description) 

  def change_title(self, new_title):
    self.title = Title(new_title)
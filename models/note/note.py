from models.manager.prometei_id import PrometeiId
from models.note.title import Title
from models.note.description import Description
import uuid

class Note:
  def __init__(self, title, description, promid: PrometeiId):
    self.title = Title(title)
    self.description = Description(description)
    self._promid = promid

  @property
  def promid(self):
    return self._promid

  def __str__(self):
    return f"{self._promid.value[0]} | {self.title.value}: {self.description.value}"
  
  def change_description(self, new_description):
    self.description = Description(new_description) 

  def change_title(self, new_title):
    self.title = Title(new_title)
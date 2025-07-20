import re
from models.note.tag import Tag
from models.manager.prometei_id import PrometeiId
from models.note.title import Title
from models.note.description import Description
import uuid

class Note:
  def __init__(self, title, description, promid: PrometeiId):
    self._title = Title(title)
    self.description = Description(description)
    self._promid = promid

  @property
  def promid(self):
    return self._promid

  @property
  def title(self):
    return self._title

  @title.setter
  def title(self, title):
     self._title = Title(title)

  def __str__(self):
    return f"{self._promid.value[0]} | {self.title.value}: {self.description.value}"
  
  def change_description(self, new_description):
    self.description = Description(new_description) 

  def change_title(self, new_title):
    self.title = Title(new_title)

  def parse_tags(self):
    found_tags = re.findall(r'#\w+', self.description.value)
    tags_set = set({tag for tag in found_tags})
    tags = list(Tag(tag) for tag in tags_set)
    return tags or []

  def is_tag_in_note(self, tag):
    if not tag.startswith("#"):
        tag = "#" + tag
    return any(tag == tag_value.value for tag_value in self.tags)
import re
from models.note.tag import Tag
from models.note.title import Title
from models.note.description import Description
import uuid

class Note:
  def __init__(self, title, description):
    self.title = Title(title)
    self.description = Description(description)
    self.id = uuid.uuid4()
    self.tags = self.parse_tags()

  def __str__(self):
    return f"{self.id} | {self.title.value}: {self.description.value}"
  
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
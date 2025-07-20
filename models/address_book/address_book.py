from collections import UserDict


from models.manager.manager_prometei_id import ManagerPrometeiId
from utils.date import get_upcoming_birthdays
from utils.custom_exceptions import BirthdayPeriodException
from config.general import OUT_BIRTHDAY_FORMAT
from utils.helpers import notes_to_dict, record_to_dict
from utils.search import search
import copy

class AddressBook(UserDict):
  def __init__(self):
    super().__init__()
    self.contacts = {}
    self.notes = {}
    self._managerID = ManagerPrometeiId()


  @property
  def manager(self):
      return self._managerID
  
  def __setstate__(self, state):
    self.__dict__ = state
    if "contacts" not in self.__dict__:
        self.contacts = {}
    if "notes" not in self.__dict__:
        self.notes = {}

  def add_record(self, record):
    self.contacts[record.promid.value[0]] = record

  def find(self, name):
      normalized = name.strip().lower()
      for record in self.contacts.values():
          if record.name.value.strip().lower() == normalized:
              return record
      return None

  def find_record_by_id(self, promid):
      return self.contacts.get(promid)

  def delete(self, name):
    normalized = name.strip().capitalize()
    return self.contacts.pop(normalized, None)

  def delete_record_by_id(self, promid):
      return self.contacts.pop(promid, None)

  def show_all(self):
    deepcopy_contacts = copy.deepcopy(self.contacts)
    deepcopy_contacts = dict(sorted(deepcopy_contacts.items(), key=lambda item: int(item[0])))
    return [record_to_dict(record) for record in deepcopy_contacts.values()]

  def get_upcoming_birthdays(self, days=7):
    if not isinstance(days, int):
      raise BirthdayPeriodException()
    return get_upcoming_birthdays(records = self.contacts.values(), days = days, out_birthday_format = OUT_BIRTHDAY_FORMAT)
  
  def search(self, query):
    query_lower = query.lower()
    return [
        record_to_dict(record)
        for record in self.contacts.values()
        if query_lower in search(record)
      ]
  

  # ********** Notes **********

  def add_note(self, note):
    self.notes[note.promid.value[0]] = note

  def find_note(self, title):
    return [notes_to_dict(record) for record in self.notes.values() if record.title.value == title]

  def find_note_by_id(self, promid):
      return self.notes.get(promid)

  def delete_note(self, title):
      normalized = title.strip().lower()
      for note_id, note in self.notes.items():
          if note.title.value.strip().lower() == normalized:
              return self.notes.pop(note_id)
      return None

  def delete_note_by_id(self, promid):
      return self.notes.pop(promid, None)

  def show_all_notes(self):
    deepcopy_notes = copy.deepcopy(self.notes)
    deepcopy_notes = dict(sorted(deepcopy_notes.items(), key=lambda item: int(item[0])))
    return [notes_to_dict(record) for record in deepcopy_notes.values()]
  
  def find_notes_by_tag(self, tag):
    return [notes_to_dict(record) for record in self.notes.values() if record.is_tag_in_note(tag)]
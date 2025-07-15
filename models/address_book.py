from collections import UserDict
from utils.date import get_upcoming_birthdays
from utils.custom_exceptions import BirthdayPeriodException
from config.general import OUT_BIRTHDAY_FORMAT

class AddressBook(UserDict):
  def add_record(self, record):
    self.data[record.name.value] = record

  def find(self, name):
    normalized = name.strip().capitalize()
    return self.data.get(normalized)

  def delete(self, name):
    normalized = name.strip().capitalize()
    return self.data.pop(normalized, None)

  def show_all(self):
    if not self.data:
      return "No records found"
    return '\n'.join(str(record) for record in self.data.values())

  def get_upcoming_birthdays(self, days=7):
    if not isinstance(days, int):
      raise BirthdayPeriodException()
    return get_upcoming_birthdays(records = self.data.values(), days = days, out_birthday_format = OUT_BIRTHDAY_FORMAT)
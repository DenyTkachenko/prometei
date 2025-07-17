from models.name import Name
from models.phone import Phone
from models.email import Email
from models.address import Address
from models.birthday import Birthday

class Record:
  def __init__(self, name):
    self.name = Name(name)
    self.phones = []
    self.emails = []
    self.birthday = None
    self.address = None

  def add_phone(self, phone):
    if any(ph.value == phone for ph in self.phones):
      return True
    phone_obj = Phone(phone)
    self.phones.append(phone_obj)

  def add_email(self, email):
    if any(em.value == email for em in self.emails):
      return True
    email_obj = Email(email)
    self.emails.append(email_obj)

  def remove_phone(self, phone):
    for ph in self.phones:
      if ph.value == phone:
        self.phones.remove(ph)
        return True
    return False

  def edit_phone(self, old_phone, new_phone):
    for idx, ph in enumerate(self.phones):
      if ph.value == old_phone:
        if any(p.value == new_phone for p in self.phones):
          self.phones.pop(idx)
        else:
          self.phones[idx] = Phone(new_phone)
        return True
    return False

  def find_phone(self, phone):
    for ph in self.phones:
      if ph.value == phone:
        return ph
    return None

  def add_birthday(self, birthday):
    if self.birthday is not None:
      raise ValueError("Birthday already exists for this contact")
    self.birthday = Birthday(birthday)

  def set_address(self, address):
    self.address = Address(address)

  def __str__(self):
    phones_str = '; '.join(p.value for p in self.phones)
    birthday_str = f", Birthday: {self.birthday.value}" if self.birthday else ""
    email_str = f", Emails: {'; '.join(p.value for p in self.emails)}" if len(self.emails) else ""
    address_str = f", Address: {self.address.value}" if self.address else ""
    return f"{self.name.value}: {phones_str if phones_str else 'No phone numbers found'}{birthday_str}{email_str}{address_str}"

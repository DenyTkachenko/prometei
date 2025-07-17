from models.name import Name
from models.phone import Phone
from models.email import Email
from models.address import Address
from models.birthday import Birthday
from utils.custom_exceptions import PhoneValueException, EmailValueException

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.emails: list[Email] = []
        self.birthday: Birthday | None = None
        self.address: Address | None = None

    def set_name(self, new_name: str) -> None:
        self.name = Name(new_name)

    # Phone methods
    def add_phone(self, phone: str) -> bool:
        if any(p.value == phone for p in self.phones):
            return False
        self.phones.append(Phone(phone))
        return True

    def remove_phone(self, phone: str) -> bool:
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        for idx, p in enumerate(self.phones):
            if p.value == old_phone:
                if any(p2.value == new_phone for p2 in self.phones):
                    raise PhoneValueException(f"⚠️ New phone '{new_phone}' already exists.")
                self.phones[idx] = Phone(new_phone)
                return
        raise PhoneValueException(f"⚠️ Old phone '{old_phone}' not found.")

    # Email methods
    def add_email(self, email: str) -> bool:
        if any(e.value == email for e in self.emails):
            return False
        self.emails.append(Email(email))
        return True

    def remove_email(self, email: str) -> bool:
        for e in self.emails:
            if e.value == email:
                self.emails.remove(e)
                return True
        return False

    def edit_email(self, old_email: str, new_email: str) -> None:
        for idx, e in enumerate(self.emails):
            if e.value == old_email:
                if any(e2.value == new_email for e2 in self.emails):
                    raise EmailValueException(f"⚠️ New email '{new_email}' already exists.")
                self.emails[idx] = Email(new_email)
                return
        raise EmailValueException(f"⚠️ Old email '{old_email}' not found.")

    # Birthday methods
    def set_birthday(self, birthday: str) -> None:
        birthday = Birthday(birthday)
        self.birthday = birthday

    def remove_birthday(self) -> bool:
        if self.birthday:
            self.birthday = None
            return True
        return False

    def set_address(self, address: str) -> None:
        self.address = Address(address)

    def remove_address(self) -> bool:
        if self.address:
            self.address = None
            return True
        return False

    def __str__(self) -> str:
        parts = [f"{self.name.value}"]
        if self.phones:
            phones_str = '; '.join(p.value for p in self.phones)
            parts.append(f"Phones: {phones_str}")
        if self.emails:
            emails_str = '; '.join(e.value for e in self.emails)
            parts.append(f"Emails: {emails_str}")
        if self.birthday:
            parts.append(f"Birthday: {self.birthday.value}")
        if self.address:
            parts.append(f"Address: {self.address.value}")
        return ' | '.join(parts)

from datetime import datetime
from models.field import Field
from config.general import INCOME_BIRTHDAY_FORMAT
from utils.date import date_to_readable_format
from utils.custom_exceptions import BirthdayFormatException

class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, INCOME_BIRTHDAY_FORMAT).date()
            super().__init__(value)
        except ValueError:
            readable_format = date_to_readable_format(INCOME_BIRTHDAY_FORMAT)
            raise BirthdayFormatException(expected_format=readable_format)
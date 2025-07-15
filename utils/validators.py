from datetime import datetime
from config.general import INCOME_BIRTHDAY_FORMAT
from utils.date import date_to_readable_format
from utils.custom_exceptions import BirthdayFormatException

def validate_args(args, arg_order, validators):
    validated_args = {}
    for i, arg_name in enumerate(arg_order):
        if i >= len(args):
            break
        value = args[i]
        validator = validators.get(arg_name)
        if validator:
            try:
                validated_args[arg_name] = validator(value)
            except ValueError as e:
                print(f"❌ Error in '{arg_name}': {e}")
                return None
        else:
            validated_args[arg_name] = value
    return validated_args

def get_validators(cmd_conf):
    validators = {}
    validators.update(cmd_conf.get("args_required", {}))
    validators.update(cmd_conf.get("args_optional", {}))
    return validators

def name_validator(value):
    if not value:
        raise ValueError("Name cannot be empty")
    return value

def phone_validator(value):
    if not isinstance(value, str):
        raise ValueError("Phone number must be a string.")
    digits = value.strip()
    if not digits.isdigit():
        raise ValueError("Phone number must contain only digits.")
    if len(digits) != 10:
        raise ValueError("Phone number must be exactly 10 digits long.")
    return digits

def birthday_validator(value):
    try:
        date_obj = datetime.strptime(value.strip(), INCOME_BIRTHDAY_FORMAT).date()
        return date_obj
    except ValueError:
        readable_format = date_to_readable_format(INCOME_BIRTHDAY_FORMAT)
        raise BirthdayFormatException(expected_format=readable_format)
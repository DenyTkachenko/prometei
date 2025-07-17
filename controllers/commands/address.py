from utils.decorators import input_error
from utils.custom_exceptions import UserNotExistException

@input_error('add-address', ['name', 'address'])
def add_address(args, address_book, **kwargs):
    name, address, *_ = args
    record = address_book.find(name)
    if not record:
        return UserNotExistException(user_name = name)
    try:
        record.set_address(address)
        return f"✅ 📫Address added for {name}."
    except ValueError as e:
        return str(e)

@input_error('remove-address', ['name'])
def remove_address(args, address_book, **kwargs):
    name, *_ = args
    record = address_book.find(name)
    if not record:
        return UserNotExistException(user_name = name)
    try:
        if record.remove_address():
            return f"✅ 📫 Address removed for '{name}'."
        else:
            return f"ℹ️ 📫 No address set for '{name}'."
    except ValueError as e:
        return str(e)
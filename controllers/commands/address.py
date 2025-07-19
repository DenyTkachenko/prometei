from models.address_book.address_book import AddressBook
from utils.decorators import input_error
from utils.custom_exceptions import UserNotExistException

@input_error('add-address', ['promid', 'address'])
def add_address(args, address_book: AddressBook, **kwargs):
    promid, address, *_ = args
    record = address_book.find_record_by_id(promid)
    if not record:
        return UserNotExistException(user_name = record.name.value)
    try:
        record.set_address(address)
        return f"✅ 📫Address added for {record.name.value}."
    except ValueError as e:
        return str(e)

@input_error('remove-address', ['promid'])
def remove_address(args, address_book: AddressBook, **kwargs):
    promid = args[0]
    record = address_book.find_record_by_id(promid)
    if not record:
        return UserNotExistException(user_name = record.name.value)
    try:
        if record.remove_address():
            return f"✅ 📫 Address removed for '{record.name.value}'."
        else:
            return f"ℹ️ 📫 No address set for '{record.name.value}'."
    except ValueError as e:
        return str(e)
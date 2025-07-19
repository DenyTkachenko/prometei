from models.address_book.address_book import AddressBook
from utils.decorators import input_error
from utils.custom_exceptions import UserNotExistException

@input_error('phone', ['promid'])
def show_phone(args, address_book: AddressBook,  **keyword):
    promid = args[0]
    record = address_book.find_record_by_id(promid)
    if not record:
        return UserNotExistException(user_name = record.name.value)
    return '; '.join(p.value for p in record.phones) if record.phones else "No phone records found."

@input_error('change-phone', ['promid', 'old_phone', 'new_phone'])
def change_phone(args, address_book: AddressBook, **kwargs):
    promid, old_phone, new_phone, *_ = args
    record = address_book.find_record_by_id(promid)
    if not record:
        return UserNotExistException(user_name = record.name.value)
    record.edit_phone(old_phone, new_phone)
    return f"✅ Contact '{record.name.value}' updated with phone 📞 {new_phone}"
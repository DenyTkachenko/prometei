from utils.decorators import input_error
from utils.custom_exceptions import UserNotExistException

@input_error('phone', ['name'])
def show_phone(args, address_book,  **keyword):
    name = args[0]
    record = address_book.find(name)
    if not record:
        return UserNotExistException(user_name = name)
    return '; '.join(p.value for p in record.phones) if record.phones else "No phone records found."

@input_error('change-phone', ['name', 'old_phone', 'new_phone'])
def change_phone(args, address_book, **kwargs):
    name, old_phone, new_phone, *_ = args
    record = address_book.find(name)
    if not record:
        return UserNotExistException(user_name = name)
    record.edit_phone(old_phone, new_phone)
    return f"✅ Contact '{name}' updated with phone 📞 {new_phone}"
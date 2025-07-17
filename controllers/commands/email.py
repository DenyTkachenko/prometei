from utils.decorators import input_error
from utils.custom_exceptions import UserNotExistException

@input_error('remove-email', ['name', 'old_email'])
def remove_email(args, address_book, **kwargs):
    name, old_email, *_ = args
    record = address_book.find(name)
    if not record:
        return UserNotExistException(user_name = name)
    record.remove_email(old_email)
    return f"✅ Email 📧 {old_email} removed from contact '{name}'."

@input_error('change-email', ['name', 'old_email', 'new_email'])
def change_email(args, address_book, **kwargs):
    name, old_email, new_email, *_ = args
    record = address_book.find(name)
    if not record:
        return UserNotExistException(user_name = name)
    record.edit_email(old_email, new_email)
    return f"✅ Contact '{name}' updated with email 📧 {new_email}"
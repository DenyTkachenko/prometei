from models.address_book.address_book import AddressBook
from utils.decorators import input_error
from utils.custom_exceptions import UserNotExistException

@input_error('remove-email', ['promid', 'old_email'])
def remove_email(args, address_book: AddressBook, **kwargs):
    promid, old_email, *_ = args
    record = address_book.find_record_by_id(str(promid))
    if not record:
        return UserNotExistException(user_id = str(promid))
    record.remove_email(old_email)
    return f"✅ Email 📧 {old_email} removed from contact '{record.name.value}'."

@input_error('change-email', ['promid', 'old_email', 'new_email'])
def change_email(args, address_book: AddressBook, **kwargs):
    promid, old_email, new_email, *_ = args
    record = address_book.find_record_by_id(str(promid))
    if not record:
        return UserNotExistException(user_id = str(promid))
    record.edit_email(old_email, new_email)
    return f"✅ Contact '{record.name.value}' updated with email 📧 {new_email}"
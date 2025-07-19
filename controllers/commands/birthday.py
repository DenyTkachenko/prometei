from models.address_book.address_book import AddressBook
from utils.decorators import input_error
from views.renderers import ContactTableRenderer
from utils.custom_exceptions import UserNotExistException

@input_error('add-birthday', ['promid', 'birthday'])
def add_birthday(args, address_book: AddressBook, **kwargs):
    promid, birthday, *_ = args
    record = address_book.find_record_by_id(str(promid))
    if not record:
        return UserNotExistException(user_id = str(promid))
    try:
        record.set_birthday(birthday)
        return f"✅ 🎂Birthday added for {record.name.value}."
    except ValueError as e:
        return str(e)

@input_error('remove-birthday', ['promid'])
def remove_birthday(args, address_book: AddressBook, **kwargs):
    promid = args[0]
    record = address_book.find_record_by_id(str(promid))
    if not record:
        return UserNotExistException(user_id = str(promid))
    try:
        if record.remove_birthday():
            return f"✅ 🎂 Birthday removed for '{record.name.value}'."
        else:
            return f"ℹ️ No birthday set for '{record.name.value}'."
    except ValueError as e:
        return str(e)

@input_error('show-birthday', [], [])
def show_birthdays(args, address_book, **kwargs):
    days = args[0] if args and args[0] is not None else 7
    records = address_book.get_upcoming_birthdays(days)
    renderer = ContactTableRenderer()
    return renderer.render(records)

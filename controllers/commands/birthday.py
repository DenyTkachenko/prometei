from utils.decorators import input_error
from views.table import TableRenderer
from utils.custom_exceptions import UserNotExistException

@input_error('add-birthday', ['name', 'birthday'])
def add_birthday(args, address_book, **kwargs):
    name, birthday, *_ = args
    record = address_book.find(name)
    if not record:
        return UserNotExistException(user_name = name)
    try:
        record.set_birthday(birthday)
        return f"✅ 🎂Birthday added for {name}."
    except ValueError as e:
        return str(e)

@input_error('remove-birthday', ['name'])
def remove_birthday(args, address_book, **kwargs):
    name, *_ = args
    record = address_book.find(name)
    if not record:
        return UserNotExistException(user_name = name)
    try:
        if record.remove_birthday():
            return f"✅ 🎂 Birthday removed for '{name}'."
        else:
            return f"ℹ️ No birthday set for '{name}'."
    except ValueError as e:
        return str(e)

@input_error('show-birthday', [], [])
def show_birthdays(args, address_book, **kwargs):
    days = args[0] if args and args[0] is not None else 7
    records = address_book.get_upcoming_birthdays(days)
    renderer = TableRenderer()
    return renderer.render(records)

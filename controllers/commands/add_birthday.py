from models.name import Name
from utils.decorators import input_error

@input_error('add-birthday', ['name', 'birthday'])
def add_birthday(args, address_book, **kwargs):
    name, birthday, *_ = args
    record = address_book.find(name)
    if not record:
        return f"Contact with name: {Name(name).value} does not exist."
    try:
        record.add_birthday(birthday)
        return f"Birthday added for {Name(name).value}."
    except ValueError as e:
        return str(e)
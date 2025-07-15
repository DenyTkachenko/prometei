from models.name import Name
from utils.decorators import input_error

@input_error('phone', ['name'])
def show_phone(args, address_book,  **keyword):
    name = args[0]
    record = address_book.find(name)
    if not record:
        return f"Contact with name: {Name(name).value} does not exist."
    return '; '.join(p.value for p in record.phones) if record.phones else "No phone records found."
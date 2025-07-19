from models.address_book.address_book import AddressBook
from utils.decorators import input_error

@input_error('change-note', ['promid', 'description'])
def change_note(args, address_book: AddressBook, **kwargs):
    promid, description, *_ = args
    note = address_book.find_note_by_id(promid)
    if not note:
        return f"Note with title: {note.title.value} not found"
    elif not description:
        return f"Description cannot be empty"
    note.change_description(description)
    return f"Note with title: {note.title.value} changed: {note}"

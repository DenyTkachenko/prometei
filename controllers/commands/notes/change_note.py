from models.address_book.address_book import AddressBook
from utils.decorators import input_error

@input_error('change-note', ['promid'], ['title', 'description'])
def change_note(args, address_book: AddressBook, **kwargs):

    promid, title, description, *_ = args
    note = address_book.find_note_by_id(str(promid))
    if not note:
        return f"Note with id: {promid} not found"
    elif title:
        note.change_title(title)
    elif description:
        note.change_description(description)
    return f"Note with title: {note.title.value} changed: {note}"

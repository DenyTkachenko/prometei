from models.address_book.address_book import AddressBook
from models.note.note import Note
from utils.decorators import input_error

@input_error('add-note', ['title', 'description'])
def add_note(args, address_book: AddressBook, **kwargs):
    title, description, *_ = args
    note = address_book.find_note(title)
    if note:
        return f"Note with title: {title} already exists."
    promid = address_book.manager.get_new_id("notes")
    note = Note(title, description, promid)
    address_book.add_note(note)
    return f"Note added: {note}"
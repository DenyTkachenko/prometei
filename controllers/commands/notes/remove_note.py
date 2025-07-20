from models.address_book.address_book import AddressBook
from utils.decorators import input_error

@input_error('remove-note', ['promid'])
def remove_note(args, address_book: AddressBook, **kwargs):
    promid = args[0]
    note = address_book.find_note_by_id(str(promid))
    if not note:
        return f"Note with id: {promid} not found"
    address_book.delete_note_by_id(str(promid))
    address_book.manager.delete_item("notes", str(promid))
    return f"Note with title: {note.title.value} and id {promid} deleted"
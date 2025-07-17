from utils.decorators import input_error

@input_error('remove-note', ['title'])
def remove_note(args, address_book, **kwargs):
    title, *_ = args
    note = address_book.find_note(title)
    if not note:
        return f"Note with title: {title} not found"
    address_book.delete_note(title)
    return f"Note with title: {title} deleted"
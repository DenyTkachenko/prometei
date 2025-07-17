from utils.decorators import input_error

@input_error('find-note', ['title'])
def find_note(args, address_book, **kwargs):
    title, *_ = args
    note = address_book.find_note(title)
    if note:
        return f"Note with title: {title} found: {note}"
    return f"Note with title: {title} not found"
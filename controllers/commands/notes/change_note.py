from utils.decorators import input_error

@input_error('change-note', ['title', 'description'])
def change_note(args, address_book, **kwargs):
    title, description, *_ = args
    note = address_book.find_note(title)
    if not note:
        return f"Note with title: {title} not found"
    elif not description:
        return f"Description cannot be empty"
    note.change_description(description)
    return f"Note with title: {title} changed: {note}"

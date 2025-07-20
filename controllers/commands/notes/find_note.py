from utils.decorators import input_error
from views.table import TableRenderer

@input_error('find-note', ['title'])
def find_note(args, address_book, **kwargs):
    title, *_ = args
    note = address_book.find_note(title)
    if note:
        renderer = TableRenderer()
        return renderer.render(note)
    return f"Note with title: {title} not found"
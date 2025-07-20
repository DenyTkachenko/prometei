from utils.decorators import input_error
from views.renderers import ContactTableRenderer

@input_error('find-note', ['title'])
def find_note(args, address_book, **kwargs):
    title, *_ = args
    note = address_book.find_note(title)
    if note:
        renderer = ContactTableRenderer()
        return renderer.render(note)
    return f"Note with title: {title} not found"
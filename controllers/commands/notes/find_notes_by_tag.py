from utils.decorators import input_error
from views.renderers import ContactTableRenderer

@input_error('find-notes-by-tag', ['tag'])
def find_notes_by_tag(args, address_book, **kwargs):
    tag, *_ = args
    notes = address_book.find_notes_by_tag(tag)
    if notes:
        renderer = ContactTableRenderer()
        return renderer.render(notes)
    return f"No notes found with tag: {tag}"
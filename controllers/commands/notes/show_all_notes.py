from views.renderers import ContactTableRenderer


def show_all_notes(args, address_book, **kwargs):
    notes = address_book.show_all_notes()
    renderer = ContactTableRenderer()
    return renderer.render(notes)
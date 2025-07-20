from views.table import TableRenderer


def show_all_notes(args, address_book, **kwargs):
    notes = address_book.show_all_notes()
    renderer = TableRenderer()
    return renderer.render(notes)
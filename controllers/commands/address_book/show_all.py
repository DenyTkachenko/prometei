from views.table import TableRenderer

def show_all(args, address_book, **kwargs):
    records = address_book.show_all()
    renderer = TableRenderer()
    return renderer.render(records)

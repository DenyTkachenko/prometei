from views.renderers import ContactTableRenderer

def show_all(args, address_book, **kwargs):
    records = address_book.show_all()
    renderer = ContactTableRenderer()
    return renderer.render(records)
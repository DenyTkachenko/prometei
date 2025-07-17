from views.renderers import ContactTableRenderer

def show_birthdays(args, address_book, **kwargs):
    days = args[0] if args and args[0] is not None else 7
    records = address_book.get_upcoming_birthdays(days)
    renderer = ContactTableRenderer()
    return renderer.render(records)

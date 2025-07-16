# from views.renderers import ContactTableRenderer

def find_user(args, address_book, **kwargs):
    if not args:
        return "❗ Введіть запит для пошуку. Наприклад: `find_user mariia`"

    query = " ".join(args)
    records = address_book.search(query)
    return records
    # renderer = ContactTableRenderer()
    # return renderer.render(records)
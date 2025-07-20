from views.table import TableRenderer
from utils.decorators import input_error

def find_user(args, address_book, **kwargs):
    query = " ".join(args)
    records = address_book.search(query)
    if not records:
        return "🔍 No records found"
    renderer = TableRenderer()
    return renderer.render(records)

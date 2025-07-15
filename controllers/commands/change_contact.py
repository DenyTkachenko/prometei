from models.name import Name
from utils.decorators import input_error

@input_error('change', ['name', 'old_phone', 'new_phone'])
def change_contact(args, address_book, **kwargs):
    name, old_phone, new_phone = args
    record = address_book.find(name)
    if not record:
        return f"❌ Contact with name: {Name(name).value} does not exist."
    if not record.edit_phone(old_phone, new_phone):
        return f"❌ Phone number {old_phone} not found for user {Name(name).value}."
    return f"🔁 Contact '{name}' updated with phone 📞 {new_phone}"
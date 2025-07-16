from models.record import Record
from utils.decorators import input_error

@input_error('add', ['name', 'phone'], ["birthday"])
def add_contact(args, address_book, **kwargs):
    name, phone, birthday, email, address, *_ = args
    record = address_book.find(name)
    message = f"🔁 Contact '{name}' updated with phone 📞 {phone}"
    if record is None:
        record = Record(name)
        address_book.add_record(record)
        message = f"✅ Contact '{name}' added with phone 📞 {phone}"
    record.add_phone(phone)
    if birthday:
        record.add_birthday(birthday)
        message += f" and birthday 🎂 {birthday}"
    if email:
        record.add_email(email)
        message += f" and email 📧 {email}"
    if address:
        record.set_address(address)
        message += f" and address 📫 {address}"
    return message
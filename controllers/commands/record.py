from models.address_book.address_book import AddressBook
from models.address_book.record import Record
from utils.decorators import input_error
from utils.custom_exceptions import UserNotExistException

@input_error('add', ['name'], ['phone', 'birthday', 'email', 'address'])
def add_contact(args, address_book: AddressBook, **kwargs):
    name, phone, birthday, email, address, *_ = args

    if address_book.find(name):
        return f"⚠️ Contact '{name}' already exists."

    promid = address_book.manager.get_new_id("contacts")
    record = Record(name, promid)
    address_book.add_record(record)

    # Collect parts for message
    parts = []
    if phone:
        record.add_phone(phone)
        parts.append(f"phone 📞 {phone}")
    if birthday:
        record.set_birthday(birthday)
        parts.append(f"birthday 🎂 {birthday}")
    if email:
        record.add_email(email)
        parts.append(f"email 📧 {email}")
    if address:
        record.set_address(address)
        parts.append(f"address 📫 {address}")

    # Build summary for parts
    if parts:
        details = ' and '.join(parts) if len(parts) == 1 else ', '.join(parts[:-1]) + ' and ' + parts[-1]
        return f"✅ Contact '{name}' added with {details}."
    return f"✅ Contact '{name}' added with no additional details."

@input_error("remove_contact", ["promid"])
def remove_contact(args, address_book: AddressBook, **kwargs):
    promid = str(args[0])
    record = address_book.find_record_by_id(str(promid))
    if not record:
        return UserNotExistException(user_id=str(promid))
    address_book.delete_record_by_id(str(promid))
    address_book.manager.delete_item("contacts", str(promid))
    return f"Note with title: {record.name.value} and id {promid} deleted"


@input_error('add', ['promid'], ['name','phone', 'birthday', 'email', 'address'])
def modify_contact(args, address_book: AddressBook, **kwargs):
    promid, name, phone, birthday, email, address, *_ = args
    record = address_book.find_record_by_id(str(promid))
    if not record:
        return UserNotExistException(user_id = str(promid))

    # Collect changes for message
    changes = []
    if name:
        record.name = name
        changes.append(f"name: {name}")
    if phone:
        record.add_phone(phone)
        changes.append(f"📞 phone: {phone}")
    if birthday:
        record.set_birthday(birthday)
        changes.append(f"🎂 birthday: {birthday}")
    if email:
        record.add_email(email)
        changes.append(f"📧 email: {email}")
    if address:
        record.set_address(address)
        changes.append(f"📫 address: {address}")

    if not changes:
        return f"ℹ️ No updates provided for '{record.name.value}'."

    # Build summary for changes
    if len(changes) > 1:
        changes_str = ', '.join(changes[:-1]) + ' and ' + changes[-1]
    else:
        changes_str = changes[0]

    return f"✅ Contact '{record.name.value}' updated with {changes_str}."

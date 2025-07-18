from controllers.commands.address import add_address, remove_address
from controllers.commands.address_book.show_all import show_all
from controllers.commands.exit import exit_handler
from controllers.commands.email import change_email, remove_email
from controllers.commands.notes.find_notes_by_tag import find_notes_by_tag
from controllers.commands.phone import change_phone, show_phone
from controllers.commands.record import add_contact, modify_contact
from controllers.commands.birthday import add_birthday, show_birthdays
from controllers.commands.find_user import find_user
from utils.validators import name_validator, phone_validator, birthday_validator, days_validator,email_validator, address_validator
from controllers.commands.exit import exit_handler

from controllers.commands.notes.add_note import add_note
from controllers.commands.notes.change_note import change_note
from controllers.commands.notes.find_note import find_note
from controllers.commands.notes.remove_note import remove_note
from controllers.commands.notes.show_all_notes import show_all_notes

COMMANDS = {
    "exit": {
        "handler": exit_handler,
        "args_required": {},
        "args_optional": {},
        "step_prompts": {},
        "description": "Exit and save",
    },
    "close": {
        "handler": exit_handler,
        "args_required": {},
        "args_optional": {},
        "step_prompts": {},
        "description": "Exit and save",
    },
    "add": {
        "handler": add_contact,
        "args_required": {"name": name_validator, "phone": phone_validator},
        "args_optional": {"birthday": birthday_validator, "email": email_validator, "address": address_validator},
        "step_prompts": {
            "name": "👤Enter the name of the contact: ",
            "phone": "📞Enter the phone number: ",
            "birthday": "🎂Enter the birthday (optional): ",
            "email": "📧Enter contact email (optional): ",
            "address": "📫Enter contact address (optional): ",
        },
        "description": "Add a new contact",
    },
    "modify-contact": {
        "handler": modify_contact,
        "args_required": {"name": name_validator },
        "args_optional": {"phone": phone_validator, "birthday": birthday_validator, "email": email_validator, "address": address_validator},
        "step_prompts": {
            "name": "👤Enter the name of the contact: ",
            "phone": "📞Enter additional phone number (optional): ",
            "birthday": "🎂Enter the birthday (optional): ",
            "email": "📧Enter additional contact email (optional): ",
            "address": "📫Enter contact address (optional): ",
        },
        "description": "Modify a contact by several parameters",
    },
    "all": {
        "handler": show_all,
        "args_required": {},
        "args_optional": {},
        "step_prompts": {},
        "description": "Display all contacts",
    },
    "change-phone":{
        "handler": change_phone,
        "args_required": {"name": name_validator, "old_phone": phone_validator, "new_phone": phone_validator},
        "args_optional": {},
        "step_prompts": {
            "name": "👤Enter the name of the contact: ",
            "old_phone": "📞Enter the old phone number: ",
            "new_phone": "📞Enter the new phone number: ",
        },
        "description": "Change contact phone number",
    },
    "change-email": {
        "handler": change_email,
        "args_required": {"name": name_validator, "old_email": email_validator, "new_email": email_validator},
        "args_optional": {},
        "step_prompts": {
            "name": "👤Enter the name of the contact: ",
            "old_phone": "📧Enter the old email: ",
            "new_phone": "📧Enter the new email: ",
        },
        "description": "Change contact email",
    },
    "remove-email": {
        "handler": remove_email,
        "args_required": {"name": name_validator, "old_email": email_validator},
        "args_optional": {},
        "step_prompts": {
            "name": "👤Enter the name of the contact: ",
            "old_phone": "📧Enter the contact email: ",
        },
        "description": "Remove contact email",
    },
    "add-address": {
        "handler": add_address,
        "args_required": {"name": name_validator, "address": address_validator},
        "args_optional": {},
        "step_prompts": {
            "name": "👤Enter the name of the contact: ",
            "address": "📫Enter contact address: ",
        },
        "description": "Add contact address",
    },
    "remove-address": {
        "handler": remove_address,
        "args_required": {"name": name_validator},
        "args_optional": {},
        "step_prompts": {
            "name": "👤Enter the name of the contact: ",
        },
        "description": "Remove contact address",
    },
    "add-birthday": {
        "handler": add_birthday,
        "args_required": {"name": name_validator, "birthday": birthday_validator},
        "args_optional": {},
        "step_prompts": {
            "name": "👤Enter the name of the contact: ",
            "birthday": "🎂Enter the birthday: ",
        },
        "description": "Change contact birthday",
    },
    "show_phone": {
        "handler": show_phone,
        "args_required": {"name": name_validator},
        "args_optional": {},
        "step_prompts": {
            "name": "👤Enter the name of the contact: ",
        },
        "description": "Show user phone number",
    },
    "upcoming": {
        "handler": show_birthdays,
        "args_required": {},
        "args_optional": {"days": days_validator},
        "step_prompts": {
            "days": "📅 Enter the number of days to check for upcoming birthdays (default is 7): ",
        },
        "description": "Show upcoming birthdays",
    },
    # ********************
    "add_note": {
        "handler": add_note,
        "args_required": {"title": name_validator, "description": name_validator},
        "args_optional": {},
        "step_prompts": {
            "title": "Enter the title of the note: ",
            "description": "Enter the description: ",
        },
        "description": "Add a new note",
    },
    "change_note":{
        "handler": change_note,
        "args_required": {"title": name_validator, "description": name_validator},
        "args_optional": {},
        "step_prompts": {
            "description": "Enter new description: ",
        },
        "description": "Change note description",
    },
    "find_note": {
        "handler": find_note,
        "args_required": {"title": name_validator},
        "args_optional": {},
        "step_prompts": {},
        "description": "Find note by title",
    },
    "remove_note": {
        "handler": remove_note,
        "args_required": {"title": name_validator},
        "args_optional": {},
        "step_prompts": {},
        "description": "Remove note by title",
    },
    "all_notes": {
        "handler": show_all_notes,
        "args_required": {},
        "args_optional": {},
        "step_prompts": {},
        "description": "Display all notes",
    },
    "find_user": {
        "handler": find_user,
        "args_required": {"query": str},
        "args_optional": {},
        "step_prompts": {
            "query": " 🔍Enter search query (name, phone, emails, address, birthday): "
        },
        "description": "Find user by query",
    },
    "find_notes_by_tag": {
        "handler": find_notes_by_tag,
        "args_required": {"tag": str},
        "args_optional": {},
        "step_prompts": {
            "tag": "Enter tag: "
        },
        "description": "Find notes by tag",
    }
}
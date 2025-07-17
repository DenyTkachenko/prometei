from controllers.commands.address import add_address, remove_address
from controllers.commands.exit import exit_handler
from controllers.commands.email import change_email, remove_email
from controllers.commands.phone import change_phone, show_phone
from controllers.commands.record import add_contact, modify_contact
from controllers.commands.show_all import show_all
from controllers.commands.birthday import add_birthday
from utils.validators import name_validator, phone_validator, birthday_validator, days_validator,email_validator, address_validator

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
}
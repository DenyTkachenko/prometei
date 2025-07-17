from controllers.commands.exit import exit_handler
from controllers.commands.show_all import show_all
from controllers.commands.add_contact import add_contact
from controllers.commands.add_birthday import add_birthday
from controllers.commands.change_contact import change_contact
from controllers.commands.show_phone import show_phone
from controllers.commands.show_birthdays import show_birthdays
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
    "all": {
        "handler": show_all,
        "args_required": {},
        "args_optional": {},
        "step_prompts": {},
        "description": "Display all contacts",
    },
    "change":{
        "handler": change_contact,
        "args_required": {"name": name_validator, "old_phone": phone_validator, "new_phone": phone_validator},
        "args_optional": {},
        "step_prompts": {
            "name": "👤Enter the name of the contact: ",
            "old_phone": "📞Enter the old phone number: ",
            "new_phone": "📞Enter the new phone number: ",
        },
        "description": "Change contact phone number",
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
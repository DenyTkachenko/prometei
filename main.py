from models.address_book import AddressBook
from utils.helpers import parse_input
from storage.pickle_storage import PickleStorage
from config.commands import COMMANDS
from utils.validators import validate_args, get_validators


def main():
    storage = PickleStorage[AddressBook](
        filename="addressbook.pkl",
        factory=AddressBook,
        backup=True
    )
    address_book = storage.load()
    print("Welcome to the assistant bot!")
    state = None

    while True:
        if state is None:
            user_input = input("📥 Enter a command: ").strip()
            command_name, args = parse_input(user_input)
            cmd_conf = COMMANDS.get(command_name)

            if not cmd_conf:
                print("⚠️ Invalid command.")
                continue

            required = list(cmd_conf.get("args_required", {}).keys())
            optional = list(cmd_conf.get("args_optional", {}).keys())
            arg_order = required + optional
            validators = get_validators(cmd_conf)

            validated_args = validate_args(args, arg_order, validators)
            if validated_args is None:
                continue  # restart input loop on validation failure

            state = {
                "command": command_name,
                "args": validated_args,
            }

        cmd_conf = COMMANDS[state["command"]]
        required = list(cmd_conf.get("args_required", {}).keys())
        optional = list(cmd_conf.get("args_optional", {}).keys())
        arg_order = required + optional
        validators = get_validators(cmd_conf)

        # Collect missing arguments step-by-step
        missing_args = [arg for arg in arg_order if arg not in state["args"]]

        if not missing_args:
            # All arguments collected, call handler
            ordered_args = [state["args"].get(arg) for arg in arg_order]
            result = cmd_conf["handler"](ordered_args, address_book, storage)
            print(f"✅ {result}")
            state = None
            continue

        next_arg = missing_args[0]
        prompt = cmd_conf["step_prompts"].get(next_arg, f"Enter {next_arg}: ")
        answer = input(prompt).strip()

        if not answer and next_arg in optional:
            state["args"][next_arg] = None
            continue

        validator = validators.get(next_arg)
        if validator:
            try:
                state["args"][next_arg] = validator(answer)
            except ValueError as e:
                print(f"❌ Error in '{next_arg}': {e}")
        else:
            state["args"][next_arg] = answer

if __name__ == "__main__":
    main()

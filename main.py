# main.py

from storage.pickle_storage import PickleStorage
from models.address_book      import AddressBook
from views.cli_interface      import CLIInterface
from controllers.core         import CommandContext, CommandProcessor, ProcessorResult


def create_context() -> CommandContext:
    """
    Initialize storage and load the address book.
    Returns a CommandContext holding shared state.
    """
    storage      = PickleStorage("addressbook.pkl", factory=AddressBook, backup=True)
    address_book = storage.load()
    return CommandContext(storage=storage, address_book=address_book)


def main() -> None:
    """
    Entry point for the CLI.
    Runs a loop, prompting for commands or arguments, and dispatching them to the processor.
    """
    context   = create_context()
    interface = CLIInterface()
    processor = CommandProcessor(context)

    # First prompt: ask for a command
    result = ProcessorResult("📥 Enter a command (type 'help'): ", expect_input=True)

    # Main loop: continue until a handler sets context.running = False
    while context.running:
        if result.expect_input:
            # If processor asked for input, use that as our prompt
            user_text = interface.receive_message(user_id=0, prompt=result.text)
        else:
            # Otherwise, display the result and then re‑prompt for a new command
            if result.text:
                interface.send_message(user_id=0, text=result.text)
            user_text = interface.receive_message(
                user_id=0,
                prompt="📥 Enter a command (type 'help'): "
            )

        # Feed the user’s text back into the processor
        result = processor.process_message(user_id=0, message=user_text)


if __name__ == "__main__":
    main()

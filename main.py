from storage.pickle_storage                import PickleStorage
from models.address_book.address_book      import AddressBook
from controllers.core                      import CommandContext, CommandProcessor
from views.cli_interface                   import CLIInterface, BaseInterface
from controllers.telegram.telegram_wrapper import TelegramBot
from config.general                        import MODE, TG_TOKEN


def create_context() -> CommandContext:
    storage      = PickleStorage("addressbook.pkl", factory=AddressBook, backup=True)
    address_book = storage.load()
    return CommandContext(storage=storage, address_book=address_book)


def run_loop(interface: BaseInterface, initial_prompt: str) -> None:
    context   = create_context()
    processor = CommandProcessor(context)

    # Start with the initial prompt
    prompt = initial_prompt

    while context.running:
        # 1) Receive from interface (CLI display prompt, Telegram ignore)
        user_id, text = interface.receive_message(prompt=prompt)

        # 2) Process
        result = processor.process_message(user_id, text)

        if result.expect_input:
            # multi‑step mode
            prompt = result.text or ""
            continue

        # one-step mode
        if result.text:
            interface.send_message(user_id, result.text)

        prompt = initial_prompt


def cli_main() -> None:
    """Run the assistant in command‑line mode."""
    default_prompt = "📥 Enter a command (type 'help'): "
    run_loop(CLIInterface(), default_prompt)


def telegram_main(token: str) -> None:

    context   = create_context()
    processor = CommandProcessor(context)
    bot       = TelegramBot(token, processor)
    bot.run_polling()


if __name__ == "__main__":
    if MODE == "telegram":
        if not TG_TOKEN:
            raise RuntimeError("TG_TOKEN is not set")
        telegram_main(TG_TOKEN)
    else:
        cli_main()
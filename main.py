import config.commands
from storage.pickle_storage                import PickleStorage
from models.address_book.address_book      import AddressBook
from controllers.core                      import CommandContext, CommandProcessor
from views.cli_interface                   import CLIInterface, BaseInterface
from controllers.telegram.telegram_wrapper import TelegramBot
from config.general                        import MODE, TG_TOKEN
from views.completer.prompt_session import get_prompt_session


def create_context() -> CommandContext:
    storage      = PickleStorage("addressbook.pkl", factory=AddressBook, backup=True)
    address_book = storage.load()
    return CommandContext(storage=storage, address_book=address_book)


def run_loop(interface: BaseInterface, initial_prompt: str) -> None:
    context   = create_context()
    processor = CommandProcessor(context)

    # Start with the initial prompt
    prompt = initial_prompt

    try:
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

    except Exception:
        # Emergency saving
        try:
            context.storage.save(context.address_book)
            print('❗An unexpected error occurred, the data has been saved.')
        except Exception as save_err:
            print(f"❗Error when saving data: {save_err}")
        raise

def cli_main() -> None:
    """Run the assistant in command‑line mode."""
    default_prompt = "📥 Enter a command (type 'help'): "
    run_loop(CLIInterface(get_prompt_session(list(config.commands.COMMANDS.keys()))), default_prompt)


def telegram_main(token: str) -> None:

    context   = create_context()
    processor = CommandProcessor(context)
    bot       = TelegramBot(token, processor)

    try:
        bot.run_polling()
    except Exception:
        print('❗An unexpected error occurred, the data has been saved.')
        context.storage.save(context.address_book)
        raise

if __name__ == "__main__":
    if MODE == "telegram":
        if not TG_TOKEN:
            raise RuntimeError("TG_TOKEN is not set")
        telegram_main(TG_TOKEN)
    else:
        cli_main()
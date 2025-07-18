from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

from controllers.core import CommandProcessor
from config.commands import COMMANDS


class TelegramBot:
    """
    Telegram bot using custom keyboards to guide multi-step commands.
    Supports 'Back', 'Finish', and quick field selection.
    """

    def __init__(self, token: str, processor: CommandProcessor):
        self.processor = processor
        self.initial_prompt = "📥 Enter a command (type 'help'): "

        # Create application and register handlers
        self.app = ApplicationBuilder().token(token).build()
        self.app.add_handler(CommandHandler("start", self._handle_start))
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message)
        )

    def _main_keyboard(self) -> ReplyKeyboardMarkup:
        """Build keyboard with all top-level commands."""
        buttons = [KeyboardButton(cmd) for cmd in COMMANDS]
        # arrange in rows of 3
        rows = [buttons[i:i+3] for i in range(0, len(buttons), 3)]
        return ReplyKeyboardMarkup(rows, one_time_keyboard=True, resize_keyboard=True)

    def _optional_keyboard(self, cmd_name: str) -> ReplyKeyboardMarkup:
        """Build keyboard for optional args plus Back and Finish."""
        opts = list(COMMANDS[cmd_name]["args_optional"].keys())
        controls = ["Back", "Finish"]
        buttons = [KeyboardButton(opt) for opt in opts + controls]
        rows = [buttons[i:i+3] for i in range(0, len(buttons), 3)]
        return ReplyKeyboardMarkup(rows, one_time_keyboard=True, resize_keyboard=True)

    async def _handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send initial prompt and main keyboard on /start."""
        user_id = str(update.effective_user.id)
        self.processor.cleanup_session(user_id)
        await update.message.reply_text(
            self.initial_prompt,
            reply_markup=self._main_keyboard()
        )

    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process user text input with CommandProcessor and manage keyboards."""
        user_id = str(update.effective_user.id)
        text = update.message.text or ""
        session = self.processor.sessions.get(user_id)

        # Handle Back command
        if text == "Back" and session and session.command:
            result = self.processor.process_message(user_id, "back")
            await update.message.reply_text(result.text or "")
            return

        # Handle Finish command
        if text == "Finish" and session and session.command:
            result = self.processor.process_message(user_id, "finish")
            # send command result
            if result.text:
                await update.message.reply_text(result.text)
            # back to main
            await update.message.reply_text(
                self.initial_prompt,
                reply_markup=self._main_keyboard()
            )
            return

        # Quick jump to optional field via button text
        if session and session.command:
            optional = list(COMMANDS[session.command]["args_optional"].keys())
            if text in optional:
                # send as --field to processor
                result = self.processor.process_message(user_id, f"--{text}")
                if result.text:
                    await update.message.reply_text(result.text)
                return

        # Normal processing
        result = self.processor.process_message(user_id, text)

        # If expecting input and required are filled, show optional keyboard
        if result.expect_input:
            session = self.processor.sessions.get(user_id)
            if session and session.command:
                cmd_name = session.command
                required = set(COMMANDS[cmd_name]["args_required"].keys())
                filled = set(session.args.keys())

                if required.issubset(filled) and COMMANDS[cmd_name]["args_optional"] and result.text in session.prompts.values():
                    await update.message.reply_text(
                        "✅ Required fields done. Choose optional or Finish.",
                        reply_markup=self._optional_keyboard(cmd_name)
                    )
                    return
            # prompt next argument
            if result.text:
                await update.message.reply_text(result.text)
            return

        # Command completed: send result and show main keyboard
        if result.text:
            await update.message.reply_text(result.text)
        await update.message.reply_text(
            self.initial_prompt,
            reply_markup=self._main_keyboard()
        )

    def run_polling(self) -> None:
        """Start long polling for the bot (blocking call)."""
        self.app.run_polling()

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from controllers.telegram.keyboards import KeyboardFactory
from controllers.core import CommandProcessor
from config.commands import COMMANDS
from config.general import StreamControlCmd

class TelegramBot:
    """
    Telegram bot using custom keyboards to guide multi-step commands.
    """

    def __init__(self, token: str, processor: CommandProcessor) -> None:
        self.token = token
        self.processor = processor
        self.initial_prompt = "📥 Enter a command (type 'help'):"

        self.app = self._create_application()
        self._register_handlers()

    def _create_application(self) -> Application:
        return Application.builder().token(self.token).build()

    def _register_handlers(self) -> None:
        self.app.add_handler(CommandHandler("start", self._on_start))
        text_filter = filters.TEXT & ~filters.COMMAND
        self.app.add_handler(MessageHandler(text_filter, self._on_message))

    async def _on_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_id = self._user_id(update)
        self.processor.cleanup_session(user_id)
        await update.message.reply_text(
            self.initial_prompt,
            reply_markup=KeyboardFactory.main(),
        )

    async def _on_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_id = self._user_id(update)
        text = update.message.text or ""

        session = self.processor.sessions.get(user_id)
        # Delegate back/finish if in-progress
        if self._is_control(text, session):
            await self._handle_control(text, update)
            return

        # Quick-select optional argument
        if session and session.command and self._is_optional_field(text, session.command):
            await self._handle_optional_jump(text, user_id, update)
            return

        # Normal processing
        result = self.processor.process_message(user_id, text)
        await self._dispatch_result(result, user_id, update)

    async def _handle_control(self, text: str, update: Update) -> None:
        user_id = self._user_id(update)
        cmd = "back" if text == StreamControlCmd.BACK.value else "finish"
        result = self.processor.process_message(user_id, cmd)

        if cmd == "finish":
            if result.text:
                await update.message.reply_text(result.text)
            await update.message.reply_text(
                self.initial_prompt,
                reply_markup=KeyboardFactory.main(),
            )
        else:
            if result.text:
                await update.message.reply_text(result.text)

    async def _handle_optional_jump(
        self, text: str, user_id: str, update: Update
    ) -> None:
        result = self.processor.process_message(user_id, f"--{text}")
        if result.text:
            await update.message.reply_text(result.text)

    async def _dispatch_result(
        self, result, user_id: str, update: Update
    ) -> None:
        # If awaiting more input
        if result.expect_input:
            await self._prompt_for_next(result, user_id, update)
        else:
            # Completed command
            if result.text:
                await update.message.reply_text(result.text)
            await update.message.reply_text(
                self.initial_prompt,
                reply_markup=KeyboardFactory.main(),
            )

    async def _prompt_for_next(
        self, result, user_id: str, update: Update
    ) -> None:
        # Retrieve session and command definition
        session = self.processor.sessions.get(user_id)
        if not session or not session.command:
            return

        cmd_def = COMMANDS[session.command]
        required = set(cmd_def["args_required"].keys())
        filled = set(session.args.keys())
        optional_fields = list(cmd_def["args_optional"].keys())
        optional_exists = bool(optional_fields)

        last_prompt = result.text or ""
        # Determine prompts for optional args
        optional_prompts = [session.prompts.get(arg) for arg in optional_fields if arg in session.prompts]

        # Show optional keyboard only when required are filled and last prompt was the optional field prompt
        if required.issubset(filled) and optional_exists and last_prompt in optional_prompts:
            await update.message.reply_text(
                "✅ Required fields completed. Choose optional or Finish.",
                reply_markup=KeyboardFactory.optional(session.command),
            )
            return

        # Otherwise, display prompt or validation error
        if result.text:
            await update.message.reply_text(result.text)

    def _is_control(self, text: str, session) -> bool:
        return bool(session and session.command and text in (StreamControlCmd.BACK.value, StreamControlCmd.FINISH.value))

    def _is_optional_field(self, text: str, command: str) -> bool:
        return text in COMMANDS[command]["args_optional"]

    @staticmethod
    def _user_id(update: Update) -> str:
        return str(update.effective_user.id)

    def run_polling(self) -> None:
        """Start the bot with polling."""
        self.app.run_polling()

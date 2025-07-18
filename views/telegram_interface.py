from typing import Any, List
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)
from controllers.core import CommandProcessor
from config.commands import COMMANDS


class TelegramBot:
    def __init__(self, token: str, processor: CommandProcessor):
        self.processor = processor
        self.initial_prompt = "📥 Enter a command (type 'help'): "

        # List of command for  keyboard
        self._build_keyboard()

        self.app = ApplicationBuilder().token(token).build()

        # /start display initial_prompt + keyboard
        self.app.add_handler(CommandHandler("start", self._on_start))

        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._on_message)
        )

    def _build_keyboard(self) -> None:
        """
        Builds self.keyboard as a list of KeyboardButton lists,
        with 3 buttons per row.
        """
        cmds: List[str] = list(COMMANDS.keys())
        rows: List[List[KeyboardButton]] = []
        row: List[KeyboardButton] = []

        for name in cmds:
            row.append(KeyboardButton(name))
            if len(row) == 3:
                rows.append(row)
                row = []
        if row:
            rows.append(row)

        self.keyboard = ReplyKeyboardMarkup(
            rows,
            one_time_keyboard=True,
            resize_keyboard=True
        )

    async def _on_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            self.initial_prompt,
            reply_markup=self.keyboard
        )

    async def _on_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        On any message:
        - if multi-step input (expect_input=True) - send prompt without keyboard;
        - otherwise - send result + initial_prompt with keyboard.
        """
        user_id = str(update.effective_user.id)
        text    = update.message.text or ""

        result = self.processor.process_message(user_id, text)

        if result.expect_input:
            # Multi-step input: only the text of the next step
            if result.text:
                await update.message.reply_text(result.text)
        else:
            # End of command: result + repeat initial prompt with keyboard
            if result.text:
                await update.message.reply_text(result.text)
            await update.message.reply_text(
                self.initial_prompt,
                reply_markup=self.keyboard
            )

    def run_polling(self) -> None:
        self.app.run_polling()

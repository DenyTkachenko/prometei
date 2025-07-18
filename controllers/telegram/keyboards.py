from typing import List

from telegram import ReplyKeyboardMarkup, KeyboardButton
from config.commands import COMMANDS
from config.general import StreamControlCmd

class KeyboardFactory:
    """
    Factory for generating reply keyboards for the bot.
    """

    @staticmethod
    def build_layout(buttons: List[str], row_size: int = 3) -> List[List[KeyboardButton]]:
        return [
            [KeyboardButton(text=btn) for btn in buttons[i : i + row_size]]
            for i in range(0, len(buttons), row_size)
        ]

    @classmethod
    def main(cls) -> ReplyKeyboardMarkup:
        labels = list(COMMANDS.keys())
        layout = cls.build_layout(labels)
        return ReplyKeyboardMarkup(layout, one_time_keyboard=True, resize_keyboard=True)

    @classmethod
    def optional(cls, command_name: str) -> ReplyKeyboardMarkup:
        opts = list(COMMANDS[command_name]["args_optional"].keys())
        layout = cls.build_layout(opts + [StreamControlCmd.BACK.value, StreamControlCmd.FINISH.value])
        return ReplyKeyboardMarkup(layout, one_time_keyboard=True, resize_keyboard=True)
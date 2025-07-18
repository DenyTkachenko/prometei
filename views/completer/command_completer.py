from typing import Iterable

from prompt_toolkit.completion import Completer, CompleteEvent, Completion
from prompt_toolkit.document import Document


class CommandCompleter(Completer):


    def __init__(self, commands: list[str]):
        self.commands = commands

    def get_completions(self, document: Document, complete_event: CompleteEvent) -> Iterable[Completion]:
        word = document.get_word_before_cursor().lower()

        for cmd in self.commands:
            if cmd.startswith(word):
                yield Completion(cmd, start_position=-len(word))

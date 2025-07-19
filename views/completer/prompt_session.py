from prompt_toolkit import PromptSession

from views.completer.command_completer import CommandCompleter


def get_prompt_session(commands: list[str]) -> PromptSession:
    return PromptSession(
        completer=CommandCompleter(commands),
        complete_while_typing=True
    )
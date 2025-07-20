from prompt_toolkit import PromptSession

from views.completer.command_completer import CommandCompleter


def get_prompt_session(commands: list[str]) -> PromptSession:
    prompt_session = None
    try:
        prompt_session = PromptSession(
            completer=CommandCompleter(commands),
            complete_while_typing=True
        )
    except Exception as ex:
        print(str(ex))

    return prompt_session
from prompt_toolkit import PromptSession

from views.completer.command_completer import CommandCompleter

"""
Функція get_prompt_session приймає список комманд
та повертає об'єкт типу PromptSession

Аргументи:
commands: list[str] - список комманд, що повинні підказуватися користувачу

return: PromptSession - об'єкт типу PromptSession
"""

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
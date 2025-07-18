from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
import threading

from config.commands import COMMANDS
from utils.helpers import parse_input
from utils.validators import validate_args, get_validators


@dataclass
class ProcessorResult:
    """
    Represents the result of processing a user message.

    Attributes:
        text: The response text or prompt for the next input.
        expect_input: If True, next input is taken without redisplaying the main prompt.
    """
    text: Optional[str] = None
    expect_input: bool = False


class CommandSession:
    """
    Stores the state of a multi-step command for a single user.
    """
    def __init__(self):
        # Active command name
        self.command: Optional[str] = None
        # List of all expected arguments (required + optional)
        self.arg_order: List[str] = []
        # Validator functions for each argument
        self.validators: Dict[str, Any] = {}
        # Step-by-step prompts for each argument
        self.prompts: Dict[str, str] = {}
        # Collected argument values
        self.args: Dict[str, Any] = {}
        # Name of the next field selected via "--field"
        self.next_field: Optional[str] = None


class CommandContext:
    """
    Shared context: storage, address book, running flag.
    """
    def __init__(self, storage: Any, address_book: Any):
        self.storage = storage
        self.address_book = address_book
        # Set to False to stop loops and shutdown
        self.running: bool = True


class CommandProcessor:
    """
    Processes text messages into commands with multi-step flows.

    Sessions are stored per user_id and protected by a reentrant lock.
    """

    def __init__(self, context: CommandContext):
        self.context = context
        self.sessions: Dict[Any, CommandSession] = {}
        self.lock = threading.RLock()

    def cleanup_session(self, user_id: Any) -> None:
        """Remove the user's session, if it exists."""
        with self.lock:
            self.sessions.pop(user_id, None)

    def _optional_args(self, cmd_name: str) -> List[str]:
        """Return a list of optional argument names for the command."""
        return list(COMMANDS[cmd_name]["args_optional"].keys())

    def process_message(self, user_id: Any, message: str) -> ProcessorResult:
        """
        Main entry: process incoming text, return a ProcessorResult.
        Always returns a ProcessorResult; never returns None.
        """
        text = message.strip()

        with self.lock:
            session = self.sessions.get(user_id)
            if session is None:
                session = CommandSession()
                self.sessions[user_id] = session

        # If no command active and no text, do nothing
        if session.command is None and not text:
            return ProcessorResult(text="", expect_input=False)

        # Handle 'back' in multi-step flow
        if session.command and text.lower() == "back":
            provided = [a for a in session.arg_order if a in session.args]
            if not provided:
                self.cleanup_session(user_id)
                return ProcessorResult(text=None, expect_input=False)
            last = provided[-1]
            session.args.pop(last, None)
            session.next_field = None
            prompt = session.prompts.get(last, f"Enter {last}: ")
            return ProcessorResult(text=f"⬅️ Going back.\n{prompt}", expect_input=True)

        # Handle 'start' to cancel flow
        if session.command and text.lower() == "start":
            self.cleanup_session(user_id)
            return ProcessorResult(text=None, expect_input=False)

        if session.command and text.lower() == "finish":
            cmd_conf = COMMANDS[session.command]
            required = set(cmd_conf["args_required"].keys())
            # If all required fields are filled, run the handler
            if required.issubset(session.args.keys()):
                handler = cmd_conf["handler"]
                values = [session.args.get(arg) for arg in session.arg_order]
                print('call handler')
                result_text = handler(values,
                                      self.context.address_book,
                                      storage=self.context.storage)
                self.cleanup_session(user_id)
                return ProcessorResult(text=result_text, expect_input=False)
            # Otherwise, prompt for the next missing required field
            missing = [arg for arg in cmd_conf["args_required"].keys()
                       if arg not in session.args]
            print('missing missing argu')
            next_arg = missing[0]
            prompt = session.prompts.get(next_arg, f"Enter {next_arg}: ")
            return ProcessorResult(
                text=f"❌ Required fields missing. {prompt}",
                expect_input=True
            )

        # Quick switch to an optional field: --field
        if session.command and text.startswith("--"):
            field = text[2:]
            if field in self._optional_args(session.command) and field not in session.args:
                session.next_field = field
                prompt = session.prompts.get(field, f"Enter {field}: ")
                return ProcessorResult(text=prompt, expect_input=True)
            return ProcessorResult(text=f"❌ Unknown argument '{field}'.", expect_input=True)

        # Multi-step argument collection
        if session.command:
            # Determine which field to fill next
            if session.next_field:
                current = session.next_field
                session.next_field = None
            else:
                # First missing in order
                current = next(arg for arg in session.arg_order if arg not in session.args)

            # Allow blank for optional
            if text == "" and current in self._optional_args(session.command):
                session.args[current] = None
            else:
                validator = session.validators.get(current)
                try:
                    session.args[current] = validator(text) if validator else text
                except Exception as err:
                    prompt = session.prompts.get(current, f"Enter {current}: ")
                    return ProcessorResult(
                        text=f"❌ Error in '{current}': {err}\n{prompt}",
                        expect_input=True,
                    )

            # Check for remaining args
            remaining = [a for a in session.arg_order if a not in session.args]
            if remaining:
                next_arg = remaining[0]
                prompt = session.prompts.get(next_arg, f"Enter {next_arg}: ")
                return ProcessorResult(text=prompt, expect_input=True)

            # All args collected: execute handler
            cmd_conf = COMMANDS[session.command]
            handler = cmd_conf["handler"]
            values = [session.args[arg] for arg in session.arg_order]
            result_text = handler(values, self.context.address_book, storage=self.context.storage)
            self.cleanup_session(user_id)
            return ProcessorResult(text=result_text, expect_input=False)

        # No active session: parse new command
        # parse_input returns (command_name, raw_args list)
        name, raw_args = parse_input(text)
        cmd_conf = COMMANDS.get(name)
        if not cmd_conf:
            return ProcessorResult(text=f"❌ Unknown command '{name}'.", expect_input=False)

        # Prepare args
        required = list(cmd_conf["args_required"].keys())
        optional = list(cmd_conf["args_optional"].keys())
        order = required + optional
        validators = get_validators(cmd_conf)

        # Validate inline args
        validated = validate_args(raw_args, order, validators)
        if validated is None:
            return ProcessorResult(text=None, expect_input=False)

        # If all args present, call handler immediately
        if len(validated) == len(order):
            values = [validated[arg] for arg in order]
            result_text = cmd_conf["handler"](values, self.context.address_book, storage=self.context.storage)
            return ProcessorResult(text=result_text, expect_input=False)

        # Enter multi-step flow
        session.command = name
        session.arg_order = order
        session.validators = validators
        session.prompts = cmd_conf.get("step_prompts", {})
        session.args = validated
        session.next_field = None

        # Prompt first missing argument
        missing = [a for a in order if a not in validated]
        first = missing[0]
        prompt = session.prompts.get(first, f"Enter {first}: ")
        return ProcessorResult(text=prompt, expect_input=True)

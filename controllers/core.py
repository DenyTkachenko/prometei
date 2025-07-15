# controllers/core.py

from typing      import Any, Dict, List, Optional
from dataclasses import dataclass

from config.commands   import COMMANDS
from utils.helpers     import parse_input
from utils.validators  import validate_args, get_validators


@dataclass
class ProcessorResult:
    """
    text: what to send or prompt the user
    expect_input: if True, call receive_message immediately with this text as prompt
    """
    text: str
    expect_input: bool = False


class CommandSession:
    """Tracks multi‑step command state for one user."""
    def __init__(self):
        self.command:    Optional[str]    = None
        self.arg_order:  List[str]        = []
        self.validators: Dict[str,Any]    = {}
        self.prompts:    Dict[str,str]    = {}
        self.args:       Dict[str,Any]    = {}


class CommandContext:
    """Holds shared state: storage, address_book, running flag."""
    def __init__(self, storage, address_book):
        self.storage      = storage
        self.address_book = address_book
        self.running      = True


class CommandProcessor:
    def __init__(self, context: CommandContext):
        self.context  = context
        self.sessions: Dict[Any, CommandSession] = {}

    def process_message(self, user_id: Any, message: str) -> ProcessorResult:
        session = self.sessions.setdefault(user_id, CommandSession())
        text = message.strip()

        # === Multi‑step argument collection ===
        if session.command:
            # find next arg to collect
            for name in session.arg_order:
                if name not in session.args:
                    current = name
                    break

            # if optional & blank → assign None
            if text == "" and current in self._optional_args(session.command):
                session.args[current] = None
            else:
                # validate and store
                validator = session.validators.get(current)
                try:
                    session.args[current] = validator(text) if validator else text
                except Exception as e:
                    # prompt error + same step prompt again
                    prompt = session.prompts.get(current, f"Enter {current}: ")
                    error_msg = f"❌ Error '{current}': {e}\n{prompt}"
                    return ProcessorResult(error_msg, expect_input=True)

            # check if anything left to ask
            missing = [a for a in session.arg_order if a not in session.args]
            if missing:
                nxt = missing[0]
                prompt = session.prompts.get(nxt, f"Enter {nxt}: ")
                return ProcessorResult(prompt, expect_input=True)

            # all args collected → execute handler
            ordered_args = [session.args.get(a) for a in session.arg_order]
            cmd_conf = COMMANDS[session.command]
            handler  = cmd_conf["handler"]
            # pass storage as keyword so **kwargs picks it up
            result   = handler(ordered_args,
                               self.context.address_book,
                               storage=self.context.storage)

            # cleanup and return
            del self.sessions[user_id]
            return ProcessorResult(result, expect_input=False)

        # === New command start ===
        if not text:
            return ProcessorResult(
                "📥 Enter a command (type 'help' for list of commands): ",
                expect_input=True
            )

        # parse command + inline args
        name, raw_args = parse_input(text)
        cmd_conf = COMMANDS.get(name)
        if not cmd_conf:
            return ProcessorResult(f"❌ Unknown command '{name}'.", expect_input=False)

        # prepare arg lists
        required   = list(cmd_conf["args_required"].keys())
        optional   = list(cmd_conf["args_optional"].keys())
        order      = required + optional
        validators = get_validators(cmd_conf)

        # bulk validation of inline args
        validated = validate_args(raw_args, order, validators)
        if validated is None:
            # validator already printed error — restart command entry
            return ProcessorResult(
                "📥 Enter a command (type 'help' for list of commands): ",
                expect_input=True
            )

        # if user provided ALL args at once → execute immediately
        if len(validated) == len(order):
            ordered_args = [validated.get(a) for a in order]
            result = cmd_conf["handler"](ordered_args,
                                         self.context.address_book,
                                         storage=self.context.storage)
            return ProcessorResult(result, expect_input=False)

        # else — enter multi‑step mode
        session.command    = name
        session.arg_order  = order
        session.validators = validators
        session.prompts    = cmd_conf.get("step_prompts", {})
        session.args       = validated

        # ask for first missing arg (including optional!)
        next_arg = order[len(validated)]
        prompt   = session.prompts.get(next_arg, f"Enter {next_arg}: ")
        return ProcessorResult(prompt, expect_input=True)

    def _optional_args(self, command_name: str) -> List[str]:
        """Return optional args names for this command."""
        return list(COMMANDS[command_name]["args_optional"].keys())

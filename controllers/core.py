from typing      import Any, Dict, List, Optional
from dataclasses import dataclass

from config.commands   import COMMANDS
from utils.helpers     import parse_input
from utils.validators  import validate_args, get_validators


@dataclass
class ProcessorResult:
    """
    text: what to send or prompt the user
    expect_input: if True, interface should immediately call receive_message(text)
    """
    text: Optional[str] = None
    expect_input: bool = False


class CommandSession:
    """Tracks one user’s in‑progress multi‑step command."""
    def __init__(self):
        # name of the current command
        self.command:    Optional[str] = None
        # ordered list of argument names
        self.arg_order:  List[str]     = []
        # per-argument validator functions
        self.validators: Dict[str,Any] = {}
        # per-argument step prompts
        self.prompts:    Dict[str,str] = {}
        # collected argument values
        self.args:       Dict[str,Any] = {}


class CommandContext:
    """Global state shared by all handlers."""
    def __init__(self, storage, address_book):
        self.storage      = storage
        self.address_book = address_book
        # flag to stop the main loop when exit
        self.running      = True


class CommandProcessor:
    """
    Core processor, fully decoupled from any frontend.
    Sessions keyed by user_id for per‑user multi‑step flows.
    """
    def __init__(self, context: CommandContext):
        self.context  = context
        self.sessions: Dict[Any, CommandSession] = {}

    def process_message(self, user_id: Any, message: str) -> ProcessorResult:
        session = self.sessions.setdefault(user_id, CommandSession())
        text = message.strip()

        # --- Multi‑step argument collection ---
        if session.command:
            # 1) find next argument name to collect
            for name in session.arg_order:
                if name not in session.args:
                    current = name
                    break

            # 2) if optional & blank → assign None
            if text == "" and current in self._optional_args(session.command):
                session.args[current] = None
            else:
                # 3) validate and store
                validator = session.validators.get(current)
                try:
                    session.args[current] = validator(text) if validator else text
                except Exception as e:
                    # on validation error, re‑prompt the same step
                    prompt = session.prompts.get(current, f"Enter {current}: ")
                    return ProcessorResult(f"❌ Error '{current}': {e}\n{prompt}",
                                           expect_input=True)

            # 4) check if more args remain
            missing = [a for a in session.arg_order if a not in session.args]
            if missing:
                nxt = missing[0]
                prompt = session.prompts.get(nxt, f"Enter {nxt}: ")
                return ProcessorResult(prompt, expect_input=True)

            # 5) all collected → call handler
            ordered_args = [session.args[a] for a in session.arg_order]
            cmd_conf = COMMANDS[session.command]
            handler  = cmd_conf["handler"]
            # pass storage as keyword only
            result   = handler(ordered_args,
                               self.context.address_book,
                               storage=self.context.storage)

            # cleanup session
            del self.sessions[user_id]
            return ProcessorResult(result, expect_input=False)

        # Empty enter
        if not text:
            return ProcessorResult("",expect_input=False)

        # parse command name and any inline args
        name, raw_args = parse_input(text)
        cmd_conf = COMMANDS.get(name)
        if not cmd_conf:
            return ProcessorResult(f"❌ Unknown command '{name}'.", expect_input=False)

        # prepare lists of arg names and validators
        required   = list(cmd_conf["args_required"].keys())
        optional   = list(cmd_conf["args_optional"].keys())
        order      = required + optional
        validators = get_validators(cmd_conf)

        # bulk‑validate any inline args
        validated = validate_args(raw_args, order, validators)
        if validated is None:
            # validation error already printed; restart command entry
            return ProcessorResult(expect_input=False)

        # if user provided all args at once → call handler immediately
        if len(validated) == len(order):
            ordered_args = [validated[a] for a in order]
            result = cmd_conf["handler"](ordered_args,
                                         self.context.address_book,
                                         storage=self.context.storage)
            return ProcessorResult(result, expect_input=False)

        # else → enter multi‑step mode
        session.command    = name
        session.arg_order  = order
        session.validators = validators
        session.prompts    = cmd_conf.get("step_prompts", {})
        session.args       = validated

        # ask for the first missing argument
        next_arg = order[len(validated)]
        prompt   = session.prompts.get(next_arg, f"Enter {next_arg}: ")
        return ProcessorResult(prompt, expect_input=True)

    def _optional_args(self, command_name: str) -> List[str]:
        """Return the list of optional arg names for a command."""
        return list(COMMANDS[command_name]["args_optional"].keys())

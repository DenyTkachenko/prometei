from typing import Dict, Any, Optional

class CommandSession:
    def __init__(self):
        self.command: Optional[str] = None
        self.args: Dict[str, Any] = {}
        self.arg_order: list[str] = []
        self.current_arg: Optional[str] = None
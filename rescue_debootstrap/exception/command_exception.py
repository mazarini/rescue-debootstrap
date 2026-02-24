# exception/command_exception.py


class CommandException(Exception):
    """Exception levée lorsqu'une commande échoue."""

    def __init__(self, command: str, returncode: int):
        self.command = command
        self.returncode = returncode
        super().__init__(f"Command failed ({returncode}): {command}")

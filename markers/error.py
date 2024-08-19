import sys
from contextlib import contextmanager
from typing import Generator

from markers.tokens import PositionInfo


class UserError(Exception):
    """Error resulting from user input."""

    pos: PositionInfo

    def __init__(self, message: str, pos: PositionInfo):
        """Initialize a UserError.

        Args:
            message (str): The error message.
            pos (PositionInfo): The position information of the error.
        """
        self.message = message
        self.pos = pos
        super().__init__(message)


class ParseError(UserError):
    """Error resulting from a failure to parse the program successfully."""

    def __init__(self, message: str, pos: PositionInfo):
        """Initialize a ParseError.

        Args:
            message (str): The error message.
            pos (PositionInfo): The position information of the error.
        """
        self.message = message
        super().__init__(message, pos)


class EvaluateError(UserError):
    """Error resulting from a failure to evaluate the program successfully."""

    def __init__(self, message: str, pos: PositionInfo):
        """Initialize a EvaluateError.

        Args:
            message (str): The error message.
            pos (PositionInfo): The position information of the error.
        """
        self.message = message
        super().__init__(message, pos)


class InternalError(Exception):
    """Error resulting from an internal failure."""

    def __init__(self, message: str):
        """Initialize a InternalError.

        Args:
            message (str): The error message.
        """
        self.message = message
        super().__init__(message)


@contextmanager
def error_context(program: str) -> Generator[None, None, None]:
    """Context manager to handle errors."""
    lines = program.split("\n")

    try:
        yield
    except UserError as exc:
        line_no = exc.pos.line_no
        char_no = exc.pos.char_no
        length = exc.pos.length

        error_message = f"{type(exc).__name__}: {exc.message}"
        print(error_message, file=sys.stderr)
        print(f"line {line_no}, col {char_no}", file=sys.stderr)

        if line_no > 0:
            print()
            program_line = lines[line_no - 1]
            print(program_line, file=sys.stderr)

            carets = "-" * (char_no - 1) + "^" * length
            print(carets, file=sys.stderr)

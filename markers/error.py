import sys
from contextlib import contextmanager
from typing import Generator

from markers.type import PosInfo


class UserError(Exception):
    """Error resulting from user input."""

    pos_info: PosInfo

    def __init__(self, message: str, pos_info: PosInfo):
        """Initialize a UserError.

        Args:
            message (str): The error message.
            pos_info (PosInfo): The position information of the error.
        """
        self.message = message
        self.pos_info = pos_info
        super().__init__(message)


class ParseError(UserError):
    """Error resulting from a failure to parse the program successfully."""

    def __init__(self, message: str, pos_info: PosInfo):
        """Initialize a ParseError.

        Args:
            message (str): The error message.
            pos_info (PosInfo): The position information of the error.
        """
        self.message = message
        super().__init__(message, pos_info)


class EvaluateError(UserError):
    """Error resulting from a failure to evaluate the program successfully."""

    def __init__(self, message: str, pos_info: PosInfo):
        """Initialize a EvaluateError.

        Args:
            message (str): The error message.
            pos_info (PosInfo): The position information of the error.
        """
        self.message = message
        super().__init__(message, pos_info)


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
        pos_info = exc.pos_info
        line_no = pos_info.line_no
        char_no = pos_info.char_no
        length = pos_info.length

        error_message = f"{type(exc).__name__}: {exc.message}"
        print(error_message, file=sys.stderr)
        print()
        program_line = lines[line_no - 1]
        print(program_line, file=sys.stderr)

        carets = "-" * (char_no - 1) + "^" * length
        print(carets, file=sys.stderr)

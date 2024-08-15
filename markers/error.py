from markers.type import PosInfo


class ParseError(Exception):
    """Error resulting from a failure to parse the program successfully."""

    pos_info: PosInfo

    def __init__(self, message: str, pos_info: PosInfo):
        """Initialize a ParseError.

        Args:
            message (str): The error message.
            pos_info (PosInfo): The position information of the error.
        """
        self.message = message
        self.pos_info = pos_info
        super().__init__(message)


class EvaluateError(Exception):
    """Error resulting from a failure to evaluate the program successfully."""

    pos_info: PosInfo

    def __init__(self, message: str, pos_info: PosInfo):
        """Initialize a EvaluateError.

        Args:
            message (str): The error message.
            pos_info (PosInfo): The position information of the error.
        """
        self.message = message
        self.pos_info = pos_info
        super().__init__(message)


class InternalError(Exception):
    """Error resulting from an internal failure."""

    def __init__(self, message: str):
        """Initialize a InternalError.

        Args:
            message (str): The error message.
        """
        self.message = message
        super().__init__(message)

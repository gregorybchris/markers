from dataclasses import dataclass
from enum import StrEnum, auto

Env = dict[str, bool]


@dataclass
class PositionInfo:
    """Position information in a program."""

    line_no: int
    char_no: int
    length: int


class Associativity(StrEnum):
    """Operator associativity."""

    LEFT = auto()
    RIGHT = auto()

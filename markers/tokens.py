from dataclasses import dataclass, field
from typing import Optional

from markers.type import Associativity, PositionInfo


@dataclass(kw_only=True)
class Token:
    """Program token."""

    pos: PositionInfo = field(default_factory=lambda: PositionInfo(0, 0, 0))

    @property
    def precedence(self) -> int:
        """Return the precedence of the token."""
        return 0

    @property
    def associativity(self) -> Optional[Associativity]:
        """Return the associativity of the token."""
        return None


@dataclass
class LitToken(Token):
    """Boolean literal token."""

    value: bool

    @property
    def precedence(self) -> int:
        """Return the precedence of the token."""
        return 2

    def __str__(self) -> str:
        """Return the string representation of the token."""
        return str(self.value).lower()


@dataclass
class NameToken(Token):
    """Variable name token."""

    value: str

    @property
    def precedence(self) -> int:
        """Return the precedence of the token."""
        return 1

    def __str__(self) -> str:
        """Return the string representation of the token."""
        return self.value


@dataclass
class AndOpToken(Token):
    """And operator token."""

    @property
    def precedence(self) -> int:
        """Return the precedence of the token."""
        return 5

    @property
    def associativity(self) -> Optional[Associativity]:
        """Return the associativity of the token."""
        return Associativity.RIGHT

    def __str__(self) -> str:
        """Return the string representation of the token."""
        return "and"


@dataclass
class OrOpToken(Token):
    """Or operator token."""

    @property
    def precedence(self) -> int:
        """Return the precedence of the token."""
        return 6

    @property
    def associativity(self) -> Optional[Associativity]:
        """Return the associativity of the token."""
        return Associativity.RIGHT

    def __str__(self) -> str:
        """Return the string representation of the token."""
        return "or"


@dataclass
class NotOpToken(Token):
    """Not operator token."""

    @property
    def precedence(self) -> int:
        """Return the precedence of the token."""
        return 4

    def __str__(self) -> str:
        """Return the string representation of the token."""
        return "not"


@dataclass
class LeftParenToken(Token):
    """Left parenthesis token."""

    @property
    def precedence(self) -> int:
        """Return the precedence of the token."""
        return 3

    def __str__(self) -> str:
        """Return the string representation of the token."""
        return "("


@dataclass
class RightParenToken(Token):
    """Right parenthesis token."""

    @property
    def precedence(self) -> int:
        """Return the precedence of the token."""
        return 3

    def __str__(self) -> str:
        """Return the string representation of the token."""
        return ")"


@dataclass
class EofToken(Token):
    """End of file token."""

    def __str__(self) -> str:
        """Return the string representation of the token."""
        return "EOF"

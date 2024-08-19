from dataclasses import dataclass, field

from markers.type import PositionInfo


@dataclass(kw_only=True)
class Token:
    """Program token."""

    # prec: int
    pos: PositionInfo = field(default_factory=lambda: PositionInfo(0, 0, 0))
    # assoc: Optional[Associativity] = None


@dataclass
class LitToken(Token):
    """Boolean literal token."""

    value: bool

    def __str__(self) -> str:
        """Return the string representation of the token."""
        return str(self.value).lower()


@dataclass
class NameToken(Token):
    """Variable name token."""

    value: str

    def __str__(self) -> str:
        """Return the string representation of the token."""
        return self.value


@dataclass
class AndOperatorToken(Token):
    """And operator token."""

    def __str__(self) -> str:
        """Return the string representation of the token."""
        return "and"


@dataclass
class OrOperatorToken(Token):
    """Or operator token."""

    def __str__(self) -> str:
        """Return the string representation of the token."""
        return "or"


@dataclass
class NotOperatorToken(Token):
    """Not operator token."""

    def __str__(self) -> str:
        """Return the string representation of the token."""
        return "not"


@dataclass
class LeftParenToken(Token):
    """Left parenthesis token."""

    def __str__(self) -> str:
        """Return the string representation of the token."""
        return "("


@dataclass
class RightParenToken(Token):
    """Right parenthesis token."""

    def __str__(self) -> str:
        """Return the string representation of the token."""
        return ")"


@dataclass
class EofToken(Token):
    """End of file token."""

    def __str__(self) -> str:
        """Return the string representation of the token."""
        return "EOF"

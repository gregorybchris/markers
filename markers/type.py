from dataclasses import dataclass
from enum import StrEnum

Env = dict[str, bool]


@dataclass
class PosInfo:
    """Position information in a program."""

    line_no: int
    char_no: int
    length: int


@dataclass
class Token:
    """Program token."""

    pos_info: PosInfo
    text: str


class BinaryOpToken(StrEnum):
    """Binary operator kind."""

    AND = "and"
    OR = "or"


class UnaryOpToken(StrEnum):
    """Unary operator kind."""

    NOT = "not"


class ParenToken(StrEnum):
    """Parentheses tokens."""

    LEFT_PAREN = "("
    RIGHT_PAREN = ")"


class LitToken(StrEnum):
    """Literal tokens."""

    TRUE = "true"
    FALSE = "false"


class BinaryOpKind(StrEnum):
    """Binary operator kind."""

    AND = "and"
    OR = "or"


class UnaryOpKind(StrEnum):
    """Unary operator kind."""

    NOT = "not"


@dataclass
class Expr:
    """AST expression node."""

    pos_info: PosInfo


@dataclass
class BinaryOp(Expr):
    """AST expression node for binary operators."""

    kind: BinaryOpKind
    left: Expr
    right: Expr

    def __str__(self) -> str:
        """Return the string representation of the binary operator."""
        return f"({self.left} {self.kind} {self.right})"


@dataclass
class UnaryOp(Expr):
    """AST expression node for unary operators."""

    kind: UnaryOpKind
    arg: Expr

    def __str__(self) -> str:
        """Return the string representation of the unary operator."""
        return f"({self.kind} {self.arg})"


@dataclass
class Var(Expr):
    """AST expression node for variables."""

    name: str

    def __str__(self) -> str:
        """Return the string representation of the variable."""
        return f"{self.name}"


@dataclass
class Lit(Expr):
    """AST expression node for literals."""

    val: bool

    def __str__(self) -> str:
        """Return the string representation of the literal."""
        return f"{self.val}"

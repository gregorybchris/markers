from dataclasses import dataclass, field
from enum import StrEnum, auto

from markers.type import PositionInfo


@dataclass(kw_only=True)
class Expr:
    """Expression node."""

    pos: PositionInfo = field(default_factory=lambda: PositionInfo(0, 0, 0))


class BinaryOpKind(StrEnum):
    """Binary operator kind."""

    AND = auto()
    OR = auto()


class UnaryOpKind(StrEnum):
    """Unary operator kind."""

    NOT = auto()


@dataclass
class BinaryOp(Expr):
    """Expression node for binary operators."""

    kind: BinaryOpKind
    left: Expr
    right: Expr

    def __str__(self) -> str:
        """Return the string representation of the binary operator."""
        return f"({self.left} {self.kind} {self.right})"


@dataclass
class UnaryOp(Expr):
    """Expression node for unary operators."""

    kind: UnaryOpKind
    arg: Expr

    def __str__(self) -> str:
        """Return the string representation of the unary operator."""
        return f"({self.kind} {self.arg})"


@dataclass
class Var(Expr):
    """Expression node for variables."""

    name: str

    def __str__(self) -> str:
        """Return the string representation of the variable."""
        return f"{self.name}"


@dataclass
class Lit(Expr):
    """Expression node for literals."""

    val: bool

    def __str__(self) -> str:
        """Return the string representation of the literal."""
        return f"{self.val}"

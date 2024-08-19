from dataclasses import dataclass
from typing import Callable, Optional, Sequence

from markers.error import ParseError
from markers.expressions import (
    BinaryOp,
    BinaryOpKind,
    Expr,
    Lit,
    PositionInfo,
    UnaryOp,
    UnaryOpKind,
    Var,
)
from markers.tokens import (
    AndOpToken,
    LeftParenToken,
    LitToken,
    NameToken,
    NotOpToken,
    OrOpToken,
    RightParenToken,
    Token,
)


@dataclass
class ParserBase:
    """Boolean expression parser base class."""

    # TODO: Accept an iterable collection of tokens.
    tokens: Sequence[Token]
    idx: int = 0

    def _match(self, token_type: type) -> Optional[Token]:
        if not self._has():
            return None
        token = self._peek()
        if isinstance(token, token_type):
            self._advance()
            return token
        return None

    def _advance(self) -> None:
        if self._has():
            self.idx += 1

    def _next(self) -> Token:
        token = self._peek()
        self._advance()
        return token

    def _peek(self) -> Token:
        return self.tokens[self.idx]

    def _has(self) -> bool:
        return self.idx < len(self.tokens)


@dataclass
class Parser(ParserBase):
    """Boolean expression parser."""

    def parse(self) -> Expr:
        """Parse the boolean expression.

        Raises:
            ParseError: If the expression is invalid.

        Returns:
            Expr: The AST expression node.
        """
        result = self._first_fn()
        if self._has():
            token = self._peek()
            msg = f'Unexpected token "{token!s}"'
            raise ParseError(msg, token.pos)
        return result

    def _get_table(
        self,
    ) -> list[Callable[[], Expr]]:
        return [
            self._or,
            self._and,
            self._not,
            self._paren,
            self._lit,
            self._var,
            self._default,
        ]

    def _first_fn(self) -> Expr:
        return self._get_table()[0]()

    def _next_fn(self, fn: Callable[[], Expr]) -> Expr:
        table = self._get_table()
        precedence = table.index(fn)
        return table[precedence + 1]()

    def _or(self) -> Expr:
        left = self._next_fn(self._or)
        while token := self._match(OrOpToken):
            right = self._next_fn(self._or)
            left = BinaryOp(BinaryOpKind.OR, left, right, pos=token.pos)
        return left

    def _and(self) -> Expr:
        left = self._next_fn(self._and)
        while token := self._match(AndOpToken):
            right = self._next_fn(self._and)
            left = BinaryOp(BinaryOpKind.AND, left, right, pos=token.pos)
        return left

    def _not(self) -> Expr:
        if token := self._match(NotOpToken):
            arg = self._not()
            return UnaryOp(UnaryOpKind.NOT, arg, pos=token.pos)
        return self._next_fn(self._not)

    def _paren(self) -> Expr:
        if token := self._match(LeftParenToken):
            result = self._first_fn()
            if not self._match(RightParenToken):
                msg = "Expected closing paren matching opening"
                raise ParseError(msg, token.pos)
            return result
        return self._next_fn(self._paren)

    def _lit(self) -> Expr:
        if token := self._match(LitToken):
            assert isinstance(token, LitToken)
            return Lit(token.value, pos=token.pos)
        return self._next_fn(self._lit)

    def _var(self) -> Expr:
        if token := self._match(NameToken):
            assert isinstance(token, NameToken)
            if not token.value.isidentifier():
                msg = f'Unexpected token "{token.value}"'
                raise ParseError(msg, token.pos)
            return Var(token.value, pos=token.pos)
        return self._next_fn(self._var)

    def _default(self) -> Expr:
        if len(self.tokens) == 0:
            msg = "Unexpected end of input"
            raise ParseError(msg, PositionInfo(0, 0, 0))

        # TODO: Avoid accessing tokens directly
        token = self.tokens[-1]
        msg = "Unexpected end of input"
        raise ParseError(msg, token.pos)

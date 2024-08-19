from dataclasses import dataclass
from typing import Callable, Sequence

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

    tokens: Sequence[Token]
    idx: int = 0

    def _match(self, token_type: type) -> bool:
        return self._has() and isinstance(self._curr(), token_type)

    def _advance(self) -> None:
        if self._has():
            self.idx += 1

    def _curr(self) -> Token:
        return self.tokens[self.idx]

    def _prev(self) -> Token:
        return self.tokens[self.idx - 1]

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
            token = self._curr()
            msg = f'Unexpected token "{token!s}" at line {token.pos.line_no}, char {token.pos.char_no}'
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
        while self._match(OrOpToken):
            token = self._curr()
            self._advance()
            right = self._next_fn(self._or)
            left = BinaryOp(BinaryOpKind.OR, left, right, pos=token.pos)
        return left

    def _and(self) -> Expr:
        left = self._next_fn(self._and)
        while self._match(AndOpToken):
            token = self._curr()
            self._advance()
            right = self._next_fn(self._and)
            left = BinaryOp(BinaryOpKind.AND, left, right, pos=token.pos)
        return left

    def _not(self) -> Expr:
        if self._match(NotOpToken):
            token = self._curr()
            self._advance()
            left = self._not()
            return UnaryOp(UnaryOpKind.NOT, left, pos=token.pos)
        return self._next_fn(self._not)

    def _paren(self) -> Expr:
        if self._match(LeftParenToken):
            self._advance()
            result = self._first_fn()
            if self._match(RightParenToken):
                self._advance()
            else:
                token = self._prev()
                msg = f"Expected token {RightParenToken()!s} at line {token.pos.line_no}, char {token.pos.char_no}"
                raise ParseError(msg, token.pos)
            return result
        return self._next_fn(self._paren)

    def _lit(self) -> Expr:
        if self._match(LitToken):
            token = self._curr()
            assert isinstance(token, LitToken)
            self._advance()
            return Lit(token.value, pos=token.pos)
        return self._next_fn(self._lit)

    def _var(self) -> Expr:
        if self._match(NameToken):
            token = self._curr()
            assert isinstance(token, NameToken)
            self._advance()

            if not token.value.isidentifier():
                msg = f'Unexpected token "{token.value}" at line {token.pos.line_no}, char {token.pos.char_no}'
                raise ParseError(msg, token.pos)

            return Var(token.value, pos=token.pos)
        return self._next_fn(self._var)

    def _default(self) -> Expr:  # noqa: PLR6301
        msg = "Unexpected end of input"
        # TODO(chris): Maybe handle this case better?
        raise ParseError(msg, PositionInfo(0, 0, 0))

from dataclasses import dataclass

from markers.error import ParseError
from markers.type import (
    BinaryOp,
    BinaryOpKind,
    BinaryOpToken,
    Expr,
    Lit,
    LitToken,
    ParenToken,
    PositionInfo,
    Token,
    UnaryOp,
    UnaryOpKind,
    UnaryOpToken,
    Var,
)


@dataclass
class ParserBase:
    """Boolean expression parser base class."""

    tokens: list[Token]
    idx: int = 0

    def _match(self, token_text: str) -> bool:
        return self._has() and self._curr().text == token_text

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
        result = self._or()
        if self._has():
            token = self._curr()
            msg = f'Unexpected token "{token.text}" at line {token.pos.line_no}, char {token.pos.char_no}'
            raise ParseError(msg, token.pos)
        return result

    def _or(self) -> Expr:
        left = self._and()
        while self._match(BinaryOpToken.OR):
            token = self._curr()
            self._advance()
            right = self._and()
            left = BinaryOp(BinaryOpKind.OR, left, right, pos=token.pos)
        return left

    def _and(self) -> Expr:
        left = self._not()
        while self._match(BinaryOpToken.AND):
            token = self._curr()
            self._advance()
            right = self._not()
            left = BinaryOp(BinaryOpKind.AND, left, right, pos=token.pos)
        return left

    def _not(self) -> Expr:
        if self._match(UnaryOpToken.NOT):
            token = self._curr()
            self._advance()
            left = self._not()
            return UnaryOp(UnaryOpKind.NOT, left, pos=token.pos)
        return self._paren()

    def _paren(self) -> Expr:
        if self._match(ParenToken.LEFT_PAREN):
            self._advance()
            result = self._or()
            if self._match(ParenToken.RIGHT_PAREN):
                self._advance()
            else:
                token = self._prev()
                msg = f"Expected token {ParenToken.RIGHT_PAREN} at line {token.pos.line_no}, char {token.pos.char_no}"
                raise ParseError(msg, token.pos)
            return result
        return self._lit()

    def _lit(self) -> Expr:
        if self._match(LitToken.TRUE):
            token = self._curr()
            self._advance()
            return Lit(True, pos=token.pos)
        if self._match(LitToken.FALSE):
            token = self._curr()
            self._advance()
            return Lit(False, pos=token.pos)
        return self._var()

    def _var(self) -> Expr:
        if self._has():
            token = self._curr()
            name = token.text
            if name.isidentifier():
                token = self._curr()
                self._advance()
                return Var(name, pos=token.pos)
        return self._default()

    def _default(self) -> Expr:
        if not self._has():
            msg = "Unexpected end of input"
            # TODO(chris): Maybe handle this case better?
            raise ParseError(msg, PositionInfo(0, 0, 0))

        token = self._curr()
        msg = f'Unexpected token "{token.text}" at line {token.pos.line_no}, char {token.pos.char_no}'
        raise ParseError(msg, token.pos)

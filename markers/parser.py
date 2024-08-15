from dataclasses import dataclass

from markers.error import ParseError
from markers.type import (
    BinaryOp,
    BinaryOpKind,
    BinaryOpTokens,
    BoolTokens,
    Expr,
    Lit,
    ParenTokens,
    PosInfo,
    Token,
    UnaryOp,
    UnaryOpKind,
    UnaryOpTokens,
    Var,
)


@dataclass
class Parser:
    """Boolean expression parser."""

    tokens: list[Token]
    pos: int = 0

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
            pos_info = token.pos_info
            msg = f'Unexpected token "{token.text}" at line {pos_info.line_no}, char {pos_info.char_no}'
            raise ParseError(msg, pos_info)
        return result

    def _or(self) -> Expr:
        left = self._and()
        while self._match(BinaryOpTokens.OR):
            token = self._curr()
            self._advance()
            right = self._and()
            left = BinaryOp(token.pos_info, BinaryOpKind.OR, left, right)
        return left

    def _and(self) -> Expr:
        left = self._not()
        while self._match(BinaryOpTokens.AND):
            token = self._curr()
            self._advance()
            right = self._not()
            left = BinaryOp(token.pos_info, BinaryOpKind.AND, left, right)
        return left

    def _not(self) -> Expr:
        if self._match(UnaryOpTokens.NOT):
            token = self._curr()
            self._advance()
            left = self._not()
            return UnaryOp(token.pos_info, UnaryOpKind.NOT, left)
        return self._paren()

    def _paren(self) -> Expr:
        if self._match(ParenTokens.LEFT_PAREN):
            self._advance()
            result = self._or()
            if self._match(ParenTokens.RIGHT_PAREN):
                self._advance()
            else:
                token = self._prev()
                pos_info = token.pos_info
                msg = f"Expected token {ParenTokens.RIGHT_PAREN} at line {pos_info.line_no}, char {pos_info.char_no}"
                raise ParseError(msg, pos_info)
            return result
        return self._lit()

    def _lit(self) -> Expr:
        if self._match(BoolTokens.TRUE):
            token = self._curr()
            self._advance()
            return Lit(token.pos_info, True)
        if self._match(BoolTokens.FALSE):
            token = self._curr()
            self._advance()
            return Lit(token.pos_info, False)
        return self._var()

    def _var(self) -> Expr:
        if self._has():
            token = self._curr()
            name = token.text
            if name.isidentifier():
                token = self._curr()
                self._advance()
                return Var(token.pos_info, name)
        return self._default()

    def _default(self) -> Expr:
        if not self._has():
            msg = "Unexpected end of input"
            # TODO(chris): Maybe handle this case better?
            raise ParseError(msg, PosInfo(0, 0, 0))

        token = self._curr()
        pos_info = token.pos_info
        msg = f'Unexpected token "{token.text}" at line {pos_info.line_no}, char {pos_info.char_no}'
        raise ParseError(msg, pos_info)

    def _match(self, token_text: str) -> bool:
        return self._has() and self._curr().text == token_text

    def _advance(self) -> None:
        if self._has():
            self.pos += 1

    def _curr(self) -> Token:
        return self.tokens[self.pos]

    def _prev(self) -> Token:
        return self.tokens[self.pos - 1]

    def _has(self) -> bool:
        return self.pos < len(self.tokens)

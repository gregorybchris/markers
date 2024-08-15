from dataclasses import dataclass

from markers.type import (
    BinaryOp,
    BinaryOpKind,
    BinaryOpTokens,
    BoolTokens,
    Expr,
    Lit,
    ParenTokens,
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
            SyntaxError: If the expression is invalid.

        Returns:
            Expr: The AST expression node.
        """
        result = self._or()
        if self._has():
            token = self._peek()
            pos_info = token.pos_info
            msg = f'Unexpected token "{token.text}" at line {pos_info.line_no}, char {pos_info.char_no}'
            raise SyntaxError(msg)
        return result

    def _or(self) -> Expr:
        left = self._and()
        while self._match(BinaryOpTokens.OR):
            token = self._prev()
            right = self._and()
            left = BinaryOp(token.pos_info, BinaryOpKind.OR, left, right)
        return left

    def _and(self) -> Expr:
        left = self._not()
        while self._match(BinaryOpTokens.AND):
            token = self._prev()
            right = self._not()
            left = BinaryOp(token.pos_info, BinaryOpKind.AND, left, right)
        return left

    def _not(self) -> Expr:
        if self._match(UnaryOpTokens.NOT):
            token = self._prev()
            left = self._not()
            return UnaryOp(token.pos_info, UnaryOpKind.NOT, left)
        return self._paren()

    def _paren(self) -> Expr:
        if self._match(ParenTokens.LEFT_PAREN):
            result = self._or()
            if not self._match(ParenTokens.RIGHT_PAREN):
                token = self._prev()
                pos_info = token.pos_info
                msg = f"Expected token {ParenTokens.RIGHT_PAREN} at line {pos_info.line_no}, char {pos_info.char_no}"
                raise SyntaxError(msg)
            return result
        return self._lit()

    def _lit(self) -> Expr:
        if self._match(BoolTokens.TRUE):
            token = self._prev()
            return Lit(token.pos_info, True)
        if self._match(BoolTokens.FALSE):
            token = self._prev()
            return Lit(token.pos_info, False)
        return self._var()

    def _var(self) -> Expr:
        if self._has():
            token = self._peek()
            name = token.text
            if name.isidentifier():
                self._next()
                token = self._prev()
                return Var(token.pos_info, name)
        return self._default()

    def _default(self) -> Expr:
        if not self._has():
            msg = "Unexpected end of input"
            raise SyntaxError(msg)

        token = self._peek()
        pos_info = token.pos_info
        msg = f'Unexpected token "{token.text}" at line {pos_info.line_no}, char {pos_info.char_no}'
        raise SyntaxError(msg)

    def _match(self, token_text: str) -> bool:
        if self._has() and self._peek().text == token_text:
            self._next()
            return True
        return False

    def _next(self) -> None:
        if self._has():
            self.pos += 1

    def _peek(self) -> Token:
        return self.tokens[self.pos]

    def _prev(self) -> Token:
        return self.tokens[self.pos - 1]

    def _has(self) -> bool:
        return self.pos < len(self.tokens)

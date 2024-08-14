from dataclasses import dataclass

from markers.types import (
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
    char_num: int = 0

    def parse(self) -> Expr:
        """Parse the boolean expression.

        Raises:
            SyntaxError: If the expression is invalid.

        Returns:
            Expr: The AST expression node.
        """
        result = self._or()
        if self._has():
            msg = f'Unexpected token "{self._peek()}" at position {self.char_num}'
            raise SyntaxError(msg)
        return result

    def _or(self) -> Expr:
        left = self._and()
        while self._match(BinaryOpTokens.OR):
            right = self._and()
            left = BinaryOp(BinaryOpKind.OR, left, right)
        return left

    def _and(self) -> Expr:
        left = self._not()
        while self._match(BinaryOpTokens.AND):
            right = self._not()
            left = BinaryOp(BinaryOpKind.AND, left, right)
        return left

    def _not(self) -> Expr:
        while self._match(UnaryOpTokens.NOT):
            left = self._not()
            return UnaryOp(UnaryOpKind.NOT, left)
        return self._paren()

    def _paren(self) -> Expr:
        if self._match(ParenTokens.LEFT_PAREN):
            result = self._or()
            if not self._match(ParenTokens.RIGHT_PAREN):
                msg = f"Expected token {ParenTokens.RIGHT_PAREN} at position {self.char_num}"
                raise SyntaxError(msg)
            return result
        return self._lit()

    def _lit(self) -> Expr:
        if self._match(BoolTokens.TRUE):
            return Lit(True)
        if self._match(BoolTokens.FALSE):
            return Lit(False)
        return self._var()

    def _var(self) -> Expr:
        if not self._has():
            msg = "Unexpected end of input"
            raise SyntaxError(msg)

        if not self._peek().isidentifier():
            msg = f'Unexpected token "{self._peek()}" at position {self.char_num}'
            raise SyntaxError(msg)

        name = self._peek()
        self._next()
        return Var(name)

    def _match(self, token: Token) -> bool:
        if self._has() and self._peek() == token:
            self._next()
            return True
        return False

    def _next(self) -> None:
        if self._has():
            self.char_num += len(self._peek())
            self.pos += 1

    def _peek(self) -> Token:
        return self.tokens[self.pos]

    def _prev(self) -> Token:
        return self.tokens[self.pos - 1]

    def _has(self) -> bool:
        return self.pos < len(self.tokens)

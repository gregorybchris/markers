from dataclasses import dataclass
from typing import Iterator

from markers.error import InternalError
from markers.tokens import (
    AndOpToken,
    EofToken,
    LeftParenToken,
    LitToken,
    NameToken,
    NotOpToken,
    OrOpToken,
    PositionInfo,
    RightParenToken,
    Token,
)


@dataclass
class LexerBase:
    """Lexer base class."""

    text: str
    idx: int = 0
    line_no: int = 1
    char_no: int = 1

    def _has_char(self) -> bool:
        return self.idx < len(self.text)

    def _next_char(self) -> str:
        c = self._peek_char()
        self.idx += 1
        if c == "\n":
            self.line_no += 1
            self.char_no = 1
        else:
            self.char_no += 1
        return c

    def _peek_char(self) -> str:
        if not self._has_char():
            msg = "unexpected end of input"
            raise InternalError(msg)
        return self.text[self.idx]


@dataclass
class Lexer(LexerBase):
    """Boolean expression lexer."""

    def next(self) -> Token:  # noqa: PLR0911
        """Get the next token.

        Returns:
            Token: The next token.
        """
        while self._has_char():
            line_no = self.line_no
            char_no = self.char_no
            c = self._next_char()
            if not (c.isspace() or c == "\n"):
                break
        else:
            pos = PositionInfo(line_no, char_no, 0)
            return EofToken(pos=pos)

        if c == "(":
            pos = PositionInfo(line_no, char_no, 1)
            return LeftParenToken(pos=pos)
        if c == ")":
            pos = PositionInfo(line_no, char_no, 1)
            return RightParenToken(pos=pos)
        if self._is_identifier_char(c):
            name = self._read_identifier(c)
            pos = PositionInfo(line_no, char_no, len(name))
            if name == "true":
                return LitToken(True, pos=pos)
            if name == "false":
                return LitToken(False, pos=pos)
            if name == "and":
                return AndOpToken(pos=pos)
            if name == "or":
                return OrOpToken(pos=pos)
            if name == "not":
                return NotOpToken(pos=pos)
            return NameToken(name, pos=pos)

        return NameToken(c, pos=PositionInfo(line_no, char_no, 1))

    def has(self) -> bool:
        """Return whether the lexer has another token.

        Returns:
            bool: Whether the lexer has another token.
        """
        return self._has_char()

    @classmethod
    def _is_identifier_char(cls, c: str) -> bool:
        return c.isalnum() or c in ("_")

    def _read_identifier(self, first_char: str) -> str:
        name = first_char
        while self._has_char():
            c = self._peek_char()
            if self._is_identifier_char(c):
                name += self._next_char()
            else:
                break
        return name

    @classmethod
    def iter_tokens(cls, program: str) -> Iterator[Token]:
        """Iterate over the tokens of a boolean expression.

        Args:
            program (str): The boolean expression program.

        Yields:
            Token: The next token.
        """
        lexer = cls(program)
        while lexer.has():
            token = lexer.next()
            yield token

    @classmethod
    def tokenize(cls, program: str) -> list[Token]:
        """Tokenize a boolean expression.

        Args:
            program (str): The boolean expression program.

        Returns:
            list[Token]: The list of tokens.
        """
        tokens = []
        lexer = cls(program)
        while lexer.has():
            token = lexer.next()
            tokens.append(token)
        return tokens

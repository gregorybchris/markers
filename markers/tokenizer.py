from dataclasses import dataclass, field

from markers.type import ParenToken, PositionInfo, Token


@dataclass
class Tokenizer:
    """Boolean expression tokenizer."""

    program: str = ""
    tokens: list[Token] = field(default_factory=list)
    token_text: str = ""
    line_no: int = 1
    char_no: int = 1

    def tokenize(self) -> list[Token]:
        """Tokenize a boolean expression.

        Returns:
            list[Token]: The list of tokens.
        """
        for c in self.program:
            if c in {ParenToken.LEFT_PAREN, ParenToken.RIGHT_PAREN}:
                self._append()
                pos = PositionInfo(self.line_no, self.char_no, 1)
                token = Token(c, pos=pos)
                self.tokens.append(token)
            elif c == " ":
                self._append()
            elif c == "\n":
                self._append()
                self.line_no += 1
                self.char_no = 0
            else:
                self.token_text += c
            self.char_no += 1
        self._append()
        return self.tokens

    def _append(self) -> None:
        if self.token_text:
            token_length = len(self.token_text)
            pos = PositionInfo(self.line_no, self.char_no - token_length, token_length)
            token = Token(self.token_text, pos=pos)
            self.tokens.append(token)
            self.token_text = ""

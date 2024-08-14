from dataclasses import dataclass, field

from markers.types import ParenTokens, Token


@dataclass
class Tokenizer:
    """Boolean expression tokenizer."""

    program: str = ""
    tokens: list[Token] = field(default_factory=list)
    token: str = ""

    def tokenize(self) -> list[Token]:
        """Tokenize a boolean expression.

        Returns:
            list[Token]: The list of tokens.
        """
        for c in self.program:
            if c in [ParenTokens.LEFT_PAREN, ParenTokens.RIGHT_PAREN]:
                self._append()
                self.tokens.append(c)
            elif c == " ":
                self._append()
            else:
                self.token += c
        self._append()
        return self.tokens

    def _append(self) -> None:
        if self.token != "":
            self.tokens.append(self.token)
            self.token = ""

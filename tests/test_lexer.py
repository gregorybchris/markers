from markers.lexer import Lexer
from markers.tokens import (
    AndOpToken,
    LeftParenToken,
    NameToken,
    NotOpToken,
    OrOpToken,
    PositionInfo,
    RightParenToken,
    Token,
)


class TestLexer:
    def _to_strings(self, tokens: list[Token]) -> list[str]:
        return [str(token) for token in tokens]

    def test_tokenize_var(self) -> None:
        text = "A"
        tokens = Lexer.tokenize(text)
        assert self._to_strings(tokens) == ["A"]

    def test_tokenize_not(self) -> None:
        text = "not A"
        tokens = Lexer.tokenize(text)
        assert self._to_strings(tokens) == ["not", "A"]

    def test_tokenize_and(self) -> None:
        text = "A and B"
        tokens = Lexer.tokenize(text)
        assert self._to_strings(tokens) == ["A", "and", "B"]

    def test_tokenize_or(self) -> None:
        text = "A or B"
        tokens = Lexer.tokenize(text)
        assert self._to_strings(tokens) == ["A", "or", "B"]

    def test_tokenize_parentheses(self) -> None:
        text = "A and (B or C)"
        tokens = Lexer.tokenize(text)
        assert self._to_strings(tokens) == ["A", "and", "(", "B", "or", "C", ")"]

    def test_tokenize_parentheses_extra_space(self) -> None:
        text = "A and ( B or C )"
        tokens = Lexer.tokenize(text)
        assert self._to_strings(tokens) == ["A", "and", "(", "B", "or", "C", ")"]

    def test_tokenize_parentheses_no_space(self) -> None:
        text = "(A)and not(B or C)"
        tokens = Lexer.tokenize(text)
        assert self._to_strings(tokens) == ["(", "A", ")", "and", "not", "(", "B", "or", "C", ")"]

    def test_tokenize_boolean_literals(self) -> None:
        text = "true and false"
        tokens = Lexer.tokenize(text)
        assert self._to_strings(tokens) == ["true", "and", "false"]

    def test_tokenize_adds_position_info(self) -> None:
        text = "(A)and\nnot(B or C)"
        tokens = Lexer.tokenize(text)
        assert tokens == [
            LeftParenToken(pos=PositionInfo(1, 1, 1)),
            NameToken("A", pos=PositionInfo(1, 2, 1)),
            RightParenToken(pos=PositionInfo(1, 3, 1)),
            AndOpToken(pos=PositionInfo(1, 4, 3)),
            NotOpToken(pos=PositionInfo(2, 1, 3)),
            LeftParenToken(pos=PositionInfo(2, 4, 1)),
            NameToken("B", pos=PositionInfo(2, 5, 1)),
            OrOpToken(pos=PositionInfo(2, 7, 2)),
            NameToken("C", pos=PositionInfo(2, 10, 1)),
            RightParenToken(pos=PositionInfo(2, 11, 1)),
        ]

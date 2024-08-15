from markers import Tokenizer
from markers.type import PositionInfo, Token


class TestTokenizer:
    def _to_strings(self, tokens: list[Token]) -> list[str]:
        return [token.text for token in tokens]

    def test_tokenize_var(self) -> None:
        program = "A"
        tokens = Tokenizer(program).tokenize()
        assert self._to_strings(tokens) == ["A"]

    def test_tokenize_not(self) -> None:
        program = "not A"
        tokens = Tokenizer(program).tokenize()
        assert self._to_strings(tokens) == ["not", "A"]

    def test_tokenize_and(self) -> None:
        program = "A and B"
        tokens = Tokenizer(program).tokenize()
        assert self._to_strings(tokens) == ["A", "and", "B"]

    def test_tokenize_or(self) -> None:
        program = "A or B"
        tokens = Tokenizer(program).tokenize()
        assert self._to_strings(tokens) == ["A", "or", "B"]

    def test_tokenize_parentheses(self) -> None:
        program = "A and (B or C)"
        tokens = Tokenizer(program).tokenize()
        assert self._to_strings(tokens) == ["A", "and", "(", "B", "or", "C", ")"]

    def test_tokenize_parentheses_extra_space(self) -> None:
        program = "A and ( B or C )"
        tokens = Tokenizer(program).tokenize()
        assert self._to_strings(tokens) == ["A", "and", "(", "B", "or", "C", ")"]

    def test_tokenize_parentheses_no_space(self) -> None:
        program = "(A)and not(B or C)"
        tokens = Tokenizer(program).tokenize()
        assert self._to_strings(tokens) == ["(", "A", ")", "and", "not", "(", "B", "or", "C", ")"]

    def test_tokenize_boolean_literals(self) -> None:
        program = "true and false"
        tokens = Tokenizer(program).tokenize()
        assert self._to_strings(tokens) == ["true", "and", "false"]

    def test_tokenize_adds_position_info(self) -> None:
        program = "(A)and\nnot(B or C)"
        tokens = Tokenizer(program).tokenize()
        assert tokens == [
            Token("(", pos=PositionInfo(1, 1, 1)),
            Token("A", pos=PositionInfo(1, 2, 1)),
            Token(")", pos=PositionInfo(1, 3, 1)),
            Token("and", pos=PositionInfo(1, 4, 3)),
            Token("not", pos=PositionInfo(2, 1, 3)),
            Token("(", pos=PositionInfo(2, 4, 1)),
            Token("B", pos=PositionInfo(2, 5, 1)),
            Token("or", pos=PositionInfo(2, 7, 2)),
            Token("C", pos=PositionInfo(2, 10, 1)),
            Token(")", pos=PositionInfo(2, 11, 1)),
        ]

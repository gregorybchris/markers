from markers import Tokenizer
from markers.type import PosInfo, Token


class TestTokenizer:
    def _list_token_strings(self, tokens: list[Token]) -> list[str]:
        return [token.text for token in tokens]

    def test_tokenize_var(self) -> None:
        program = "A"
        tokens = Tokenizer(program).tokenize()
        assert self._list_token_strings(tokens) == ["A"]

    def test_tokenize_not(self) -> None:
        program = "not A"
        tokens = Tokenizer(program).tokenize()
        assert self._list_token_strings(tokens) == ["not", "A"]

    def test_tokenize_and(self) -> None:
        program = "A and B"
        tokens = Tokenizer(program).tokenize()
        assert self._list_token_strings(tokens) == ["A", "and", "B"]

    def test_tokenize_or(self) -> None:
        program = "A or B"
        tokens = Tokenizer(program).tokenize()
        assert self._list_token_strings(tokens) == ["A", "or", "B"]

    def test_tokenize_parentheses(self) -> None:
        program = "A and (B or C)"
        tokens = Tokenizer(program).tokenize()
        assert self._list_token_strings(tokens) == ["A", "and", "(", "B", "or", "C", ")"]

    def test_tokenize_parentheses_extra_space(self) -> None:
        program = "A and ( B or C )"
        tokens = Tokenizer(program).tokenize()
        assert self._list_token_strings(tokens) == ["A", "and", "(", "B", "or", "C", ")"]

    def test_tokenize_parentheses_no_space(self) -> None:
        program = "(A)and not(B or C)"
        tokens = Tokenizer(program).tokenize()
        assert self._list_token_strings(tokens) == ["(", "A", ")", "and", "not", "(", "B", "or", "C", ")"]

    def test_tokenize_boolean_literals(self) -> None:
        program = "true and false"
        tokens = Tokenizer(program).tokenize()
        assert self._list_token_strings(tokens) == ["true", "and", "false"]

    def test_tokenize_adds_position_info(self) -> None:
        program = "(A)and\nnot(B or C)"
        tokens = Tokenizer(program).tokenize()
        assert tokens == [
            Token(PosInfo(1, 1, 1), "("),
            Token(PosInfo(1, 2, 1), "A"),
            Token(PosInfo(1, 3, 1), ")"),
            Token(PosInfo(1, 4, 3), "and"),
            Token(PosInfo(2, 1, 3), "not"),
            Token(PosInfo(2, 4, 1), "("),
            Token(PosInfo(2, 5, 1), "B"),
            Token(PosInfo(2, 7, 2), "or"),
            Token(PosInfo(2, 10, 1), "C"),
            Token(PosInfo(2, 11, 1), ")"),
        ]

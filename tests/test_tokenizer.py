from markers import Tokenizer


class TestTokenizer:
    def test_tokenize_var(self) -> None:
        program = "A"
        tokenizer = Tokenizer(program)
        tokens = tokenizer.tokenize()
        assert tokens == ["A"]

    def test_tokenize_not(self) -> None:
        program = "not A"
        tokenizer = Tokenizer(program)
        tokens = tokenizer.tokenize()
        assert tokens == ["not", "A"]

    def test_tokenize_and(self) -> None:
        program = "A and B"
        tokenizer = Tokenizer(program)
        tokens = tokenizer.tokenize()
        assert tokens == ["A", "and", "B"]

    def test_tokenize_or(self) -> None:
        program = "A or B"
        tokenizer = Tokenizer(program)
        tokens = tokenizer.tokenize()
        assert tokens == ["A", "or", "B"]

    def test_tokenize_parentheses(self) -> None:
        program = "A and (B or C)"
        tokenizer = Tokenizer(program)
        tokens = tokenizer.tokenize()
        assert tokens == ["A", "and", "(", "B", "or", "C", ")"]

    def test_tokenize_parentheses_extra_space(self) -> None:
        program = "A and ( B or C )"
        tokenizer = Tokenizer(program)
        tokens = tokenizer.tokenize()
        assert tokens == ["A", "and", "(", "B", "or", "C", ")"]

    def test_tokenize_parentheses_no_space(self) -> None:
        program = "(A)and not(B or C)"
        tokenizer = Tokenizer(program)
        tokens = tokenizer.tokenize()
        assert tokens == ["(", "A", ")", "and", "not", "(", "B", "or", "C", ")"]

    def test_tokenize_boolean_literals(self) -> None:
        program = "true and false"
        tokenizer = Tokenizer(program)
        tokens = tokenizer.tokenize()
        assert tokens == ["true", "and", "false"]

import re

import pytest
from markers import Parser
from markers.types import BinaryOp, BinaryOpKind, Lit, Token, UnaryOp, UnaryOpKind, Var


class TestParser:
    def test_parse_var(self) -> None:
        tokens = ["A"]
        expr = Parser(tokens).parse()
        assert expr == Var("A")

    def test_parse_not(self) -> None:
        tokens = ["not", "A"]
        expr = Parser(tokens).parse()
        assert expr == UnaryOp(UnaryOpKind.NOT, Var("A"))

    def test_parse_and(self) -> None:
        tokens = ["A", "and", "B"]
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(BinaryOpKind.AND, Var("A"), Var("B"))

    def test_parse_or(self) -> None:
        tokens = ["A", "or", "B"]
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(BinaryOpKind.OR, Var("A"), Var("B"))

    def test_parse_parentheses(self) -> None:
        tokens = ["A", "and", "(", "B", "or", "C", ")"]
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(BinaryOpKind.AND, Var("A"), BinaryOp(BinaryOpKind.OR, Var("B"), Var("C")))

    def test_parse_and_binds_tighter_than_or(self) -> None:
        tokens = ["A", "and", "B", "or", "C"]
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(BinaryOpKind.OR, BinaryOp(BinaryOpKind.AND, Var("A"), Var("B")), Var("C"))

    def test_parse_double_negation(self) -> None:
        tokens = ["not", "not", "A"]
        expr = Parser(tokens).parse()
        assert expr == UnaryOp(UnaryOpKind.NOT, UnaryOp(UnaryOpKind.NOT, Var("A")))

    def test_parse_negation_of_parentheses(self) -> None:
        tokens = ["not", "(", "A", "or", "B", ")"]
        expr = Parser(tokens).parse()
        assert expr == UnaryOp(UnaryOpKind.NOT, BinaryOp(BinaryOpKind.OR, Var("A"), Var("B")))

    def test_parse_missing_right_paren_raises_syntax_error(self) -> None:
        tokens = ["(", "A", "or", "B"]
        with pytest.raises(SyntaxError, match=re.escape("Expected token ) at position 5")):
            Parser(tokens).parse()

    def test_parse_missing_left_paren_raises_syntax_error(self) -> None:
        tokens = ["A", "or", "B", ")"]
        with pytest.raises(SyntaxError, match=re.escape('Unexpected token ")" at position 4')):
            Parser(tokens).parse()

    def test_parse_empty_input_raises_syntax_error(self) -> None:
        tokens: list[Token] = []
        with pytest.raises(SyntaxError, match=re.escape("Unexpected end of input")):
            Parser(tokens).parse()

    def test_incomplete_and_raises_syntax_error(self) -> None:
        tokens = ["A", "and"]
        with pytest.raises(SyntaxError, match=re.escape("Unexpected end of input")):
            Parser(tokens).parse()

    def test_parse_true(self) -> None:
        tokens = ["true"]
        expr = Parser(tokens).parse()
        assert expr == Lit(True)

    def test_parse_false(self) -> None:
        tokens = ["false"]
        expr = Parser(tokens).parse()
        assert expr == Lit(False)

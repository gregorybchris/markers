import re

import pytest
from markers import Parser
from markers.error import ParseError
from markers.type import BinaryOp, BinaryOpKind, Lit, PosInfo, Token, UnaryOp, UnaryOpKind, Var

p = PosInfo(0, 0, 0)


class TestParser:
    def _add_pos_info(self, token_texts: list[str]) -> list[Token]:
        return [Token(p, text) for text in token_texts]

    def test_parse_var(self) -> None:
        tokens = self._add_pos_info(["A"])
        expr = Parser(tokens).parse()
        assert expr == Var(p, "A")

    def test_parse_not(self) -> None:
        tokens = self._add_pos_info(["not", "A"])
        expr = Parser(tokens).parse()
        assert expr == UnaryOp(p, UnaryOpKind.NOT, Var(p, "A"))

    def test_parse_and(self) -> None:
        tokens = self._add_pos_info(["A", "and", "B"])
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(p, BinaryOpKind.AND, Var(p, "A"), Var(p, "B"))

    def test_parse_or(self) -> None:
        tokens = self._add_pos_info(["A", "or", "B"])
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(p, BinaryOpKind.OR, Var(p, "A"), Var(p, "B"))

    def test_parse_parentheses(self) -> None:
        tokens = self._add_pos_info(["A", "and", "(", "B", "or", "C", ")"])
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(
            p, BinaryOpKind.AND, Var(p, "A"), BinaryOp(p, BinaryOpKind.OR, Var(p, "B"), Var(p, "C"))
        )

    def test_parse_and_binds_tighter_than_or(self) -> None:
        tokens = self._add_pos_info(["A", "and", "B", "or", "C"])
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(
            p, BinaryOpKind.OR, BinaryOp(p, BinaryOpKind.AND, Var(p, "A"), Var(p, "B")), Var(p, "C")
        )

    def test_parse_double_negation(self) -> None:
        tokens = self._add_pos_info(["not", "not", "A"])
        expr = Parser(tokens).parse()
        assert expr == UnaryOp(p, UnaryOpKind.NOT, UnaryOp(p, UnaryOpKind.NOT, Var(p, "A")))

    def test_parse_negation_of_parentheses(self) -> None:
        tokens = self._add_pos_info(["not", "(", "A", "or", "B", ")"])
        expr = Parser(tokens).parse()
        assert expr == UnaryOp(p, UnaryOpKind.NOT, BinaryOp(p, BinaryOpKind.OR, Var(p, "A"), Var(p, "B")))

    def test_parse_missing_right_paren_raises_parse_error(self) -> None:
        tokens = self._add_pos_info(["(", "A", "or", "B"])
        with pytest.raises(ParseError, match=re.escape("Expected token ) at line 0, char 0")):
            Parser(tokens).parse()

    def test_parse_missing_left_paren_raises_parse_error(self) -> None:
        tokens = self._add_pos_info(["A", "or", "B", ")"])
        with pytest.raises(ParseError, match=re.escape('Unexpected token ")" at line 0, char 0')):
            Parser(tokens).parse()

    def test_parse_empty_input_raises_parse_error(self) -> None:
        tokens: list[Token] = []
        with pytest.raises(ParseError, match=re.escape("Unexpected end of input")):
            Parser(tokens).parse()

    def test_incomplete_and_raises_parse_error(self) -> None:
        tokens = self._add_pos_info(["A", "and"])
        with pytest.raises(ParseError, match=re.escape("Unexpected end of input")):
            Parser(tokens).parse()

    def test_parse_true(self) -> None:
        tokens = self._add_pos_info(["true"])
        expr = Parser(tokens).parse()
        assert expr == Lit(p, True)

    def test_parse_false(self) -> None:
        tokens = self._add_pos_info(["false"])
        expr = Parser(tokens).parse()
        assert expr == Lit(p, False)

    def test_parse_invalid_var_raises_parse_error(self) -> None:
        tokens = self._add_pos_info(["A", "or", "0_invalid"])
        with pytest.raises(ParseError, match=re.escape('Unexpected token "0_invalid" at line 0, char 0')):
            Parser(tokens).parse()

    def test_parse_repeated_and(self) -> None:
        tokens = self._add_pos_info(["A", "and", "B", "and", "C"])
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(
            p, BinaryOpKind.AND, BinaryOp(p, BinaryOpKind.AND, Var(p, "A"), Var(p, "B")), Var(p, "C")
        )

    def test_parse_repeated_or(self) -> None:
        tokens = self._add_pos_info(["A", "or", "B", "or", "C"])
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(p, BinaryOpKind.OR, BinaryOp(p, BinaryOpKind.OR, Var(p, "A"), Var(p, "B")), Var(p, "C"))

    def test_parse_retains_position_info(self) -> None:
        tokens = [
            Token(PosInfo(1, 1, 1), "A"),
            Token(PosInfo(1, 3, 3), "and"),
            Token(PosInfo(1, 7, 1), "("),
            Token(PosInfo(1, 8, 1), "B"),
            Token(PosInfo(1, 10, 2), "or"),
            Token(PosInfo(1, 13, 1), "C"),
            Token(PosInfo(1, 14, 1), ")"),
        ]
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(
            PosInfo(1, 3, 3),
            BinaryOpKind.AND,
            Var(PosInfo(1, 1, 1), "A"),
            BinaryOp(PosInfo(1, 10, 2), BinaryOpKind.OR, Var(PosInfo(1, 8, 1), "B"), Var(PosInfo(1, 13, 1), "C")),
        )

    def test_parse_missing_right_paren_retains_position_info(self) -> None:
        tokens = [
            Token(PosInfo(1, 1, 1), "("),
            Token(PosInfo(1, 2, 1), "A"),
        ]
        with pytest.raises(ParseError, match=re.escape("Expected token ) at line 1, char 2")):
            Parser(tokens).parse()

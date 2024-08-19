import re

import pytest
from markers import Parser
from markers.error import ParseError
from markers.expressions import BinaryOp, BinaryOpKind, Lit, UnaryOp, UnaryOpKind, Var
from markers.tokens import (
    AndOperatorToken,
    LeftParenToken,
    LitToken,
    NameToken,
    NotOperatorToken,
    OrOperatorToken,
    RightParenToken,
    Token,
)
from markers.type import PositionInfo


class TestParser:
    def test_parse_var(self) -> None:
        tokens = [NameToken("A")]
        expr = Parser(tokens).parse()
        assert expr == Var("A")

    def test_parse_not(self) -> None:
        tokens = [NotOperatorToken(), NameToken("A")]
        expr = Parser(tokens).parse()
        assert expr == UnaryOp(UnaryOpKind.NOT, Var("A"))

    def test_parse_and(self) -> None:
        tokens = [NameToken("A"), AndOperatorToken(), NameToken("B")]
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(BinaryOpKind.AND, Var("A"), Var("B"))

    def test_parse_or(self) -> None:
        tokens = [NameToken("A"), OrOperatorToken(), NameToken("B")]
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(BinaryOpKind.OR, Var("A"), Var("B"))

    def test_parse_parentheses(self) -> None:
        tokens = [
            NameToken("A"),
            AndOperatorToken(),
            LeftParenToken(),
            NameToken("B"),
            OrOperatorToken(),
            NameToken("C"),
            RightParenToken(),
        ]
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(BinaryOpKind.AND, Var("A"), BinaryOp(BinaryOpKind.OR, Var("B"), Var("C")))

    def test_parse_and_binds_tighter_than_or(self) -> None:
        tokens = [NameToken("A"), AndOperatorToken(), NameToken("B"), OrOperatorToken(), NameToken("C")]
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(BinaryOpKind.OR, BinaryOp(BinaryOpKind.AND, Var("A"), Var("B")), Var("C"))

    def test_parse_double_negation(self) -> None:
        tokens = [NotOperatorToken(), NotOperatorToken(), NameToken("A")]
        expr = Parser(tokens).parse()
        assert expr == UnaryOp(UnaryOpKind.NOT, UnaryOp(UnaryOpKind.NOT, Var("A")))

    def test_parse_negation_of_parentheses(self) -> None:
        tokens = [
            NotOperatorToken(),
            LeftParenToken(),
            NameToken("A"),
            OrOperatorToken(),
            NameToken("B"),
            RightParenToken(),
        ]
        expr = Parser(tokens).parse()
        assert expr == UnaryOp(UnaryOpKind.NOT, BinaryOp(BinaryOpKind.OR, Var("A"), Var("B")))

    def test_parse_missing_right_paren_raises_parse_error(self) -> None:
        tokens = [LeftParenToken(), NameToken("A"), OrOperatorToken(), NameToken("B")]
        with pytest.raises(ParseError, match=re.escape("Expected token ) at line 0, char 0")):
            Parser(tokens).parse()

    def test_parse_missing_left_paren_raises_parse_error(self) -> None:
        tokens = [NameToken("A"), OrOperatorToken(), NameToken("B"), RightParenToken()]
        with pytest.raises(ParseError, match=re.escape('Unexpected token ")" at line 0, char 0')):
            Parser(tokens).parse()

    def test_parse_empty_input_raises_parse_error(self) -> None:
        tokens: list[Token] = []
        with pytest.raises(ParseError, match=re.escape("Unexpected end of input")):
            Parser(tokens).parse()

    def test_incomplete_and_raises_parse_error(self) -> None:
        tokens = [NameToken("A"), AndOperatorToken()]
        with pytest.raises(ParseError, match=re.escape("Unexpected end of input")):
            Parser(tokens).parse()

    def test_parse_true(self) -> None:
        tokens = [LitToken(True)]
        expr = Parser(tokens).parse()
        assert expr == Lit(True)

    def test_parse_false(self) -> None:
        tokens = [LitToken(False)]
        expr = Parser(tokens).parse()
        assert expr == Lit(False)

    def test_parse_invalid_var_raises_parse_error(self) -> None:
        tokens = [NameToken("A"), OrOperatorToken(), NameToken("0_invalid")]
        with pytest.raises(ParseError, match=re.escape('Unexpected token "0_invalid" at line 0, char 0')):
            Parser(tokens).parse()

    def test_parse_repeated_and(self) -> None:
        tokens = [NameToken("A"), AndOperatorToken(), NameToken("B"), AndOperatorToken(), NameToken("C")]
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(BinaryOpKind.AND, BinaryOp(BinaryOpKind.AND, Var("A"), Var("B")), Var("C"))

    def test_parse_repeated_or(self) -> None:
        tokens = [NameToken("A"), OrOperatorToken(), NameToken("B"), OrOperatorToken(), NameToken("C")]
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(BinaryOpKind.OR, BinaryOp(BinaryOpKind.OR, Var("A"), Var("B")), Var("C"))

    def test_parse_retains_position_info(self) -> None:
        tokens = [
            NameToken("A", pos=PositionInfo(1, 1, 1)),
            AndOperatorToken(pos=PositionInfo(1, 3, 3)),
            LeftParenToken(pos=PositionInfo(1, 7, 1)),
            NameToken("B", pos=PositionInfo(1, 8, 1)),
            OrOperatorToken(pos=PositionInfo(1, 10, 2)),
            NameToken("C", pos=PositionInfo(1, 13, 1)),
            RightParenToken(pos=PositionInfo(1, 14, 1)),
        ]
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(
            BinaryOpKind.AND,
            Var("A", pos=PositionInfo(1, 1, 1)),
            BinaryOp(
                BinaryOpKind.OR,
                Var("B", pos=PositionInfo(1, 8, 1)),
                Var("C", pos=PositionInfo(1, 13, 1)),
                pos=PositionInfo(1, 10, 2),
            ),
            pos=PositionInfo(1, 3, 3),
        )

    def test_parse_missing_right_paren_retains_position_info(self) -> None:
        tokens = [
            LeftParenToken(pos=PositionInfo(1, 1, 1)),
            NameToken("A", pos=PositionInfo(1, 2, 1)),
        ]
        with pytest.raises(ParseError, match=re.escape("Expected token ) at line 1, char 2")):
            Parser(tokens).parse()

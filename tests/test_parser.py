import re

import pytest
from markers import Parser
from markers.error import ParseError
from markers.expressions import BinaryOp, BinaryOpKind, Lit, UnaryOp, UnaryOpKind, Var
from markers.tokens import (
    AndOpToken,
    LeftParenToken,
    LitToken,
    NameToken,
    NotOpToken,
    OrOpToken,
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
        tokens = [NotOpToken(), NameToken("A")]
        expr = Parser(tokens).parse()
        assert expr == UnaryOp(UnaryOpKind.NOT, Var("A"))

    def test_parse_and(self) -> None:
        tokens = [NameToken("A"), AndOpToken(), NameToken("B")]
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(BinaryOpKind.AND, Var("A"), Var("B"))

    def test_parse_or(self) -> None:
        tokens = [NameToken("A"), OrOpToken(), NameToken("B")]
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(BinaryOpKind.OR, Var("A"), Var("B"))

    def test_parse_parentheses(self) -> None:
        tokens = [
            NameToken("A"),
            AndOpToken(),
            LeftParenToken(),
            NameToken("B"),
            OrOpToken(),
            NameToken("C"),
            RightParenToken(),
        ]
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(BinaryOpKind.AND, Var("A"), BinaryOp(BinaryOpKind.OR, Var("B"), Var("C")))

    def test_parse_and_binds_tighter_than_or(self) -> None:
        tokens = [NameToken("A"), AndOpToken(), NameToken("B"), OrOpToken(), NameToken("C")]
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(BinaryOpKind.OR, BinaryOp(BinaryOpKind.AND, Var("A"), Var("B")), Var("C"))

    def test_parse_double_negation(self) -> None:
        tokens = [NotOpToken(), NotOpToken(), NameToken("A")]
        expr = Parser(tokens).parse()
        assert expr == UnaryOp(UnaryOpKind.NOT, UnaryOp(UnaryOpKind.NOT, Var("A")))

    def test_parse_negation_of_parentheses(self) -> None:
        tokens = [
            NotOpToken(),
            LeftParenToken(),
            NameToken("A"),
            OrOpToken(),
            NameToken("B"),
            RightParenToken(),
        ]
        expr = Parser(tokens).parse()
        assert expr == UnaryOp(UnaryOpKind.NOT, BinaryOp(BinaryOpKind.OR, Var("A"), Var("B")))

    def test_parse_missing_right_paren_raises_parse_error(self) -> None:
        tokens = [LeftParenToken(), NameToken("A"), OrOpToken(), NameToken("B")]
        with pytest.raises(ParseError, match=re.escape("Expected closing paren matching opening")) as exc:
            Parser(tokens).parse()
        assert exc.value.pos == PositionInfo(0, 0, 0)

    def test_parse_missing_left_paren_raises_parse_error(self) -> None:
        tokens = [NameToken("A"), OrOpToken(), NameToken("B"), RightParenToken()]
        with pytest.raises(ParseError, match=re.escape('Unexpected token ")"')) as exc:
            Parser(tokens).parse()
        assert exc.value.pos == PositionInfo(0, 0, 0)

    def test_parse_empty_input_raises_parse_error(self) -> None:
        tokens: list[Token] = []
        with pytest.raises(ParseError, match=re.escape("Unexpected end of input")):
            Parser(tokens).parse()

    def test_incomplete_and_raises_parse_error(self) -> None:
        tokens = [NameToken("A"), AndOpToken()]
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
        # Testing expression: "A or 0_invalid"
        tokens = [
            NameToken("A", pos=PositionInfo(1, 1, 1)),
            OrOpToken(pos=PositionInfo(1, 3, 2)),
            NameToken("0_invalid", pos=PositionInfo(1, 6, 9)),
        ]
        with pytest.raises(ParseError, match=re.escape('Unexpected token "0_invalid"')) as exc:
            Parser(tokens).parse()
        assert exc.value.pos == PositionInfo(1, 6, 9)

    def test_parse_repeated_and(self) -> None:
        tokens = [NameToken("A"), AndOpToken(), NameToken("B"), AndOpToken(), NameToken("C")]
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(BinaryOpKind.AND, BinaryOp(BinaryOpKind.AND, Var("A"), Var("B")), Var("C"))

    def test_parse_repeated_or(self) -> None:
        tokens = [NameToken("A"), OrOpToken(), NameToken("B"), OrOpToken(), NameToken("C")]
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(BinaryOpKind.OR, BinaryOp(BinaryOpKind.OR, Var("A"), Var("B")), Var("C"))

    def test_parse_expression_after_right_paren(self) -> None:
        tokens = [
            LeftParenToken(),
            NameToken("A"),
            RightParenToken(),
            OrOpToken(),
            NameToken("B"),
        ]
        expr = Parser(tokens).parse()
        assert expr == BinaryOp(BinaryOpKind.OR, Var("A"), Var("B"))

    def test_parse_retains_position_info(self) -> None:
        # Testing expression: "A and (B or C)"
        tokens = [
            NameToken("A", pos=PositionInfo(1, 1, 1)),
            AndOpToken(pos=PositionInfo(1, 3, 3)),
            LeftParenToken(pos=PositionInfo(1, 7, 1)),
            NameToken("B", pos=PositionInfo(1, 8, 1)),
            OrOpToken(pos=PositionInfo(1, 10, 2)),
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
        # Testing expression: "not (A"
        tokens = [
            NotOpToken(pos=PositionInfo(1, 1, 1)),
            LeftParenToken(pos=PositionInfo(1, 5, 1)),
            NameToken("A", pos=PositionInfo(1, 6, 1)),
        ]
        with pytest.raises(ParseError, match=re.escape("Expected closing paren matching opening")) as exc:
            Parser(tokens).parse()
        assert exc.value.pos == PositionInfo(1, 5, 1)

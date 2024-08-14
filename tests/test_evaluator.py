import pytest
from markers import Evaluator
from markers.type import BinaryOp, BinaryOpKind, Lit, UnaryOp, UnaryOpKind, Var


class TestEvaluator:
    def test_evaluate_var_returns_true(self) -> None:
        expr = Var("A")
        true_vars = ["A"]
        result = Evaluator().evaluate(expr, true_vars)
        assert result

    def test_evaluate_var_returns_false(self) -> None:
        expr = Var("A")
        true_vars = ["B"]
        result = Evaluator().evaluate(expr, true_vars)
        assert not result

    def test_evaluate_not_returns_false(self) -> None:
        expr = UnaryOp(UnaryOpKind.NOT, Var("A"))
        true_vars = ["A"]
        result = Evaluator().evaluate(expr, true_vars)
        assert not result

    def test_evaluate_not_returns_true(self) -> None:
        expr = UnaryOp(UnaryOpKind.NOT, Var("A"))
        true_vars = ["B"]
        result = Evaluator().evaluate(expr, true_vars)
        assert result

    def test_evaluate_and_returns_true(self) -> None:
        expr = BinaryOp(BinaryOpKind.AND, Var("A"), Var("B"))
        true_vars = ["A", "B"]
        result = Evaluator().evaluate(expr, true_vars)
        assert result

    def test_evaluate_and_returns_false(self) -> None:
        expr = BinaryOp(BinaryOpKind.AND, Var("A"), Var("B"))
        true_vars = ["A"]
        result = Evaluator().evaluate(expr, true_vars)
        assert not result

    def test_evaluate_or_returns_true(self) -> None:
        expr = BinaryOp(BinaryOpKind.OR, Var("A"), Var("B"))
        true_vars = ["A"]
        result = Evaluator().evaluate(expr, true_vars)
        assert result

    def test_evaluate_or_returns_false(self) -> None:
        expr = BinaryOp(BinaryOpKind.OR, Var("A"), Var("B"))
        true_vars = ["C"]
        result = Evaluator().evaluate(expr, true_vars)
        assert not result

    def test_evaluate_bool_literal_true(self) -> None:
        expr = BinaryOp(BinaryOpKind.OR, Lit(True), Var("B"))
        true_vars = ["A"]
        result = Evaluator().evaluate(expr, true_vars)
        assert result

    def test_evaluate_bool_literal_false(self) -> None:
        expr = BinaryOp(BinaryOpKind.AND, Lit(False), Var("B"))
        true_vars = ["A"]
        result = Evaluator().evaluate(expr, true_vars)
        assert not result

    def test_evaluate_false_vars(self) -> None:
        expr = Var("A")
        true_vars = ["B"]
        false_vars = ["A"]
        result = Evaluator().evaluate(expr, true_vars, false_vars)
        assert not result

    def test_evaluate_unknown_variable_name(self) -> None:
        expr = Var("A")
        true_vars = ["B"]
        false_vars = ["C"]
        with pytest.raises(ValueError, match="Unknown variable: A"):
            Evaluator().evaluate(expr, true_vars, false_vars)

    def test_evaluate_variable_both_true_and_false(self) -> None:
        expr = Var("A")
        true_vars = ["A"]
        false_vars = ["A"]
        with pytest.raises(ValueError, match="Variable cannot be both true and false: A"):
            Evaluator().evaluate(expr, true_vars, false_vars)

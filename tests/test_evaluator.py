import pytest
from markers import Evaluator
from markers.type import BinaryOp, BinaryOpKind, Env, Lit, UnaryOp, UnaryOpKind, Var


class TestEvaluator:
    def test_evaluate_lit_true(self) -> None:
        expr = Lit(True)
        env: Env = {}
        result = Evaluator().evaluate(expr, env)
        assert result

    def test_evaluate_lit_false(self) -> None:
        expr = Lit(False)
        env: Env = {}
        result = Evaluator().evaluate(expr, env)
        assert not result

    def test_evaluate_var_returns_env_value_true(self) -> None:
        expr = Var("A")
        env: Env = {"A": True}
        result = Evaluator().evaluate(expr, env)
        assert result

    def test_evaluate_var_returns_env_value_false(self) -> None:
        expr = Var("A")
        env: Env = {"A": False}
        result = Evaluator().evaluate(expr, env)
        assert not result

    def test_evaluate_var_raises_unknown_variable_name(self) -> None:
        expr = Var("A")
        env: Env = {"B": True, "C": False}
        with pytest.raises(ValueError, match="Unknown variable: A"):
            Evaluator().evaluate(expr, env)

    def test_evaluate_not_returns_negation_true(self) -> None:
        expr = UnaryOp(UnaryOpKind.NOT, Var("A"))
        env: Env = {"A": False}
        result = Evaluator().evaluate(expr, env)
        assert result

    def test_evaluate_not_returns_negation_false(self) -> None:
        expr = UnaryOp(UnaryOpKind.NOT, Var("A"))
        env: Env = {"A": True}
        result = Evaluator().evaluate(expr, env)
        assert not result

    def test_evaluate_and_returns_true(self) -> None:
        expr = BinaryOp(BinaryOpKind.AND, Var("A"), Var("B"))
        env: Env = {"A": True, "B": True}
        result = Evaluator().evaluate(expr, env)
        assert result

    def test_evaluate_and_returns_false(self) -> None:
        expr = BinaryOp(BinaryOpKind.AND, Var("A"), Var("B"))
        env: Env = {"A": True, "B": False}
        result = Evaluator().evaluate(expr, env)
        assert not result

    def test_evaluate_or_returns_true(self) -> None:
        expr = BinaryOp(BinaryOpKind.OR, Var("A"), Var("B"))
        env: Env = {"A": True, "B": False}
        result = Evaluator().evaluate(expr, env)
        assert result

    def test_evaluate_or_returns_false(self) -> None:
        expr = BinaryOp(BinaryOpKind.OR, Var("A"), Var("B"))
        env: Env = {"A": False, "B": False, "C": True}
        result = Evaluator().evaluate(expr, env)
        assert not result

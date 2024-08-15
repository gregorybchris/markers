import pytest
from markers import Evaluator
from markers.error import EvaluateError
from markers.type import BinaryOp, BinaryOpKind, Env, Lit, PosInfo, UnaryOp, UnaryOpKind, Var

p = PosInfo(0, 0, 0)


class TestEvaluator:
    def test_evaluate_lit_true(self) -> None:
        expr = Lit(p, True)
        env: Env = {}
        result = Evaluator().evaluate(expr, env)
        assert result

    def test_evaluate_lit_false(self) -> None:
        expr = Lit(p, False)
        env: Env = {}
        result = Evaluator().evaluate(expr, env)
        assert not result

    def test_evaluate_var_returns_env_value_true(self) -> None:
        expr = Var(p, "A")
        env: Env = {"A": True}
        result = Evaluator().evaluate(expr, env)
        assert result

    def test_evaluate_var_returns_env_value_false(self) -> None:
        expr = Var(p, "A")
        env: Env = {"A": False}
        result = Evaluator().evaluate(expr, env)
        assert not result

    def test_evaluate_with_unknown_variable_raises_evaluate_error(self) -> None:
        expr = Var(p, "A")
        env: Env = {"B": True, "C": False}
        with pytest.raises(EvaluateError, match='Unknown variable: "A" at line 0, char 0'):
            Evaluator().evaluate(expr, env)

    def test_evaluate_not_returns_negation_true(self) -> None:
        expr = UnaryOp(p, UnaryOpKind.NOT, Var(p, "A"))
        env: Env = {"A": False}
        result = Evaluator().evaluate(expr, env)
        assert result

    def test_evaluate_not_returns_negation_false(self) -> None:
        expr = UnaryOp(p, UnaryOpKind.NOT, Var(p, "A"))
        env: Env = {"A": True}
        result = Evaluator().evaluate(expr, env)
        assert not result

    def test_evaluate_and_returns_true(self) -> None:
        expr = BinaryOp(p, BinaryOpKind.AND, Var(p, "A"), Var(p, "B"))
        env: Env = {"A": True, "B": True}
        result = Evaluator().evaluate(expr, env)
        assert result

    def test_evaluate_and_returns_false(self) -> None:
        expr = BinaryOp(p, BinaryOpKind.AND, Var(p, "A"), Var(p, "B"))
        env: Env = {"A": True, "B": False}
        result = Evaluator().evaluate(expr, env)
        assert not result

    def test_evaluate_or_returns_true(self) -> None:
        expr = BinaryOp(p, BinaryOpKind.OR, Var(p, "A"), Var(p, "B"))
        env: Env = {"A": True, "B": False}
        result = Evaluator().evaluate(expr, env)
        assert result

    def test_evaluate_or_returns_false(self) -> None:
        expr = BinaryOp(p, BinaryOpKind.OR, Var(p, "A"), Var(p, "B"))
        env: Env = {"A": False, "B": False, "C": True}
        result = Evaluator().evaluate(expr, env)
        assert not result

    def test_evaluate_retains_position_information(self) -> None:
        expr = BinaryOp(
            PosInfo(2, 1, 2),
            BinaryOpKind.OR,
            BinaryOp(PosInfo(1, 3, 3), BinaryOpKind.AND, Var(PosInfo(1, 1, 1), "A"), Var(PosInfo(1, 7, 1), "B")),
            Var(PosInfo(2, 4, 1), "C"),
        )
        env: Env = {"A": True, "B": False}
        with pytest.raises(EvaluateError, match='Unknown variable: "C" at line 2, char 4'):
            Evaluator().evaluate(expr, env)

from dataclasses import dataclass

from markers.types import BinaryOp, BinaryOpKind, Expr, Lit, UnaryOp, UnaryOpKind, Var, VarName


@dataclass
class Evaluator:
    """Boolean expression evaluator."""

    def evaluate(self, expr: Expr, true_vars: list[VarName]) -> bool:
        """Evaluate the boolean expression.

        Args:
            expr (Expr): The AST expression node to evaluate.
            true_vars (list[VarName]): The list of variable names that are known to be true.
                Other variables are assumed to be false.

        Raises:
            ValueError: If the expression is invalid.

        Returns:
            bool: Whether the expression evaluates to true.
        """
        match expr:
            case Lit(val):
                return val
            case Var(name):
                return name in true_vars
            case UnaryOp(UnaryOpKind.NOT, arg):
                return not self.evaluate(arg, true_vars)
            case BinaryOp(BinaryOpKind.AND, left, right):
                return self.evaluate(left, true_vars) and self.evaluate(right, true_vars)
            case BinaryOp(BinaryOpKind.OR, left, right):
                return self.evaluate(left, true_vars) or self.evaluate(right, true_vars)
            case _:
                msg = "Invalid expression"
                raise ValueError(msg)

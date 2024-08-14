from dataclasses import dataclass
from typing import Optional

from markers.types import BinaryOp, BinaryOpKind, Expr, Lit, UnaryOp, UnaryOpKind, Var, VarName


@dataclass
class Evaluator:
    """Boolean expression evaluator."""

    def evaluate(self, expr: Expr, true_vars: list[VarName], false_vars: Optional[list[VarName]] = None) -> bool:
        """Evaluate the boolean expression.

        Args:
            expr (Expr): The AST expression node to evaluate.
            true_vars (list[VarName]): The list of variable names that are known to be true.
                Other variables are assumed to be false unless specified in `false_vars`.
            false_vars (Optional[list[VarName]]): The list of variable names that are known to be false.
                If provided, unknown variables will raise an error.

        Raises:
            ValueError: If the expression is invalid.
            ValueError: If a variable is both true and false.
            ValueError: If an unknown variable is evaluated and `false_vars` is provided.

        Returns:
            bool: Whether the expression evaluates to true.
        """
        if false_vars is not None:
            for name in true_vars:
                if name in false_vars:
                    msg = f"Variable cannot be both true and false: {name}"
                    raise ValueError(msg)

        match expr:
            case Lit(val):
                return val
            case Var(name):
                if false_vars is not None:
                    if name in false_vars:
                        return False
                    if name not in true_vars:
                        msg = f"Unknown variable: {name}"
                        raise ValueError(msg)
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

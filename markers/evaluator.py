from dataclasses import dataclass

from markers.error import EvaluateError, InternalError
from markers.type import BinaryOp, BinaryOpKind, Env, Expr, Lit, UnaryOp, UnaryOpKind, Var


@dataclass
class Evaluator:
    """Boolean expression evaluator."""

    def evaluate(self, expr: Expr, env: Env) -> bool:
        """Evaluate the boolean expression.

        Args:
            expr (Expr): The AST expression node to evaluate.
            env (Env): The environment with variable assignments.

        Raises:
            EvaluateError: If a variable is unknown.
            InternalError: If the expression is invalid.

        Returns:
            bool: Whether the expression evaluates to true.
        """
        match expr:
            case Lit(val):
                return val
            case Var(name, pos=pos):
                if name not in env:
                    msg = f'Unknown variable: "{name}" at line {pos.line_no}, char {pos.char_no}'
                    raise EvaluateError(msg, pos)
                return env[name]
            case UnaryOp(UnaryOpKind.NOT, arg):
                return not self.evaluate(arg, env)
            case BinaryOp(BinaryOpKind.AND, left, right):
                return self.evaluate(left, env) and self.evaluate(right, env)
            case BinaryOp(BinaryOpKind.OR, left, right):
                return self.evaluate(left, env) or self.evaluate(right, env)
            case other:
                msg = f"Evaluate is not implement for expression type: {type(other)}"
                raise InternalError(msg)

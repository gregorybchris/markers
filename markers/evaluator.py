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
            SyntaxError: If a variable is unknown.
            InternalError: If the expression is invalid.

        Returns:
            bool: Whether the expression evaluates to true.
        """
        match expr:
            case Lit(_, val):
                return val
            case Var(pos_info, name):
                if name not in env:
                    msg = f'Unknown variable: "{name}" at line {pos_info.line_no}, char {pos_info.char_no}'
                    raise EvaluateError(msg, pos_info)
                return env[name]
            case UnaryOp(_, UnaryOpKind.NOT, arg):
                return not self.evaluate(arg, env)
            case BinaryOp(_, BinaryOpKind.AND, left, right):
                return self.evaluate(left, env) and self.evaluate(right, env)
            case BinaryOp(_, BinaryOpKind.OR, left, right):
                return self.evaluate(left, env) or self.evaluate(right, env)
            case other:
                msg = f"Evaluate is not implement for expression type: {type(other)}"
                raise InternalError(msg)

from rich.pretty import pprint

from markers.evaluator import Evaluator
from markers.parser import Parser
from markers.tokenizer import Tokenizer


def run() -> None:
    """Run an example of parsing and evaluating a boolean formula."""
    boolean_formula = "not A"
    print("Input formula: ", boolean_formula)
    print()

    tokenizer = Tokenizer(boolean_formula)
    tokens = tokenizer.tokenize()
    print("Tokens: ", tokens)
    print()

    parser = Parser(tokens)
    expr = parser.parse()
    pprint(expr)
    print()
    print(expr)
    print()

    env = {"A": True, "C": True}
    print("Environment: ", env)
    print()

    evaluator = Evaluator()
    result = evaluator.evaluate(expr, env)
    print("Result: ", result)


if __name__ == "__main__":
    run()

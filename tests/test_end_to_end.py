from markers import Evaluator, Parser, Tokenizer


class TestEndToEnd:
    def test_end_to_end(self) -> None:
        boolean_formula = "A and (not B or C)"
        tokenizer = Tokenizer(boolean_formula)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        expr = parser.parse()
        env = {"A": True, "B": True, "C": False}
        evaluator = Evaluator()
        result = evaluator.evaluate(expr, env)
        assert not result

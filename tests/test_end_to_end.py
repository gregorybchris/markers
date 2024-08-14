from markers import Evaluator, Parser, Tokenizer


class TestEndToEnd:
    def test_large_input(self) -> None:
        boolean_formula = "A and (not B or D)"
        tokenizer = Tokenizer(boolean_formula)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        expr = parser.parse()
        env = {"A": True, "C": True}
        evaluator = Evaluator()
        result = evaluator.evaluate(expr, env)
        assert result

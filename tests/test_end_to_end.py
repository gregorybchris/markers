from markers import Evaluator, Parser, Tokenizer


class TestEndToEnd:
    def test_end_to_end(self) -> None:
        program = "A and (not B or C)"
        tokenizer = Tokenizer(program)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        expr = parser.parse()
        env = {"A": True, "B": True, "C": False}
        evaluator = Evaluator()
        result = evaluator.evaluate(expr, env)
        assert not result

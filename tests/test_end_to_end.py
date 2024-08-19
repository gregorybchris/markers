from markers import Evaluator, Lexer, Parser


class TestEndToEnd:
    def test_end_to_end(self) -> None:
        program = "A and (not B or C)"
        tokens = Lexer.tokenize(program)
        expr = Parser(tokens).parse()
        env = {"A": True, "B": True, "C": False}
        result = Evaluator().evaluate(expr, env)
        assert not result

import pytest
from click.testing import CliRunner
from markers.cli import main


@pytest.fixture(scope="session", name="cli_runner")
def cli_runner_fixture() -> CliRunner:
    return CliRunner()


class TestCli:
    def test_parse(self, cli_runner: CliRunner) -> None:
        result = cli_runner.invoke(main, ["parse", "a and b"])
        assert result.exit_code == 0
        expected = """BinaryOp(
│   pos_info=PosInfo(line_no=1, char_no=3, length=3),
│   kind=<BinaryOpKind.AND: 'and'>,
│   left=Var(pos_info=PosInfo(line_no=1, char_no=1, length=1), name='a'),
│   right=Var(pos_info=PosInfo(line_no=1, char_no=7, length=1), name='b')
)
"""
        assert result.output == expected

    def test_eval(self, cli_runner: CliRunner) -> None:
        result = cli_runner.invoke(main, ["eval", "a and b or d", "-t", "a", "-t", "b", "-f", "d"])
        assert result.exit_code == 0
        assert result.output == "True\n"

    def test_eval_error(self, cli_runner: CliRunner) -> None:
        result = cli_runner.invoke(main, ["eval", "alice and bob and chris", "-t", "alice", "-t", "bob"])
        assert result.exit_code == 0
        expected = """EvaluateError: Unknown variable: "chris" at line 1, char 19

alice and bob and chris
------------------^^^^^
"""
        assert result.output == expected

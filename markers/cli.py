import logging

import click
from rich.pretty import pprint

from markers.error import error_context
from markers.evaluator import Evaluator
from markers.lexer import Lexer
from markers.parser import Parser


@click.group()
def main() -> None:
    """Run main CLI entrypoint."""


def set_logger_config(info: bool, debug: bool) -> None:
    """Set the logger configuration."""
    if info:
        logging.basicConfig(level=logging.INFO)
    if debug:
        logging.basicConfig(level=logging.DEBUG)


@main.command(name="parse")
@click.argument("program")
@click.option("--pretty", is_flag=True)
@click.option("--info", is_flag=True)
@click.option("--debug", is_flag=True)
def parse_command(
    program: str,
    pretty: bool = False,
    info: bool = False,
    debug: bool = False,
) -> None:
    """Run the CLI."""
    set_logger_config(info, debug)

    with error_context(program):
        tokens = Lexer.tokenize(program)
        expr = Parser(tokens).parse()

        if pretty:
            print(str(expr))
        else:
            pprint(expr)


@main.command(name="eval")
@click.argument("program")
@click.option("--true-vars", "-t", multiple=True)
@click.option("--false-vars", "-f", multiple=True)
@click.option("--info", is_flag=True)
@click.option("--debug", is_flag=True)
def eval_command(
    program: str,
    true_vars: tuple[str],
    false_vars: tuple[str],
    info: bool = False,
    debug: bool = False,
) -> None:
    """Run the CLI."""
    set_logger_config(info, debug)

    with error_context(program):
        env = {**dict.fromkeys(true_vars, True), **dict.fromkeys(false_vars, False)}
        tokens = Lexer.tokenize(program)
        expr = Parser(tokens).parse()
        result = Evaluator().evaluate(expr, env)
        print(result)

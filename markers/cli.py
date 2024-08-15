import logging

import click
from rich.pretty import pprint

from markers.error import error_context
from markers.evaluator import Evaluator
from markers.parser import Parser
from markers.tokenizer import Tokenizer


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
@click.argument("formula")
@click.option("--pretty", is_flag=True)
@click.option("--info", is_flag=True)
@click.option("--debug", is_flag=True)
def parse_command(
    formula: str,
    pretty: bool = False,
    info: bool = False,
    debug: bool = False,
) -> None:
    """Run the CLI."""
    set_logger_config(info, debug)

    with error_context(formula):
        tokens = Tokenizer(formula).tokenize()
        expr = Parser(tokens).parse()

        if pretty:
            print(str(expr))
        else:
            pprint(expr)


@main.command(name="eval")
@click.argument("formula")
@click.option("--true-vars", "-t", multiple=True)
@click.option("--false-vars", "-f", multiple=True)
@click.option("--info", is_flag=True)
@click.option("--debug", is_flag=True)
def eval_command(
    formula: str,
    true_vars: tuple[str],
    false_vars: tuple[str],
    info: bool = False,
    debug: bool = False,
) -> None:
    """Run the CLI."""
    set_logger_config(info, debug)

    with error_context(formula):
        env = {**dict.fromkeys(true_vars, True), **dict.fromkeys(false_vars, False)}
        tokens = Tokenizer(formula).tokenize()
        expr = Parser(tokens).parse()
        result = Evaluator().evaluate(expr, env)
        print(result)

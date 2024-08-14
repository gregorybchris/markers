import logging
from typing import Optional

import click
from rich.pretty import pprint

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
@click.option("--info", is_flag=True)
@click.option("--debug", is_flag=True)
def parse_command(
    formula: str,
    info: bool = False,
    debug: bool = False,
) -> None:
    """Run the CLI."""
    set_logger_config(info, debug)

    tokens = Tokenizer(formula).tokenize()
    expr = Parser(tokens).parse()
    pprint(expr)


@main.command(name="eval")
@click.argument("formula")
@click.option("--true-vars", "-t", multiple=True, required=True)
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

    true_vars_list = list(true_vars)
    false_vars_list: Optional[list[str]] = list(false_vars)

    if false_vars_list is not None and len(false_vars_list) == 0:
        false_vars_list = None

    print(true_vars_list)
    print(false_vars_list)

    tokens = Tokenizer(formula).tokenize()
    expr = Parser(tokens).parse()
    result = Evaluator().evaluate(expr, true_vars_list, true_vars_list)
    print(result)

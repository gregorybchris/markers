<div align="center">
  <h1>Markers</h1>

  <p>
    <strong>Simple parser for boolean formulas</strong>
  </p>
</div>

## About

Markers is a parser for boolean formulas. You can provide it an expression like `a and not (b or c)` as well as variable assignments like `a = true, b = false, c = true` and Markers will evaluate `true and not (false or true)` => `false`.

Supported tokens are variables, `and`, `or`, `not`, and parentheses.

If you care about the parse tree and not the evaluation on a set of variable assignments you can also use Markers to just parse an expression and emit a recursive Python structure of boolean operators and variables.

## Installation

[Poetry](https://python-poetry.org/) is a requirement

```bash
poetry install
```

## CLI usage

### Parsing a boolean formula

```bash
$ poetry run markers parse "not a or b"
> BinaryOp(
>     kind=BinaryOpKind.OR,
>     left=UnaryOp(
>         kind=UnaryOpKind.NOT,
>         arg=Var(name='a')
>     ),
>     right=Var(name='b')
> )
```

### Evaluating a boolean formula with variable assignments

```bash
$ poetry run markers eval "not a or b" -t b -f a
> True
```

## Running tests

```bash
pytest tests
```

## Motivation

I started working on Markers when I realized that [pytest](https://docs.pytest.org) doesn't expose the internals of its [marks](https://docs.pytest.org/en/stable/reference/reference.html#custom-marks) feature to plugins. You can hook into the results of evaluating the boolean formula, but not the unevaluated parse tree. Markers per function or class can be accessed on `TestItem` objects, for example through the `handle_test_completion` hook.

The name "Markers" is a nod to the fact that pytest is inconsistent with its use of "mark" and "marker".

## Acknowledgements

This project borrowed heavily from some online resources and human minds about parsing in general and boolean formula parsing in particular.

- [Eoin Davey's Blog](https://vey.ie/2018/10/04/RecursiveDescent.html)
- [Scrapscript Interpreter](https://github.com/tekknolagi/scrapscript)
- [Typped Pratt Parsing](https://abarker.github.io/typped/pratt_parsing_intro.html)
- [Max Bernstein](https://bernsteinbear.com)

# Markers

Boolean formula parsing

## Installation

[Poetry](https://python-poetry.org/) is a requirement

```bash
poetry install
```

## CLI

```bash
# Parse
markers parse "not a or b"

# Eval
markers eval "not a or b" -t b -f a
```

## Run tests

```bash
pytest tests
```

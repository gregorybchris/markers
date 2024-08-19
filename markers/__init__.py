import importlib.metadata

from markers.evaluator import Evaluator
from markers.lexer import Lexer
from markers.parser import Parser

__version__ = importlib.metadata.version("markers")

__all__ = [
    "Evaluator",
    "Lexer",
    "Parser",
    "__version__",
]

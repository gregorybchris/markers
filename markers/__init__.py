import importlib.metadata

from markers.evaluator import Evaluator
from markers.parser import Parser
from markers.tokenizer import Tokenizer

__version__ = importlib.metadata.version("markers")

__all__ = [
    "__version__",
    "Evaluator",
    "Parser",
    "Tokenizer",
]

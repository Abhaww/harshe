"""
Harshe - The Hausa Programming Language
Babban shirin Harshe - Harshen Shirye-shiryen Kwamfuta a Yaren Hausa.
"""

__version__ = "1.0.0"
__author__ = "Antigravity Pair Programmer"

from .tokens import Token, TokenType, Position
from .lexer import Lexer
from .ast_nodes import ASTNode, Program
from .parser import Parser
from .environment import Environment
from .interpreter import Interpreter
from .values import HarsheValue, to_harshe_value, to_python_value
from .errors import HarsheError
from .repl import start_repl


def run_source(source: str, filename: str = "<shigarwa>", env: Environment = None) -> HarsheValue:
    """Gudanar da rubutun Harshe kai-tsaye daga string"""
    lexer = Lexer(source, filename)
    tokens = lexer.tokenize()
    parser = Parser(tokens, source)
    ast = parser.parse()
    interpreter = Interpreter(global_env=env, source_code=source, current_file=filename)
    return interpreter.interpret(ast)


def run_file(filepath: str) -> HarsheValue:
    """Gudanar da fayil din Harshe (.hausa)"""
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()
    return run_source(source, filepath)

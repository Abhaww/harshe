"""
Harshe - Tsarin Bishiyar Nahawu (AST - Abstract Syntax Tree Nodes)
Bishiyar nahawu da take wakiltar kowane bangare na tsarin rubutun Harshe.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Any
from .tokens import Token, Position


@dataclass(kw_only=True)
class ASTNode:
    """Tushen dukkan bishiyar nahawu (Base AST Node)"""
    start_pos: Optional[Position] = None
    end_pos: Optional[Position] = None


# ==========================================
# SANARWA DA JUMLE-JUMLE (Statements)
# ==========================================

@dataclass(kw_only=True)
class Statement(ASTNode):
    pass


@dataclass(kw_only=True)
class Program(ASTNode):
    """Cikakken shirin Harshe (Entire Program)"""
    statements: List[Statement] = field(default_factory=list)


@dataclass(kw_only=True)
class BlockStatement(Statement):
    """Sashen jumla a cikin baka { ... } (Block of statements)"""
    statements: List[Statement] = field(default_factory=list)


@dataclass(kw_only=True)
class ExpressionStatement(Statement):
    """Jumla mai dauke da lissafi ko aiki (Expression as a Statement)"""
    expression: 'Expression'


@dataclass(kw_only=True)
class VariableDecl(Statement):
    """Sanar da mai canji (bari x = 10 ko tsayayye PI = 3.14)"""
    name: str
    type_hint: Optional[str] = None
    initializer: Optional['Expression'] = None
    is_const: bool = False


@dataclass(kw_only=True)
class Assignment(Statement):
    """Sauya darajar mai canji (x = 20 ko x += 5 ko jeri[0] = 10)"""
    target: 'Expression'
    operator: str  # '=', '+=', '-=', '*=', '/='
    value: 'Expression'


@dataclass(kw_only=True)
class IfStatement(Statement):
    """Sharadi (idan, ko idan, in ba haka ba)"""
    condition: 'Expression'
    then_branch: BlockStatement
    elif_branches: List[Tuple['Expression', BlockStatement]] = field(default_factory=list)
    else_branch: Optional[BlockStatement] = None


@dataclass(kw_only=True)
class WhileStatement(Statement):
    """Madauki na yayin da (while loop)"""
    condition: 'Expression'
    body: BlockStatement


@dataclass(kw_only=True)
class ForStatement(Statement):
    """Madauki na ga ... a cikin ... (for loop)"""
    var_name: str
    iterator: 'Expression'
    body: BlockStatement


@dataclass(kw_only=True)
class FunctionDecl(Statement):
    """Kirkirar sabon aiki (Function definition)"""
    name: str
    params: List[Tuple[str, Optional[str]]]  # [(name, type_hint)]
    body: BlockStatement
    return_type_hint: Optional[str] = None


@dataclass(kw_only=True)
class ReturnStatement(Statement):
    """Koma da daraja (Return statement)"""
    value: Optional['Expression'] = None


@dataclass(kw_only=True)
class BreakStatement(Statement):
    """Tsayar da madauki (Break statement)"""
    pass


@dataclass(kw_only=True)
class ContinueStatement(Statement):
    """Ci gaba da madauki (Continue statement)"""
    pass


@dataclass(kw_only=True)
class TryCatchStatement(Statement):
    """Gwada da kama kuskure (Try-catch error handling)"""
    try_block: BlockStatement
    error_var: str
    catch_block: BlockStatement


@dataclass(kw_only=True)
class ImportStatement(Statement):
    """Shigo da wani fayil ko laburare (shigo_da "lissafi.hausa" ko daga "mod" shigo_da f1, f2)"""
    module_path: str
    imported_symbols: Optional[List[str]] = None  # None means import all / bind to module name
    alias: Optional[str] = None


# ==========================================
# LISSAFI DA HUKUNCI (Expressions)
# ==========================================

@dataclass(kw_only=True)
class Expression(ASTNode):
    pass


@dataclass(kw_only=True)
class BinaryOp(Expression):
    """Lissafi tsakanin bangarori biyu (Binary operation: a + b, x > y)"""
    left: Expression
    operator: Token
    right: Expression


@dataclass(kw_only=True)
class UnaryOp(Expression):
    """Lissafin guda daya (Unary operation: -x, !gaskiya, ba x)"""
    operator: Token
    operand: Expression


@dataclass(kw_only=True)
class LogicalOp(Expression):
    """Hadin hukunci (Logical operation: a kuma b, x ko y)"""
    left: Expression
    operator: Token
    right: Expression


@dataclass(kw_only=True)
class Literal(Expression):
    """Daraja ta asali (Number, String, Boolean, Null)"""
    value: Any
    raw: str = ""


@dataclass(kw_only=True)
class Identifier(Expression):
    """Sunan mai canji ko aiki (Variable / Function Name)"""
    name: str


@dataclass(kw_only=True)
class ListLiteral(Expression):
    """Jeri na darajoji ([1, 2, "uku"])"""
    elements: List[Expression] = field(default_factory=list)


@dataclass(kw_only=True)
class DictLiteral(Expression):
    """Kamus na bayanai ({"suna": "Aliyu", "shekaru": 25})"""
    pairs: List[Tuple[Expression, Expression]] = field(default_factory=list)


@dataclass(kw_only=True)
class IndexExpr(Expression):
    """Kiran lamba a jeri ko kamus (jeri[0] ko kamus["suna"])"""
    target: Expression
    index: Expression


@dataclass(kw_only=True)
class SliceExpr(Expression):
    """Yankin jeri ko rubutu (jeri[0:5:1])"""
    target: Expression
    start: Optional[Expression] = None
    stop: Optional[Expression] = None
    step: Optional[Expression] = None


@dataclass(kw_only=True)
class CallExpr(Expression):
    """Kiran aiki tare da shigarwa (buga("Sannu"), lissafi(5, 10))"""
    callee: Expression
    arguments: List[Expression] = field(default_factory=list)


@dataclass(kw_only=True)
class AnonymousFunction(Expression):
    """Aiki marar suna (Lambda / Anonymous Function)"""
    params: List[Tuple[str, Optional[str]]] = field(default_factory=list)
    body: BlockStatement

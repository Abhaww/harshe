"""
Harshe - Injin Gudanarwa (Interpreter Module)
Injin da yake gudanar da bishiyar nahawu (AST Tree-Walk Interpreter).
"""

import os
from typing import Any, List, Dict, Optional
from .tokens import TokenType
from .ast_nodes import (
    ASTNode, Program, Statement, BlockStatement, ExpressionStatement,
    VariableDecl, Assignment, IfStatement, WhileStatement, ForStatement,
    FunctionDecl, ReturnStatement, BreakStatement, ContinueStatement,
    TryCatchStatement, ImportStatement, Expression, BinaryOp, UnaryOp, LogicalOp,
    Literal, Identifier, ListLiteral, DictLiteral, IndexExpr, SliceExpr,
    CallExpr, AnonymousFunction
)
from .values import (
    HarsheValue, HarsheNumber, HarsheString, HarsheBoolean,
    HarsheNull, HarsheList, HarsheDict, HarsheFunction,
    HarsheBuiltinFunction, to_harshe_value
)
from .environment import Environment
from .builtins import get_default_builtins
from .errors import (
    HarsheError, KuskurenNahawu, KuskurenSuna, KuskurenNaui,
    KuskurenLissafi, KuskurenMatsayi, KuskurenAiki,
    KomaSignal, TsayaSignal, CiGabaSignal
)


class Interpreter:
    """Injin da yake gudanar da rubutun Harshe (Harshe Tree-Walk Interpreter)"""

    def __init__(self, global_env: Optional[Environment] = None, source_code: str = "", current_file: str = "<shigarwa>"):
        self.source_code = source_code
        self.current_file = current_file
        self.loaded_modules: Dict[str, Environment] = {}

        if global_env is None:
            self.globals = Environment()
            self._load_builtins()
        else:
            self.globals = global_env
        self.current_env = self.globals

    def _load_builtins(self) -> None:
        """Sanya dukkan ayyukan cikin harshe a cikin babban muhalli (Global Scope)"""
        builtins = get_default_builtins()
        for name, func in builtins.items():
            self.globals.define(name, func, is_const=True)

    def interpret(self, program: Program) -> HarsheValue:
        """Gudanar da dukkan shirin Harshe"""
        last_val: HarsheValue = HarsheNull()
        try:
            for stmt in program.statements:
                last_val = self.execute(stmt)
        except KomaSignal as sig:
            return sig.value
        except TsayaSignal:
            raise KuskurenNahawu("Ba za a iya kiran 'tsaya' a wajen madauki ba.", source_code=self.source_code)
        except CiGabaSignal:
            raise KuskurenNahawu("Ba za a iya kiran 'ci_gaba' a wajen madauki ba.", source_code=self.source_code)
        return last_val

    # ==========================================
    # GUDANAR DA JUMLOLI (Statement Execution)
    # ==========================================

    def execute(self, stmt: Statement) -> HarsheValue:
        """Gudanar da jumla guda daya"""
        if isinstance(stmt, VariableDecl):
            return self.execute_variable_decl(stmt)
        elif isinstance(stmt, Assignment):
            return self.execute_assignment(stmt)
        elif isinstance(stmt, IfStatement):
            return self.execute_if(stmt)
        elif isinstance(stmt, WhileStatement):
            return self.execute_while(stmt)
        elif isinstance(stmt, ForStatement):
            return self.execute_for(stmt)
        elif isinstance(stmt, FunctionDecl):
            return self.execute_function_decl(stmt)
        elif isinstance(stmt, ReturnStatement):
            val = self.evaluate(stmt.value) if stmt.value else HarsheNull()
            raise KomaSignal(val)
        elif isinstance(stmt, BreakStatement):
            raise TsayaSignal()
        elif isinstance(stmt, ContinueStatement):
            raise CiGabaSignal()
        elif isinstance(stmt, TryCatchStatement):
            return self.execute_try_catch(stmt)
        elif isinstance(stmt, ImportStatement):
            return self.execute_import(stmt)
        elif isinstance(stmt, BlockStatement):
            return self.execute_block(stmt, Environment(parent=self.current_env))
        elif isinstance(stmt, ExpressionStatement):
            return self.evaluate(stmt.expression)
        else:
            raise KuskurenAiki(f"Jumlar da ba a sani ba: {type(stmt).__name__}", stmt.start_pos, stmt.end_pos, self.source_code)

    def execute_import(self, stmt: ImportStatement) -> HarsheValue:
        """Shigo da wani fayil din Harshe ko laburare"""
        target_path = self._resolve_module_path(stmt.module_path)
        if not target_path or not os.path.exists(target_path):
            raise KuskurenAiki(
                f"Ba a sami fayil ko laburaren '{stmt.module_path}' ba da za a shigo da shi.",
                stmt.start_pos, stmt.end_pos, self.source_code
            )

        norm_path = os.path.abspath(target_path)

        # Check if already loaded
        if norm_path in self.loaded_modules:
            mod_env = self.loaded_modules[norm_path]
        else:
            with open(norm_path, 'r', encoding='utf-8') as f:
                mod_source = f.read()

            from .lexer import Lexer
            from .parser import Parser

            lexer = Lexer(mod_source, norm_path)
            tokens = lexer.tokenize()
            parser = Parser(tokens, mod_source)
            ast = parser.parse()

            mod_env = Environment(parent=self.globals)
            sub_interp = Interpreter(global_env=mod_env, source_code=mod_source, current_file=norm_path)
            sub_interp.loaded_modules = self.loaded_modules
            sub_interp.interpret(ast)

            self.loaded_modules[norm_path] = mod_env

        # Extract symbols
        if stmt.imported_symbols is not None:
            for sym_name in stmt.imported_symbols:
                if sym_name in mod_env.symbols:
                    sym = mod_env.symbols[sym_name]
                    self.current_env.define(sym_name, sym.value, is_const=sym.is_const, type_hint=sym.type_hint)
                else:
                    raise KuskurenSuna(
                        f"Ba a sami '{sym_name}' a cikin laburaren '{stmt.module_path}' ba.",
                        stmt.start_pos, stmt.end_pos, self.source_code
                    )
        else:
            # Import all user symbols
            for k, sym in mod_env.symbols.items():
                if k not in self.globals.symbols:
                    self.current_env.define(k, sym.value, is_const=sym.is_const, type_hint=sym.type_hint)

            # Also create a module namespace dictionary
            mod_name = os.path.splitext(os.path.basename(norm_path))[0]
            mod_dict = HarsheDict({k: sym.value for k, sym in mod_env.symbols.items() if k not in self.globals.symbols})
            self.current_env.define(mod_name, mod_dict, is_const=True)

        return HarsheNull()

    def _resolve_module_path(self, raw_path: str) -> Optional[str]:
        """Nemo ainihin hanyar fayil din laburare"""
        candidates = [raw_path]
        if not (raw_path.endswith('.hausa') or raw_path.endswith('.har') or raw_path.endswith('.hsh')):
            candidates.append(f"{raw_path}.hausa")
            candidates.append(f"{raw_path}.har")

        base_dirs = []
        if self.current_file and self.current_file != "<shigarwa>":
            base_dirs.append(os.path.dirname(os.path.abspath(self.current_file)))
        base_dirs.append(os.getcwd())
        
        # Standard library folder relative to interpreter module
        stdlib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "harshe_stdlib"))
        if os.path.exists(stdlib_path):
            base_dirs.append(stdlib_path)

        for b_dir in base_dirs:
            for cand in candidates:
                full_p = os.path.normpath(os.path.join(b_dir, cand))
                if os.path.isfile(full_p):
                    return full_p

        return None

    def execute_block(self, block: BlockStatement, env: Environment) -> HarsheValue:
        """Gudanar da sashe a cikin sabon muhallin ma'aji"""
        previous_env = self.current_env
        self.current_env = env
        last_val: HarsheValue = HarsheNull()
        try:
            for stmt in block.statements:
                last_val = self.execute(stmt)
        finally:
            self.current_env = previous_env
        return last_val

    def execute_variable_decl(self, stmt: VariableDecl) -> HarsheValue:
        val: HarsheValue = HarsheNull()
        if stmt.initializer is not None:
            val = self.evaluate(stmt.initializer)
        self.current_env.define(stmt.name, val, is_const=stmt.is_const, type_hint=stmt.type_hint)
        return val

    def execute_assignment(self, stmt: Assignment) -> HarsheValue:
        val = self.evaluate(stmt.value)

        # 1. Assignment to simple variable: x = 10, x += 5
        if isinstance(stmt.target, Identifier):
            name = stmt.target.name
            if stmt.operator == '=':
                target_val = val
            else:
                curr = self.current_env.get(name)
                target_val = self._apply_compound_op(curr, stmt.operator, val, stmt)
            self.current_env.assign(name, target_val)
            return target_val

        # 2. Assignment to index/key: arr[0] = 10, dict["suna"] = "Aliyu"
        elif isinstance(stmt.target, IndexExpr):
            obj = self.evaluate(stmt.target.target)
            idx = self.evaluate(stmt.target.index)

            if isinstance(obj, HarsheList):
                if not isinstance(idx, HarsheNumber):
                    raise KuskurenNaui("Dole ne matsayin jeri ya zama lamba.", stmt.target.index.start_pos, stmt.target.index.end_pos, self.source_code)
                i = int(idx.value)
                if not (-len(obj.elements) <= i < len(obj.elements)):
                    raise KuskurenMatsayi(f"Matsayin lamba {i} ya wuce iyakar jeri (tsawo: {len(obj.elements)}).", stmt.target.index.start_pos, stmt.target.index.end_pos, self.source_code)
                if i < 0:
                    i += len(obj.elements)

                if stmt.operator == '=':
                    target_val = val
                else:
                    curr = obj.elements[i]
                    target_val = self._apply_compound_op(curr, stmt.operator, val, stmt)
                obj.elements[i] = target_val
                return target_val

            elif isinstance(obj, HarsheDict):
                key = str(idx) if isinstance(idx, (HarsheString, HarsheNumber)) else str(idx.harshe_repr())
                if stmt.operator == '=':
                    target_val = val
                else:
                    curr = obj.pairs.get(key, HarsheNull())
                    target_val = self._apply_compound_op(curr, stmt.operator, val, stmt)
                obj.pairs[key] = target_val
                return target_val
            else:
                raise KuskurenNaui(f"Ba za a iya sauya daraja a cikin nau'in '{obj.type_name}' ba.", stmt.target.start_pos, stmt.target.end_pos, self.source_code)

        raise KuskurenNahawu("Wurin da aka yi niyyar sauyawa bai dace ba.", stmt.target.start_pos, stmt.target.end_pos, self.source_code)

    def _apply_compound_op(self, curr: HarsheValue, op: str, val: HarsheValue, stmt: Statement) -> HarsheValue:
        if op == '+=':
            return self._eval_add(curr, val, stmt)
        elif op == '-=':
            return self._eval_sub(curr, val, stmt)
        elif op == '*=':
            return self._eval_mul(curr, val, stmt)
        elif op == '/=':
            return self._eval_div(curr, val, stmt)
        raise KuskurenAiki(f"Alamar sauya daraja marar inganci: '{op}'", stmt.start_pos, stmt.end_pos, self.source_code)

    def execute_if(self, stmt: IfStatement) -> HarsheValue:
        cond_val = self.evaluate(stmt.condition)
        if cond_val.is_truthy():
            return self.execute_block(stmt.then_branch, Environment(parent=self.current_env))

        for elif_cond_node, elif_body in stmt.elif_branches:
            if self.evaluate(elif_cond_node).is_truthy():
                return self.execute_block(elif_body, Environment(parent=self.current_env))

        if stmt.else_branch is not None:
            return self.execute_block(stmt.else_branch, Environment(parent=self.current_env))

        return HarsheNull()

    def execute_while(self, stmt: WhileStatement) -> HarsheValue:
        last_val: HarsheValue = HarsheNull()
        while self.evaluate(stmt.condition).is_truthy():
            try:
                last_val = self.execute_block(stmt.body, Environment(parent=self.current_env))
            except TsayaSignal:
                break
            except CiGabaSignal:
                continue
        return last_val

    def execute_for(self, stmt: ForStatement) -> HarsheValue:
        iter_val = self.evaluate(stmt.iterator)
        items: List[HarsheValue] = []

        if isinstance(iter_val, HarsheList):
            items = iter_val.elements
        elif isinstance(iter_val, HarsheString):
            items = [HarsheString(c) for c in iter_val.value]
        elif isinstance(iter_val, HarsheDict):
            items = [HarsheString(k) for k in iter_val.pairs.keys()]
        else:
            raise KuskurenNaui(
                f"Ba za a iya yin madauki a kan nau'in '{iter_val.type_name}' ba.",
                stmt.iterator.start_pos, stmt.iterator.end_pos, self.source_code
            )

        last_val: HarsheValue = HarsheNull()
        for item in items:
            loop_env = Environment(parent=self.current_env)
            loop_env.define(stmt.var_name, item)
            try:
                last_val = self.execute_block(stmt.body, loop_env)
            except TsayaSignal:
                break
            except CiGabaSignal:
                continue

        return last_val

    def execute_function_decl(self, stmt: FunctionDecl) -> HarsheValue:
        func = HarsheFunction(
            name=stmt.name,
            params=stmt.params,
            body=stmt.body,
            closure_env=self.current_env,
            return_type=stmt.return_type_hint
        )
        self.current_env.define(stmt.name, func, is_const=False)
        return func

    def execute_try_catch(self, stmt: TryCatchStatement) -> HarsheValue:
        try:
            return self.execute_block(stmt.try_block, Environment(parent=self.current_env))
        except HarsheError as e:
            catch_env = Environment(parent=self.current_env)
            catch_env.define(stmt.error_var, HarsheString(e.details))
            return self.execute_block(stmt.catch_block, catch_env)

    # ==========================================
    # KINTA DARUJOJI (Expression Evaluation)
    # ==========================================

    def evaluate(self, expr: Expression) -> HarsheValue:
        """Kinta darajar lissafi ko aiki"""
        if isinstance(expr, Literal):
            return to_harshe_value(expr.value)

        elif isinstance(expr, Identifier):
            try:
                return self.current_env.get(expr.name)
            except KuskurenSuna as e:
                raise KuskurenSuna(e.details, expr.start_pos, expr.end_pos, self.source_code)

        elif isinstance(expr, BinaryOp):
            return self.eval_binary_op(expr)

        elif isinstance(expr, UnaryOp):
            return self.eval_unary_op(expr)

        elif isinstance(expr, LogicalOp):
            return self.eval_logical_op(expr)

        elif isinstance(expr, ListLiteral):
            elements = [self.evaluate(el) for el in expr.elements]
            return HarsheList(elements)

        elif isinstance(expr, DictLiteral):
            pairs = {}
            for k_expr, v_expr in expr.pairs:
                k_val = self.evaluate(k_expr)
                v_val = self.evaluate(v_expr)
                pairs[str(k_val)] = v_val
            return HarsheDict(pairs)

        elif isinstance(expr, IndexExpr):
            return self.eval_index_expr(expr)

        elif isinstance(expr, SliceExpr):
            return self.eval_slice_expr(expr)

        elif isinstance(expr, CallExpr):
            return self.eval_call_expr(expr)

        elif isinstance(expr, AnonymousFunction):
            return HarsheFunction(
                name="<marar_suna>",
                params=expr.params,
                body=expr.body,
                closure_env=self.current_env
            )

        raise KuskurenAiki(f"Lissafin da ba a sani ba: {type(expr).__name__}", expr.start_pos, expr.end_pos, self.source_code)

    def eval_binary_op(self, expr: BinaryOp) -> HarsheValue:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        op_type = expr.operator.type

        if op_type == TokenType.PLUS:
            return self._eval_add(left, right, expr)
        elif op_type == TokenType.MINUS:
            return self._eval_sub(left, right, expr)
        elif op_type == TokenType.STAR:
            return self._eval_mul(left, right, expr)
        elif op_type == TokenType.SLASH:
            return self._eval_div(left, right, expr)
        elif op_type == TokenType.PERCENT:
            return self._eval_mod(left, right, expr)
        elif op_type == TokenType.POW:
            return self._eval_pow(left, right, expr)
        elif op_type == TokenType.EQUAL:
            return HarsheBoolean(left == right)
        elif op_type == TokenType.NOT_EQUAL:
            return HarsheBoolean(not (left == right))
        elif op_type == TokenType.LESS:
            return self._eval_comparison(left, '<', right, expr)
        elif op_type == TokenType.LESS_EQUAL:
            return self._eval_comparison(left, '<=', right, expr)
        elif op_type == TokenType.GREATER:
            return self._eval_comparison(left, '>', right, expr)
        elif op_type == TokenType.GREATER_EQUAL:
            return self._eval_comparison(left, '>=', right, expr)

        raise KuskurenAiki(f"Alamar lissafi marar inganci: '{expr.operator.value}'", expr.start_pos, expr.end_pos, self.source_code)

    def _eval_add(self, left: HarsheValue, right: HarsheValue, node: ASTNode) -> HarsheValue:
        if isinstance(left, HarsheNumber) and isinstance(right, HarsheNumber):
            return HarsheNumber(left.value + right.value)
        if isinstance(left, HarsheString) or isinstance(right, HarsheString):
            return HarsheString(str(left) + str(right))
        if isinstance(left, HarsheList) and isinstance(right, HarsheList):
            return HarsheList(left.elements + right.elements)
        raise KuskurenNaui(
            f"Ba za a iya hada nau'in '{left.type_name}' da '{right.type_name}' ta amfani da '+' ba.",
            node.start_pos, node.end_pos, self.source_code
        )

    def _eval_sub(self, left: HarsheValue, right: HarsheValue, node: ASTNode) -> HarsheValue:
        if isinstance(left, HarsheNumber) and isinstance(right, HarsheNumber):
            return HarsheNumber(left.value - right.value)
        raise KuskurenNaui(
            f"Ba za a iya debe nau'in '{right.type_name}' daga '{left.type_name}' ta amfani da '-' ba.",
            node.start_pos, node.end_pos, self.source_code
        )

    def _eval_mul(self, left: HarsheValue, right: HarsheValue, node: ASTNode) -> HarsheValue:
        if isinstance(left, HarsheNumber) and isinstance(right, HarsheNumber):
            return HarsheNumber(left.value * right.value)
        if isinstance(left, HarsheString) and isinstance(right, HarsheNumber):
            return HarsheString(left.value * int(right.value))
        if isinstance(left, HarsheList) and isinstance(right, HarsheNumber):
            return HarsheList(left.elements * int(right.value))
        raise KuskurenNaui(
            f"Ba za a iya ninka '{left.type_name}' da '{right.type_name}' ta amfani da '*' ba.",
            node.start_pos, node.end_pos, self.source_code
        )

    def _eval_div(self, left: HarsheValue, right: HarsheValue, node: ASTNode) -> HarsheValue:
        if isinstance(left, HarsheNumber) and isinstance(right, HarsheNumber):
            if right.value == 0:
                raise KuskurenLissafi("Ba za a iya raba lamba da sifili (0) ba.", node.start_pos, node.end_pos, self.source_code)
            return HarsheNumber(left.value / right.value)
        raise KuskurenNaui(
            f"Ba za a iya raba '{left.type_name}' da '{right.type_name}' ba.",
            node.start_pos, node.end_pos, self.source_code
        )

    def _eval_mod(self, left: HarsheValue, right: HarsheValue, node: ASTNode) -> HarsheValue:
        if isinstance(left, HarsheNumber) and isinstance(right, HarsheNumber):
            if right.value == 0:
                raise KuskurenLissafi("Ba za a iya neman sauran rabo (%) da sifili (0) ba.", node.start_pos, node.end_pos, self.source_code)
            return HarsheNumber(left.value % right.value)
        raise KuskurenNaui(
            f"Ba za a iya neman sauran rabo (%) a tsakanin '{left.type_name}' da '{right.type_name}' ba.",
            node.start_pos, node.end_pos, self.source_code
        )

    def _eval_pow(self, left: HarsheValue, right: HarsheValue, node: ASTNode) -> HarsheValue:
        if isinstance(left, HarsheNumber) and isinstance(right, HarsheNumber):
            return HarsheNumber(left.value ** right.value)
        raise KuskurenNaui(
            f"Ba za a iya lissafin iko (**) tsakanin '{left.type_name}' da '{right.type_name}' ba.",
            node.start_pos, node.end_pos, self.source_code
        )

    def _eval_comparison(self, left: HarsheValue, op: str, right: HarsheValue, node: ASTNode) -> HarsheBoolean:
        if isinstance(left, HarsheNumber) and isinstance(right, HarsheNumber):
            l_val, r_val = left.value, right.value
        elif isinstance(left, HarsheString) and isinstance(right, HarsheString):
            l_val, r_val = left.value, right.value
        else:
            raise KuskurenNaui(
                f"Ba za a iya kwatanta '{left.type_name}' da '{right.type_name}' ba ta amfani da '{op}'.",
                node.start_pos, node.end_pos, self.source_code
            )

        if op == '<':
            return HarsheBoolean(l_val < r_val)
        elif op == '<=':
            return HarsheBoolean(l_val <= r_val)
        elif op == '>':
            return HarsheBoolean(l_val > r_val)
        elif op == '>=':
            return HarsheBoolean(l_val >= r_val)
        return HarsheBoolean(False)

    def eval_unary_op(self, expr: UnaryOp) -> HarsheValue:
        operand = self.evaluate(expr.operand)
        op_type = expr.operator.type

        if op_type == TokenType.MINUS:
            if isinstance(operand, HarsheNumber):
                return HarsheNumber(-operand.value)
            raise KuskurenNaui(f"Ba za a iya sanya alamar debe (-) a gaban '{operand.type_name}' ba.", expr.start_pos, expr.end_pos, self.source_code)

        elif op_type in (TokenType.NOT, TokenType.BA):
            return HarsheBoolean(not operand.is_truthy())

        raise KuskurenAiki(f"Alamar unary marar inganci: '{expr.operator.value}'", expr.start_pos, expr.end_pos, self.source_code)

    def eval_logical_op(self, expr: LogicalOp) -> HarsheValue:
        left = self.evaluate(expr.left)
        op_type = expr.operator.type

        # Short-circuit logical OR (ko / ||)
        if op_type in (TokenType.KO, TokenType.OR):
            if left.is_truthy():
                return left
            return self.evaluate(expr.right)

        # Short-circuit logical AND (kuma / &&)
        if op_type in (TokenType.KUMA, TokenType.AND):
            if not left.is_truthy():
                return left
            return self.evaluate(expr.right)

        raise KuskurenAiki(f"Alamar hadin hukunci marar inganci: '{expr.operator.value}'", expr.start_pos, expr.end_pos, self.source_code)

    def eval_index_expr(self, expr: IndexExpr) -> HarsheValue:
        obj = self.evaluate(expr.target)
        idx = self.evaluate(expr.index)

        if isinstance(obj, HarsheList):
            if not isinstance(idx, HarsheNumber):
                raise KuskurenNaui("Dole ne matsayin jeri ya zama lamba.", expr.index.start_pos, expr.index.end_pos, self.source_code)
            i = int(idx.value)
            if not (-len(obj.elements) <= i < len(obj.elements)):
                raise KuskurenMatsayi(f"Matsayin lamba {i} ya wuce iyakar jeri (tsawo: {len(obj.elements)}).", expr.index.start_pos, expr.index.end_pos, self.source_code)
            return obj.elements[i]

        elif isinstance(obj, HarsheString):
            if not isinstance(idx, HarsheNumber):
                raise KuskurenNaui("Dole ne matsayin rubutu ya zama lamba.", expr.index.start_pos, expr.index.end_pos, self.source_code)
            i = int(idx.value)
            if not (-len(obj.value) <= i < len(obj.value)):
                raise KuskurenMatsayi(f"Matsayin lamba {i} ya wuce iyakar rubutu (tsawo: {len(obj.value)}).", expr.index.start_pos, expr.index.end_pos, self.source_code)
            return HarsheString(obj.value[i])

        elif isinstance(obj, HarsheDict):
            key = str(idx)
            if key not in obj.pairs:
                raise KuskurenMatsayi(f"Ba a sami makulli mai suna '{key}' a cikin kamus ba.", expr.index.start_pos, expr.index.end_pos, self.source_code)
            return obj.pairs[key]

        raise KuskurenNaui(f"Ba za a iya kiran matsayi a kan nau'in '{obj.type_name}' ba.", expr.target.start_pos, expr.target.end_pos, self.source_code)

    def eval_slice_expr(self, expr: SliceExpr) -> HarsheValue:
        obj = self.evaluate(expr.target)
        start_val = int(self.evaluate(expr.start).value) if expr.start else None
        stop_val = int(self.evaluate(expr.stop).value) if expr.stop else None
        step_val = int(self.evaluate(expr.step).value) if expr.step else None

        if isinstance(obj, HarsheList):
            sliced = obj.elements[slice(start_val, stop_val, step_val)]
            return HarsheList(sliced)

        elif isinstance(obj, HarsheString):
            sliced_str = obj.value[slice(start_val, stop_val, step_val)]
            return HarsheString(sliced_str)

        raise KuskurenNaui(f"Ba za a iya yanka sashen '{obj.type_name}' ba.", expr.target.start_pos, expr.target.end_pos, self.source_code)

    def eval_call_expr(self, expr: CallExpr) -> HarsheValue:
        callee = self.evaluate(expr.callee)
        evaluated_args = [self.evaluate(arg) for arg in expr.arguments]

        # 1. User-defined Function
        if isinstance(callee, HarsheFunction):
            expected_count = len(callee.params)
            given_count = len(evaluated_args)
            if expected_count != given_count:
                raise KuskurenAiki(
                    f"Aikin '{callee.name}' yana bukatar ma'auni {expected_count}, amma an shigar da {given_count}.",
                    expr.start_pos, expr.end_pos, self.source_code
                )

            call_env = Environment(parent=callee.closure_env)
            for (p_name, p_type), arg_val in zip(callee.params, evaluated_args):
                call_env.define(p_name, arg_val, is_const=False, type_hint=p_type)

            try:
                ret_val = self.execute_block(callee.body, call_env)
            except KomaSignal as sig:
                ret_val = sig.value

            # Check return type if specified
            if callee.return_type is not None and not isinstance(ret_val, HarsheNull):
                call_env._check_type(f"koma daga {callee.name}", ret_val, callee.return_type)

            return ret_val

        # 2. Built-in Function
        elif isinstance(callee, HarsheBuiltinFunction):
            try:
                return callee.func(*evaluated_args)
            except HarsheError as e:
                e.start_pos = expr.start_pos
                e.end_pos = expr.end_pos
                e.source_code = self.source_code
                raise e
            except Exception as e:
                raise KuskurenAiki(f"Matsala a aikin '{callee.name}': {str(e)}", expr.start_pos, expr.end_pos, self.source_code)

        raise KuskurenNaui(f"Ba za a iya kiran '{callee.type_name}' a matsayin aiki ba.", expr.callee.start_pos, expr.callee.end_pos, self.source_code)

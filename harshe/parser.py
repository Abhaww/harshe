"""
Harshe - Mai Nazarin Nahawu (Parser Module)
Sauya jerin alamomi (Tokens) zuwa bishiyar nahawu (Abstract Syntax Tree - AST).
"""

from typing import List, Optional, Tuple, Any
from .tokens import Token, TokenType
from .errors import KuskurenNahawu
from .ast_nodes import (
    Program, Statement, BlockStatement, ExpressionStatement,
    VariableDecl, Assignment, IfStatement, WhileStatement, ForStatement,
    FunctionDecl, ReturnStatement, BreakStatement, ContinueStatement,
    TryCatchStatement, ImportStatement, Expression, BinaryOp, UnaryOp, LogicalOp,
    Literal, Identifier, ListLiteral, DictLiteral, IndexExpr, SliceExpr,
    CallExpr, AnonymousFunction
)


class Parser:
    """Mai nazarin nahawun Harshe (Harshe Recursive Descent Parser)"""

    def __init__(self, tokens: List[Token], source_code: str = ""):
        self.tokens = tokens
        self.source_code = source_code
        self.current_idx = 0

    def current_token(self) -> Token:
        if self.current_idx < len(self.tokens):
            return self.tokens[self.current_idx]
        return self.tokens[-1]  # Return EOF

    def peek_token(self, offset: int = 1) -> Token:
        idx = self.current_idx + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]

    def advance(self) -> Token:
        tok = self.current_token()
        if self.current_idx < len(self.tokens) - 1:
            self.current_idx += 1
        return tok

    def skip_newlines(self) -> None:
        while self.current_token().type == TokenType.NEWLINE:
            self.advance()

    def match(self, *types: TokenType) -> bool:
        if self.current_token().type in types:
            self.advance()
            return True
        return False

    def expect(self, token_type: TokenType, error_msg: str) -> Token:
        if self.current_token().type == token_type:
            return self.advance()
        tok = self.current_token()
        raise KuskurenNahawu(
            f"{error_msg} (an sami '{tok.value if tok.value is not None else tok.type.name}')",
            tok.start_pos, tok.end_pos, self.source_code
        )

    def consume_statement_delimiter(self) -> None:
        """Kula da alamar kammala jumla (; ko sabon layi ko })"""
        if self.current_token().type == TokenType.SEMICOLON:
            self.advance()
        elif self.current_token().type in (TokenType.NEWLINE, TokenType.RBRACE, TokenType.EOF):
            while self.current_token().type == TokenType.NEWLINE:
                self.advance()
        else:
            tok = self.current_token()
            raise KuskurenNahawu(
                f"Ana bukatar ';' ko sabon layi a karshen jumla, amma an sami '{tok.value if tok.value is not None else tok.type.name}'",
                tok.start_pos, tok.end_pos, self.source_code
            )

    # ==========================================
    # BABBAN SHIRI (Program & Statements)
    # ==========================================

    def parse(self) -> Program:
        """Nazarin dukkan shirin"""
        statements: List[Statement] = []
        start_pos = self.current_token().start_pos

        self.skip_newlines()
        while self.current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()

        end_pos = self.current_token().end_pos
        return Program(start_pos=start_pos, end_pos=end_pos, statements=statements)

    def parse_statement(self) -> Statement:
        """Nazarin jumla daya"""
        self.skip_newlines()
        tok = self.current_token()

        if tok.type in (TokenType.BARI, TokenType.SAKA):
            return self.parse_variable_decl(is_const=False)
        elif tok.type == TokenType.TSAYAYYE:
            return self.parse_variable_decl(is_const=True)
        elif tok.type == TokenType.AIKI:
            return self.parse_function_decl()
        elif tok.type == TokenType.IDAN:
            return self.parse_if_statement()
        elif tok.type == TokenType.YAYIN_DA:
            return self.parse_while_statement()
        elif tok.type == TokenType.GA:
            return self.parse_for_statement()
        elif tok.type == TokenType.KOMA:
            return self.parse_return_statement()
        elif tok.type == TokenType.TSAYA:
            return self.parse_break_statement()
        elif tok.type == TokenType.CI_GABA:
            return self.parse_continue_statement()
        elif tok.type == TokenType.GWADA:
            return self.parse_try_catch_statement()
        elif tok.type == TokenType.SHIGO_DA:
            return self.parse_import_statement()
        elif tok.type == TokenType.DAGA:
            return self.parse_from_import_statement()
        elif tok.type == TokenType.LBRACE:
            return self.parse_block()
        else:
            return self.parse_expression_or_assignment_statement()

    def parse_import_statement(self) -> ImportStatement:
        """Nazarin shigo_da (shigo_da "lissafi.hausa" ko shigo_da lissafi)"""
        start_tok = self.advance()  # shigo_da
        tok = self.current_token()

        if tok.type == TokenType.STRING:
            self.advance()
            mod_path = str(tok.value)
        elif tok.type == TokenType.IDENTIFIER:
            self.advance()
            mod_path = str(tok.value)
        else:
            raise KuskurenNahawu("Ana bukatar sunan fayil ko laburare bayan 'shigo_da'", tok.start_pos, tok.end_pos, self.source_code)

        alias = None
        # Check optional alias: shigo_da lissafi a_matsayin l
        # if needed

        self.consume_statement_delimiter()
        return ImportStatement(start_pos=start_tok.start_pos, end_pos=tok.end_pos, module_path=mod_path, imported_symbols=None, alias=alias)

    def parse_from_import_statement(self) -> ImportStatement:
        """Nazarin daga ... shigo_da ... (daga "lissafi" shigo_da tushe, iko;)"""
        start_tok = self.advance()  # daga
        mod_tok = self.current_token()

        if mod_tok.type == TokenType.STRING:
            self.advance()
            mod_path = str(mod_tok.value)
        elif mod_tok.type == TokenType.IDENTIFIER:
            self.advance()
            mod_path = str(mod_tok.value)
        else:
            raise KuskurenNahawu("Ana bukatar sunan fayil ko laburare bayan 'daga'", mod_tok.start_pos, mod_tok.end_pos, self.source_code)

        self.expect(TokenType.SHIGO_DA, "Ana bukatar 'shigo_da' bayan sunan fayil a cikin 'daga ... shigo_da ...'")

        symbols: List[str] = []
        while True:
            sym_tok = self.expect(TokenType.IDENTIFIER, "Ana bukatar sunan aiki ko mai canji da za a shigo da shi")
            symbols.append(str(sym_tok.value))
            if not self.match(TokenType.COMMA):
                break

        self.consume_statement_delimiter()
        return ImportStatement(start_pos=start_tok.start_pos, end_pos=self.current_token().end_pos, module_path=mod_path, imported_symbols=symbols)

    def parse_block(self) -> BlockStatement:
        """Nazarin sashe a cikin { ... }"""
        start_tok = self.expect(TokenType.LBRACE, "Ana bukatar '{' a farkon sashen aiki ko sharadi")
        statements: List[Statement] = []

        self.skip_newlines()
        while self.current_token().type not in (TokenType.RBRACE, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()

        end_tok = self.expect(TokenType.RBRACE, "Ana bukatar '}' a karshen sashe")
        return BlockStatement(start_pos=start_tok.start_pos, end_pos=end_tok.end_pos, statements=statements)

    def parse_variable_decl(self, is_const: bool) -> VariableDecl:
        """Nazarin sanar da mai canji (bari x = 10 ko tsayayye PI = 3.14)"""
        start_tok = self.advance()  # bari / saka / tsayayye
        ident_tok = self.expect(TokenType.IDENTIFIER, "Ana bukatar sunan mai canji bayan 'bari' ko 'tsayayye'")
        name = str(ident_tok.value)

        # Optional type hint (e.g. : lamba)
        type_hint: Optional[str] = None
        if self.match(TokenType.COLON):
            type_tok = self.expect(TokenType.IDENTIFIER, "Ana bukatar sunan nau'in bayan ':'")
            type_hint = str(type_tok.value)

        init_expr: Optional[Expression] = None
        if self.match(TokenType.ASSIGN):
            init_expr = self.parse_expression()
        elif is_const:
            raise KuskurenNahawu(
                f"Dole ne a ba tsayayye '{name}' daraja a lokacin da aka sanar da shi",
                ident_tok.start_pos, ident_tok.end_pos, self.source_code
            )

        self.consume_statement_delimiter()
        end_pos = init_expr.end_pos if init_expr else ident_tok.end_pos
        return VariableDecl(
            start_pos=start_tok.start_pos, end_pos=end_pos,
            name=name, type_hint=type_hint, initializer=init_expr, is_const=is_const
        )

    def parse_function_decl(self) -> FunctionDecl:
        """Nazarin aiki (aiki gaisuwa(suna) { ... })"""
        start_tok = self.advance()  # aiki
        ident_tok = self.expect(TokenType.IDENTIFIER, "Ana bukatar sunan aiki bayan 'aiki'")
        name = str(ident_tok.value)

        self.expect(TokenType.LPAREN, "Ana bukatar '(' bayan sunan aiki")
        params: List[Tuple[str, Optional[str]]] = []

        if self.current_token().type != TokenType.RPAREN:
            while True:
                p_tok = self.expect(TokenType.IDENTIFIER, "Ana bukatar sunan ma'auni (parameter)")
                p_name = str(p_tok.value)
                p_type = None
                if self.match(TokenType.COLON):
                    pt_tok = self.expect(TokenType.IDENTIFIER, "Ana bukatar sunan nau'i bayan ':'")
                    p_type = str(pt_tok.value)
                params.append((p_name, p_type))

                if not self.match(TokenType.COMMA):
                    break

        self.expect(TokenType.RPAREN, "Ana bukatar ')' bayan jerin ma'aunan aiki")

        # Optional return type hint (-> lamba)
        ret_type: Optional[str] = None
        if self.match(TokenType.ARROW):
            rt_tok = self.expect(TokenType.IDENTIFIER, "Ana bukatar sunan nau'in komawa bayan '->'")
            ret_type = str(rt_tok.value)

        self.skip_newlines()
        body = self.parse_block()
        return FunctionDecl(
            start_pos=start_tok.start_pos, end_pos=body.end_pos,
            name=name, params=params, body=body, return_type_hint=ret_type
        )

    def parse_if_statement(self) -> IfStatement:
        """Nazarin sharadi (idan ... { } ko idan ... { } in ba haka ba { })"""
        start_tok = self.advance()  # idan
        
        # Parentheses around condition are optional
        has_paren = self.match(TokenType.LPAREN)
        condition = self.parse_expression()
        if has_paren:
            self.expect(TokenType.RPAREN, "Ana bukatar ')' bayan sharadin 'idan'")

        self.skip_newlines()
        then_branch = self.parse_block()

        elif_branches: List[Tuple[Expression, BlockStatement]] = []
        else_branch: Optional[BlockStatement] = None

        self.skip_newlines()
        while self.current_token().type == TokenType.KO_IDAN:
            self.advance()  # ko idan
            has_elif_paren = self.match(TokenType.LPAREN)
            elif_cond = self.parse_expression()
            if has_elif_paren:
                self.expect(TokenType.RPAREN, "Ana bukatar ')' bayan sharadin 'ko idan'")
            self.skip_newlines()
            elif_body = self.parse_block()
            elif_branches.append((elif_cond, elif_body))
            self.skip_newlines()

        if self.current_token().type == TokenType.IN_BA_HAKA_BA:
            self.advance()  # in ba haka ba
            self.skip_newlines()
            else_branch = self.parse_block()

        end_pos = else_branch.end_pos if else_branch else (elif_branches[-1][1].end_pos if elif_branches else then_branch.end_pos)
        return IfStatement(
            start_pos=start_tok.start_pos, end_pos=end_pos,
            condition=condition, then_branch=then_branch,
            elif_branches=elif_branches, else_branch=else_branch
        )

    def parse_while_statement(self) -> WhileStatement:
        """Nazarin madauki na yayin da (yayin da (x < 10) { ... })"""
        start_tok = self.advance()  # yayin da
        has_paren = self.match(TokenType.LPAREN)
        condition = self.parse_expression()
        if has_paren:
            self.expect(TokenType.RPAREN, "Ana bukatar ')' bayan sharadin 'yayin da'")

        self.skip_newlines()
        body = self.parse_block()
        return WhileStatement(start_pos=start_tok.start_pos, end_pos=body.end_pos, condition=condition, body=body)

    def parse_for_statement(self) -> ForStatement:
        """Nazarin madauki na ga (ga i a cikin kewayon(1, 10) { ... })"""
        start_tok = self.advance()  # ga
        var_tok = self.expect(TokenType.IDENTIFIER, "Ana bukatar sunan mai canji bayan 'ga'")
        var_name = str(var_tok.value)

        self.expect(TokenType.A_CIKIN, "Ana bukatar 'a cikin' bayan sunan mai canji a madaukin 'ga'")
        iterator = self.parse_expression()

        self.skip_newlines()
        body = self.parse_block()
        return ForStatement(start_pos=start_tok.start_pos, end_pos=body.end_pos, var_name=var_name, iterator=iterator, body=body)

    def parse_return_statement(self) -> ReturnStatement:
        """Nazarin koma (koma sakamako;)"""
        start_tok = self.advance()  # koma
        value: Optional[Expression] = None

        if self.current_token().type not in (TokenType.SEMICOLON, TokenType.NEWLINE, TokenType.RBRACE, TokenType.EOF):
            value = self.parse_expression()

        self.consume_statement_delimiter()
        end_pos = value.end_pos if value else start_tok.end_pos
        return ReturnStatement(start_pos=start_tok.start_pos, end_pos=end_pos, value=value)

    def parse_break_statement(self) -> BreakStatement:
        start_tok = self.advance()  # tsaya
        self.consume_statement_delimiter()
        return BreakStatement(start_pos=start_tok.start_pos, end_pos=start_tok.end_pos)

    def parse_continue_statement(self) -> ContinueStatement:
        start_tok = self.advance()  # ci_gaba
        self.consume_statement_delimiter()
        return ContinueStatement(start_pos=start_tok.start_pos, end_pos=start_tok.end_pos)

    def parse_try_catch_statement(self) -> TryCatchStatement:
        """Nazarin gwada ... kama (kuskure) { ... }"""
        start_tok = self.advance()  # gwada
        self.skip_newlines()
        try_block = self.parse_block()
        self.skip_newlines()

        self.expect(TokenType.KAMA, "Ana bukatar 'kama' bayan sashen 'gwada'")
        self.expect(TokenType.LPAREN, "Ana bukatar '(' bayan 'kama'")
        err_tok = self.expect(TokenType.IDENTIFIER, "Ana bukatar sunan mai canjin kuskure a cikin 'kama(kuskure)'")
        err_var = str(err_tok.value)
        self.expect(TokenType.RPAREN, "Ana bukatar ')' bayan sunan mai canjin kuskure")

        self.skip_newlines()
        catch_block = self.parse_block()
        return TryCatchStatement(start_pos=start_tok.start_pos, end_pos=catch_block.end_pos, try_block=try_block, error_var=err_var, catch_block=catch_block)

    def parse_expression_or_assignment_statement(self) -> Statement:
        expr = self.parse_expression()

        # Check if this is an assignment: x = 10, x += 5, jeri[0] = 10
        if self.current_token().type in (
            TokenType.ASSIGN, TokenType.PLUS_ASSIGN,
            TokenType.MINUS_ASSIGN, TokenType.STAR_ASSIGN, TokenType.SLASH_ASSIGN
        ):
            op_tok = self.advance()
            val_expr = self.parse_expression()
            self.consume_statement_delimiter()
            return Assignment(
                start_pos=expr.start_pos, end_pos=val_expr.end_pos,
                target=expr, operator=op_tok.value, value=val_expr
            )

        self.consume_statement_delimiter()
        return ExpressionStatement(start_pos=expr.start_pos, end_pos=expr.end_pos, expression=expr)

    # ==========================================
    # LISSAFI (Expressions & Operator Precedence)
    # ==========================================

    def parse_expression(self) -> Expression:
        return self.parse_logical_or()

    def parse_logical_or(self) -> Expression:
        expr = self.parse_logical_and()

        while self.current_token().type in (TokenType.KO, TokenType.OR):
            op_tok = self.advance()
            right = self.parse_logical_and()
            expr = LogicalOp(start_pos=expr.start_pos, end_pos=right.end_pos, left=expr, operator=op_tok, right=right)

        return expr

    def parse_logical_and(self) -> Expression:
        expr = self.parse_equality()

        while self.current_token().type in (TokenType.KUMA, TokenType.AND):
            op_tok = self.advance()
            right = self.parse_equality()
            expr = LogicalOp(start_pos=expr.start_pos, end_pos=right.end_pos, left=expr, operator=op_tok, right=right)

        return expr

    def parse_equality(self) -> Expression:
        expr = self.parse_comparison()

        while self.current_token().type in (TokenType.EQUAL, TokenType.NOT_EQUAL):
            op_tok = self.advance()
            right = self.parse_comparison()
            expr = BinaryOp(start_pos=expr.start_pos, end_pos=right.end_pos, left=expr, operator=op_tok, right=right)

        return expr

    def parse_comparison(self) -> Expression:
        expr = self.parse_term()

        while self.current_token().type in (TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL):
            op_tok = self.advance()
            right = self.parse_term()
            expr = BinaryOp(start_pos=expr.start_pos, end_pos=right.end_pos, left=expr, operator=op_tok, right=right)

        return expr

    def parse_term(self) -> Expression:
        expr = self.parse_factor()

        while self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            op_tok = self.advance()
            right = self.parse_factor()
            expr = BinaryOp(start_pos=expr.start_pos, end_pos=right.end_pos, left=expr, operator=op_tok, right=right)

        return expr

    def parse_factor(self) -> Expression:
        expr = self.parse_power()

        while self.current_token().type in (TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op_tok = self.advance()
            right = self.parse_power()
            expr = BinaryOp(start_pos=expr.start_pos, end_pos=right.end_pos, left=expr, operator=op_tok, right=right)

        return expr

    def parse_power(self) -> Expression:
        expr = self.parse_unary()

        if self.current_token().type == TokenType.POW:
            op_tok = self.advance()
            right = self.parse_power()  # Right-associative
            return BinaryOp(start_pos=expr.start_pos, end_pos=right.end_pos, left=expr, operator=op_tok, right=right)

        return expr

    def parse_unary(self) -> Expression:
        if self.current_token().type in (TokenType.MINUS, TokenType.NOT, TokenType.BA):
            op_tok = self.advance()
            operand = self.parse_unary()
            return UnaryOp(start_pos=op_tok.start_pos, end_pos=operand.end_pos, operator=op_tok, operand=operand)

        return self.parse_call_and_indexing()

    def parse_call_and_indexing(self) -> Expression:
        expr = self.parse_primary()

        while True:
            # Function Call: func(a, b)
            if self.current_token().type == TokenType.LPAREN:
                self.advance()
                args: List[Expression] = []
                if self.current_token().type != TokenType.RPAREN:
                    while True:
                        args.append(self.parse_expression())
                        if not self.match(TokenType.COMMA):
                            break
                rparen = self.expect(TokenType.RPAREN, "Ana bukatar ')' a karshen kiran aiki")
                expr = CallExpr(start_pos=expr.start_pos, end_pos=rparen.end_pos, callee=expr, arguments=args)

            # Indexing or Slicing: arr[0] ko arr[0:5]
            elif self.current_token().type == TokenType.LBRACKET:
                self.advance()
                
                # Check slice starting with colon: arr[:5]
                if self.match(TokenType.COLON):
                    stop_expr = self.parse_expression() if self.current_token().type not in (TokenType.RBRACKET, TokenType.COLON) else None
                    step_expr = None
                    if self.match(TokenType.COLON):
                        step_expr = self.parse_expression() if self.current_token().type != TokenType.RBRACKET else None
                    rbrack = self.expect(TokenType.RBRACKET, "Ana bukatar ']' a karshen yankin jeri")
                    expr = SliceExpr(start_pos=expr.start_pos, end_pos=rbrack.end_pos, target=expr, start=None, stop=stop_expr, step=step_expr)
                else:
                    first_expr = self.parse_expression()
                    if self.match(TokenType.COLON):
                        stop_expr = self.parse_expression() if self.current_token().type not in (TokenType.RBRACKET, TokenType.COLON) else None
                        step_expr = None
                        if self.match(TokenType.COLON):
                            step_expr = self.parse_expression() if self.current_token().type != TokenType.RBRACKET else None
                        rbrack = self.expect(TokenType.RBRACKET, "Ana bukatar ']' a karshen yankin jeri")
                        expr = SliceExpr(start_pos=expr.start_pos, end_pos=rbrack.end_pos, target=expr, start=first_expr, stop=stop_expr, step=step_expr)
                    else:
                        rbrack = self.expect(TokenType.RBRACKET, "Ana bukatar ']' bayan matsayin jeri")
                        expr = IndexExpr(start_pos=expr.start_pos, end_pos=rbrack.end_pos, target=expr, index=first_expr)

            # Dot notation for properties / methods: obj.property
            elif self.current_token().type == TokenType.DOT:
                self.advance()
                prop_tok = self.expect(TokenType.IDENTIFIER, "Ana bukatar sunan dukiya ko aiki bayan '.'")
                prop_literal = Literal(start_pos=prop_tok.start_pos, end_pos=prop_tok.end_pos, value=str(prop_tok.value), raw=str(prop_tok.value))
                expr = IndexExpr(start_pos=expr.start_pos, end_pos=prop_tok.end_pos, target=expr, index=prop_literal)

            else:
                break

        return expr

    def parse_primary(self) -> Expression:
        tok = self.current_token()

        # Numbers
        if tok.type == TokenType.NUMBER:
            self.advance()
            return Literal(start_pos=tok.start_pos, end_pos=tok.end_pos, value=tok.value, raw=str(tok.value))

        # Strings
        if tok.type == TokenType.STRING:
            self.advance()
            return Literal(start_pos=tok.start_pos, end_pos=tok.end_pos, value=tok.value, raw=f'"{tok.value}"')

        # Booleans: gaskiya (true), karya (false)
        if tok.type == TokenType.GASKIYA:
            self.advance()
            return Literal(start_pos=tok.start_pos, end_pos=tok.end_pos, value=True, raw="gaskiya")

        if tok.type == TokenType.KARYA:
            self.advance()
            return Literal(start_pos=tok.start_pos, end_pos=tok.end_pos, value=False, raw="karya")

        # Null: babu
        if tok.type == TokenType.BABU:
            self.advance()
            return Literal(start_pos=tok.start_pos, end_pos=tok.end_pos, value=None, raw="babu")

        # Identifiers
        if tok.type == TokenType.IDENTIFIER:
            self.advance()
            return Identifier(start_pos=tok.start_pos, end_pos=tok.end_pos, name=str(tok.value))

        # Grouping: ( expr )
        if tok.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN, "Ana bukatar ')' domin rufe lissafi")
            return expr

        # List Literal: [1, 2, "uku"]
        if tok.type == TokenType.LBRACKET:
            start_tok = self.advance()
            elements: List[Expression] = []
            self.skip_newlines()
            if self.current_token().type != TokenType.RBRACKET:
                while True:
                    self.skip_newlines()
                    elements.append(self.parse_expression())
                    self.skip_newlines()
                    if not self.match(TokenType.COMMA):
                        break
            self.skip_newlines()
            end_tok = self.expect(TokenType.RBRACKET, "Ana bukatar ']' a karshen jeri")
            return ListLiteral(start_pos=start_tok.start_pos, end_pos=end_tok.end_pos, elements=elements)

        # Dict Literal: {"suna": "Aliyu", "shekaru": 25}
        if tok.type == TokenType.LBRACE:
            start_tok = self.advance()
            pairs: List[Tuple[Expression, Expression]] = []
            self.skip_newlines()
            if self.current_token().type != TokenType.RBRACE:
                while True:
                    self.skip_newlines()
                    # Key can be string, identifier, or expression
                    key_expr = self.parse_expression()
                    self.expect(TokenType.COLON, "Ana bukatar ':' tsakanin makulli da daraja a kamus")
                    val_expr = self.parse_expression()
                    pairs.append((key_expr, val_expr))
                    self.skip_newlines()
                    if not self.match(TokenType.COMMA):
                        break
            self.skip_newlines()
            end_tok = self.expect(TokenType.RBRACE, "Ana bukatar '}' a karshen kamus")
            return DictLiteral(start_pos=start_tok.start_pos, end_pos=end_tok.end_pos, pairs=pairs)

        # Anonymous Function: aiki(x, y) { ... }
        if tok.type == TokenType.AIKI:
            start_tok = self.advance()
            self.expect(TokenType.LPAREN, "Ana bukatar '(' a aiki marar suna")
            params: List[Tuple[str, Optional[str]]] = []
            if self.current_token().type != TokenType.RPAREN:
                while True:
                    p_tok = self.expect(TokenType.IDENTIFIER, "Ana bukatar sunan ma'auni")
                    p_name = str(p_tok.value)
                    p_type = None
                    if self.match(TokenType.COLON):
                        pt_tok = self.expect(TokenType.IDENTIFIER, "Ana bukatar sunan nau'i")
                        p_type = str(pt_tok.value)
                    params.append((p_name, p_type))
                    if not self.match(TokenType.COMMA):
                        break
            self.expect(TokenType.RPAREN, "Ana bukatar ')' bayan ma'aunan aiki")
            self.skip_newlines()
            body = self.parse_block()
            return AnonymousFunction(start_pos=start_tok.start_pos, end_pos=body.end_pos, params=params, body=body)

        raise KuskurenNahawu(
            f"Alamar da ba a zata ba a nan: '{tok.value if tok.value is not None else tok.type.name}'",
            tok.start_pos, tok.end_pos, self.source_code
        )

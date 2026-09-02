"""
Gwaje-gwajen Mai Nazarin Nahawu (Parser Unit Tests)
"""

import unittest
from harshe.lexer import Lexer
from harshe.parser import Parser
from harshe.ast_nodes import (
    VariableDecl, IfStatement, WhileStatement, ForStatement,
    FunctionDecl, ReturnStatement, TryCatchStatement, BinaryOp,
    Literal, Identifier, CallExpr, ListLiteral, DictLiteral
)


class TestParser(unittest.TestCase):

    def parse_code(self, code: str):
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens, code)
        return parser.parse()

    def test_variable_declarations(self):
        ast = self.parse_code("bari x = 10; tsayayye PI = 3.14; saka suna: rubutu = 'Aliyu';")
        self.assertEqual(len(ast.statements), 3)
        self.assertIsInstance(ast.statements[0], VariableDecl)
        self.assertEqual(ast.statements[0].name, "x")
        self.assertFalse(ast.statements[0].is_const)

        self.assertIsInstance(ast.statements[1], VariableDecl)
        self.assertEqual(ast.statements[1].name, "PI")
        self.assertTrue(ast.statements[1].is_const)

        self.assertIsInstance(ast.statements[2], VariableDecl)
        self.assertEqual(ast.statements[2].name, "suna")
        self.assertEqual(ast.statements[2].type_hint, "rubutu")

    def test_if_elif_else(self):
        code = """
        idan (x > 10) {
            buga("Babba");
        } ko idan (x == 10) {
            buga("Daidai");
        } in ba haka ba {
            buga("Kankane");
        }
        """
        ast = self.parse_code(code)
        self.assertEqual(len(ast.statements), 1)
        self.assertIsInstance(ast.statements[0], IfStatement)
        stmt = ast.statements[0]
        self.assertEqual(len(stmt.elif_branches), 1)
        self.assertIsNotNone(stmt.else_branch)

    def test_loops(self):
        code = """
        yayin da (i < 5) {
            i += 1;
        }
        ga dabba a cikin jerin_dabbobi {
            buga(dabba);
        }
        """
        ast = self.parse_code(code)
        self.assertEqual(len(ast.statements), 2)
        self.assertIsInstance(ast.statements[0], WhileStatement)
        self.assertIsInstance(ast.statements[1], ForStatement)

    def test_function_decl(self):
        code = """
        aiki tara(a: lamba, b: lamba) -> lamba {
            koma a + b;
        }
        """
        ast = self.parse_code(code)
        self.assertEqual(len(ast.statements), 1)
        self.assertIsInstance(ast.statements[0], FunctionDecl)
        fn = ast.statements[0]
        self.assertEqual(fn.name, "tara")
        self.assertEqual(len(fn.params), 2)
        self.assertEqual(fn.return_type_hint, "lamba")
        self.assertIsInstance(fn.body.statements[0], ReturnStatement)

    def test_try_catch(self):
        code = """
        gwada {
            bari x = 10 / 0;
        } kama (kuskure) {
            buga(kuskure);
        }
        """
        ast = self.parse_code(code)
        self.assertEqual(len(ast.statements), 1)
        self.assertIsInstance(ast.statements[0], TryCatchStatement)
        tc = ast.statements[0]
        self.assertEqual(tc.error_var, "kuskure")


if __name__ == "__main__":
    unittest.main()

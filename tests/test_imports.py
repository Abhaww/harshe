"""
Gwaje-gwajen Shigo da Laburare (Import System Unit Tests)
"""

import unittest
from harshe import run_source


class TestImports(unittest.TestCase):

    def test_stdlib_math_import(self):
        code = """
        shigo_da "lissafi";
        koma matsakaici([10, 20, 30]);
        """
        res = run_source(code)
        self.assertEqual(res.value, 20)

    def test_from_import_syntax(self):
        code = """
        daga "rubutu" shigo_da juya_rubutu, ko_palindrome_ne;
        bari j = juya_rubutu("harshe");
        koma j;
        """
        res = run_source(code)
        self.assertEqual(res.value, "ehsrah")

    def test_random_and_json_builtins(self):
        code = """
        bari j_str = '{"a": 10, "b": 20}';
        bari k = karanta_json(j_str);
        koma k["a"] + k["b"];
        """
        res = run_source(code)
        self.assertEqual(res.value, 30)


if __name__ == "__main__":
    unittest.main()

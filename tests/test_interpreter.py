"""
Gwaje-gwajen Injin Gudanarwa (Interpreter Unit Tests)
"""

import unittest
from harshe import run_source
from harshe.values import HarsheNumber, HarsheString, HarsheBoolean, HarsheList, HarsheDict, HarsheNull
from harshe.errors import KuskurenNaui, KuskurenSuna, KuskurenLissafi, KuskurenMatsayi


class TestInterpreter(unittest.TestCase):

    def test_arithmetic_and_precedence(self):
        self.assertEqual(run_source("koma 2 + 3 * 4;").value, 14)
        self.assertEqual(run_source("koma (2 + 3) * 4;").value, 20)
        self.assertEqual(run_source("koma 2 ** 3;").value, 8)
        self.assertEqual(run_source("koma 10 - 4 - 2;").value, 4)
        self.assertEqual(run_source("koma 15 % 4;").value, 3)

    def test_strings_and_concatenation(self):
        self.assertEqual(run_source('koma "Sannu " + "Duniya";').value, "Sannu Duniya")
        self.assertEqual(run_source('koma "Shekaru: " + 25;').value, "Shekaru: 25")
        self.assertEqual(run_source('koma "ABC" * 3;').value, "ABCABCABC")

    def test_variables_and_constants(self):
        code = """
        bari x = 10;
        x += 5;
        tsayayye Y = 50;
        koma x + Y;
        """
        self.assertEqual(run_source(code).value, 65)

    def test_const_reassignment_error(self):
        code = """
        tsayayye KASA = "Nigeria";
        KASA = "Ghana";
        """
        with self.assertRaises(KuskurenNaui):
            run_source(code)

    def test_conditionals(self):
        code = """
        bari x = 15;
        bari sakamako = "";
        idan (x > 20) {
            sakamako = "Babba";
        } ko idan (x > 10) {
            sakamako = "Matsakaici";
        } in ba haka ba {
            sakamako = "Kankane";
        }
        koma sakamako;
        """
        self.assertEqual(run_source(code).value, "Matsakaici")

    def test_loops_and_controls(self):
        code = """
        bari sum = 0;
        ga i a cikin kewayon(1, 11) {
            idan (i == 5) {
                ci_gaba;
            }
            idan (i == 9) {
                tsaya;
            }
            sum += i;
        }
        koma sum;
        """
        # Sum of 1, 2, 3, 4, (skip 5), 6, 7, 8 = 31
        self.assertEqual(run_source(code).value, 31)

    def test_functions_and_recursion(self):
        code = """
        aiki factorial(n) {
            idan (n <= 1) {
                koma 1;
            }
            koma n * factorial(n - 1);
        }
        koma factorial(5);
        """
        self.assertEqual(run_source(code).value, 120)

    def test_closures(self):
        code = """
        aiki mai_karawa(n) {
            aiki kara(x) {
                koma x + n;
            }
            koma kara;
        }
        bari kara5 = mai_karawa(5);
        koma kara5(20);
        """
        self.assertEqual(run_source(code).value, 25)

    def test_lists_and_indexing(self):
        code = """
        bari j = [10, 20, 30];
        kara(j, 40);
        j[1] = 99;
        koma j;
        """
        res = run_source(code)
        self.assertIsInstance(res, HarsheList)
        self.assertEqual([v.value for v in res.elements], [10, 99, 30, 40])

    def test_dictionaries(self):
        code = """
        bari kamus = {"suna": "Aliyu", "maki": 90};
        kamus["maki"] += 5;
        koma kamus["maki"];
        """
        self.assertEqual(run_source(code).value, 95)

    def test_try_catch(self):
        code = """
        bari sakamako = "";
        gwada {
            bari a = 10 / 0;
        } kama (kuskure) {
            sakamako = "An kama kuskuren lissafi";
        }
        koma sakamako;
        """
        self.assertEqual(run_source(code).value, "An kama kuskuren lissafi")

    def test_type_hint_validation(self):
        code = """
        bari x: lamba = "ba lamba ba";
        """
        with self.assertRaises(KuskurenNaui):
            run_source(code)

    def test_math_error_zero_division(self):
        with self.assertRaises(KuskurenLissafi):
            run_source("bari x = 10 / 0;")


if __name__ == "__main__":
    unittest.main()

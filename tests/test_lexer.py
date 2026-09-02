"""
Gwaje-gwajen Mai Binciken Alamomi (Lexer Unit Tests)
"""

import unittest
from harshe.tokens import TokenType
from harshe.lexer import Lexer
from harshe.errors import KuskurenNahawu


class TestLexer(unittest.TestCase):

    def test_keywords_single_word(self):
        code = "bari saka tsayayye idan aiki koma tsaya ci_gaba gwada kama gaskiya karya babu kuma ko ba ga"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens if t.type != TokenType.EOF]
        expected = [
            TokenType.BARI, TokenType.SAKA, TokenType.TSAYAYYE, TokenType.IDAN,
            TokenType.AIKI, TokenType.KOMA, TokenType.TSAYA, TokenType.CI_GABA,
            TokenType.GWADA, TokenType.KAMA, TokenType.GASKIYA, TokenType.KARYA,
            TokenType.BABU, TokenType.KUMA, TokenType.KO, TokenType.BA, TokenType.GA
        ]
        self.assertEqual(types, expected)

    def test_multiword_keywords(self):
        code = "ko idan in ba haka ba yayin da a cikin ci gaba"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens if t.type != TokenType.EOF]
        expected = [
            TokenType.KO_IDAN,
            TokenType.IN_BA_HAKA_BA,
            TokenType.YAYIN_DA,
            TokenType.A_CIKIN,
            TokenType.CI_GABA,
        ]
        self.assertEqual(types, expected)

    def test_numbers_and_strings(self):
        code = '42 3.14159 "Sannu Duniya" \'Hausa\' "Layi 1\\nLayi 2"'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].value, 42)
        self.assertEqual(tokens[1].value, 3.14159)
        self.assertEqual(tokens[2].value, "Sannu Duniya")
        self.assertEqual(tokens[3].value, "Hausa")
        self.assertEqual(tokens[4].value, "Layi 1\nLayi 2")

    def test_operators(self):
        code = "+ - * / % ** ^ = += -= *= /= == != < <= > >= && || !"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens if t.type != TokenType.EOF]
        expected = [
            TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH, TokenType.PERCENT,
            TokenType.POW, TokenType.POW, TokenType.ASSIGN, TokenType.PLUS_ASSIGN,
            TokenType.MINUS_ASSIGN, TokenType.STAR_ASSIGN, TokenType.SLASH_ASSIGN,
            TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL,
            TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.AND, TokenType.OR, TokenType.NOT
        ]
        self.assertEqual(types, expected)

    def test_comments(self):
        code = """
        # Wannan sharhi ne
        bari x = 10; // Sharhi na biyu
        /* Sharhi
           mai layuka da yawa */
        bari y = 20;
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.EOF)]
        expected = [
            TokenType.BARI, TokenType.IDENTIFIER, TokenType.ASSIGN, TokenType.NUMBER, TokenType.SEMICOLON,
            TokenType.BARI, TokenType.IDENTIFIER, TokenType.ASSIGN, TokenType.NUMBER, TokenType.SEMICOLON,
        ]
        self.assertEqual(types, expected)

    def test_unclosed_string_error(self):
        with self.assertRaises(KuskurenNahawu):
            lexer = Lexer('"Ba a rufe wannan rubutun ba')
            lexer.tokenize()


if __name__ == "__main__":
    unittest.main()

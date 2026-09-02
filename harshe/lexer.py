"""
Harshe - Tsarin Binciken Alamomi (Lexer Module)
Rarraba rubutun harshen Harshe zuwa jerin alamomi (Tokens).
"""

from typing import List, Optional
from .tokens import Token, TokenType, Position, HAUSA_KEYWORDS, MULTIWORD_KEYWORDS
from .errors import KuskurenNahawu


class Lexer:
    """Mai binciken alamomin Harshe (Harshe Lexer / Tokenizer)"""

    def __init__(self, source: str, filename: str = "<shigarwa>"):
        self.source = source
        self.filename = filename
        self.pos = Position(1, 1, 0, filename)
        self.current_char: Optional[str] = self.source[0] if len(self.source) > 0 else None

    def advance(self) -> None:
        """Ci gaba zuwa harafi na gaba"""
        self.pos.advance(self.current_char)
        if self.pos.index < len(self.source):
            self.current_char = self.source[self.pos.index]
        else:
            self.current_char = None

    def peek(self, offset: int = 1) -> Optional[str]:
        """Duba harafi na gaba ba tare da motsawa ba"""
        target_idx = self.pos.index + offset
        if target_idx < len(self.source):
            return self.source[target_idx]
        return None

    def tokenize(self) -> List[Token]:
        """Bincika duk rubutun kuma samar da jerin alamomi (Tokens)"""
        tokens: List[Token] = []

        while self.current_char is not None:
            # 1. Ketare sarari (Whitespaces except newline)
            if self.current_char in ' \t\r':
                self.advance()
                continue

            # 2. Sabon layi (Newlines)
            if self.current_char == '\n':
                start_pos = self.pos.copy()
                self.advance()
                tokens.append(Token(TokenType.NEWLINE, '\n', start_pos, self.pos.copy()))
                continue

            # 3. Sharhi (Comments: # ko // ko /* ... */)
            if self.current_char == '#':
                self.skip_single_line_comment()
                continue

            if self.current_char == '/' and self.peek() == '/':
                self.advance()
                self.advance()
                self.skip_single_line_comment()
                continue

            if self.current_char == '/' and self.peek() == '*':
                self.skip_multi_line_comment()
                continue

            # 4. Lambobi (Numbers: Integers & Floats)
            if self.current_char.isdigit():
                tokens.append(self.make_number())
                continue

            # 5. Rubutu a cikin alamar zance (Strings: "..." ko '...')
            if self.current_char in ('"', "'"):
                tokens.append(self.make_string())
                continue

            # 6. Haruffan sunaye ko kalmomin aiki (Identifiers & Keywords)
            if self.current_char.isalpha() or self.current_char in ('_', '`'):
                token = self.make_identifier_or_keyword()
                tokens.append(token)
                continue

            # 7. Masu aiki da alamomin rarrabewa (Operators & Punctuation)
            start_pos = self.pos.copy()

            # Biyu-biyu masu aiki (Two-character operators)
            if self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.EQUAL, "==", start_pos, self.pos.copy()))
            elif self.current_char == '!' and self.peek() == '=':
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.NOT_EQUAL, "!=", start_pos, self.pos.copy()))
            elif self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.LESS_EQUAL, "<=", start_pos, self.pos.copy()))
            elif self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.GREATER_EQUAL, ">=", start_pos, self.pos.copy()))
            elif self.current_char == '+' and self.peek() == '=':
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.PLUS_ASSIGN, "+=", start_pos, self.pos.copy()))
            elif self.current_char == '-' and self.peek() == '=':
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.MINUS_ASSIGN, "-=", start_pos, self.pos.copy()))
            elif self.current_char == '*' and self.peek() == '=':
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.STAR_ASSIGN, "*=", start_pos, self.pos.copy()))
            elif self.current_char == '/' and self.peek() == '=':
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.SLASH_ASSIGN, "/=", start_pos, self.pos.copy()))
            elif self.current_char == '*' and self.peek() == '*':
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.POW, "**", start_pos, self.pos.copy()))
            elif self.current_char == '&' and self.peek() == '&':
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.AND, "&&", start_pos, self.pos.copy()))
            elif self.current_char == '|' and self.peek() == '|':
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.OR, "||", start_pos, self.pos.copy()))
            elif self.current_char == '-' and self.peek() == '>':
                self.advance()
                self.advance()
                tokens.append(Token(TokenType.ARROW, "->", start_pos, self.pos.copy()))

            # Masu aiki guda daya (Single-character operators)
            elif self.current_char == '+':
                self.advance()
                tokens.append(Token(TokenType.PLUS, "+", start_pos, self.pos.copy()))
            elif self.current_char == '-':
                self.advance()
                tokens.append(Token(TokenType.MINUS, "-", start_pos, self.pos.copy()))
            elif self.current_char == '*':
                self.advance()
                tokens.append(Token(TokenType.STAR, "*", start_pos, self.pos.copy()))
            elif self.current_char == '/':
                self.advance()
                tokens.append(Token(TokenType.SLASH, "/", start_pos, self.pos.copy()))
            elif self.current_char == '%':
                self.advance()
                tokens.append(Token(TokenType.PERCENT, "%", start_pos, self.pos.copy()))
            elif self.current_char == '^':
                self.advance()
                tokens.append(Token(TokenType.POW, "^", start_pos, self.pos.copy()))
            elif self.current_char == '=':
                self.advance()
                tokens.append(Token(TokenType.ASSIGN, "=", start_pos, self.pos.copy()))
            elif self.current_char == '<':
                self.advance()
                tokens.append(Token(TokenType.LESS, "<", start_pos, self.pos.copy()))
            elif self.current_char == '>':
                self.advance()
                tokens.append(Token(TokenType.GREATER, ">", start_pos, self.pos.copy()))
            elif self.current_char == '!':
                self.advance()
                tokens.append(Token(TokenType.NOT, "!", start_pos, self.pos.copy()))

            # Alamomin shafi da rarrabewa (Delimiters)
            elif self.current_char == '(':
                self.advance()
                tokens.append(Token(TokenType.LPAREN, "(", start_pos, self.pos.copy()))
            elif self.current_char == ')':
                self.advance()
                tokens.append(Token(TokenType.RPAREN, ")", start_pos, self.pos.copy()))
            elif self.current_char == '{':
                self.advance()
                tokens.append(Token(TokenType.LBRACE, "{", start_pos, self.pos.copy()))
            elif self.current_char == '}':
                self.advance()
                tokens.append(Token(TokenType.RBRACE, "}", start_pos, self.pos.copy()))
            elif self.current_char == '[':
                self.advance()
                tokens.append(Token(TokenType.LBRACKET, "[", start_pos, self.pos.copy()))
            elif self.current_char == ']':
                self.advance()
                tokens.append(Token(TokenType.RBRACKET, "]", start_pos, self.pos.copy()))
            elif self.current_char == ',':
                self.advance()
                tokens.append(Token(TokenType.COMMA, ",", start_pos, self.pos.copy()))
            elif self.current_char == ':':
                self.advance()
                tokens.append(Token(TokenType.COLON, ":", start_pos, self.pos.copy()))
            elif self.current_char == ';':
                self.advance()
                tokens.append(Token(TokenType.SEMICOLON, ";", start_pos, self.pos.copy()))
            elif self.current_char == '.':
                self.advance()
                tokens.append(Token(TokenType.DOT, ".", start_pos, self.pos.copy()))
            else:
                char = self.current_char
                pos = self.pos.copy()
                self.advance()
                raise KuskurenNahawu(
                    f"Harafin da ba a sani ba: '{char}'",
                    pos, self.pos.copy(), self.source
                )

        # Hada kalmomi masu kalmomi biyu ko fiye (Multi-word phrase post-processing)
        tokens = self.combine_multiword_tokens(tokens)

        # Sanya alamar karshen fayil (EOF)
        tokens.append(Token(TokenType.EOF, None, self.pos.copy(), self.pos.copy()))
        return tokens

    def skip_single_line_comment(self) -> None:
        while self.current_char is not None and self.current_char != '\n':
            self.advance()

    def skip_multi_line_comment(self) -> None:
        start_pos = self.pos.copy()
        self.advance()  # /
        self.advance()  # *
        while self.current_char is not None:
            if self.current_char == '*' and self.peek() == '/':
                self.advance()
                self.advance()
                return
            self.advance()
        raise KuskurenNahawu(
            "Ba a rufe sharhi mai layuka da yawa (/* ... */) ba kafin karshen fayil",
            start_pos, self.pos.copy(), self.source
        )

    def make_number(self) -> Token:
        start_pos = self.pos.copy()
        num_str = ""
        dot_count = 0

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if dot_count == 1:
                    break
                if self.peek() is not None and not self.peek().isdigit():
                    break
                dot_count += 1
            num_str += self.current_char
            self.advance()

        val = float(num_str) if dot_count == 1 else int(num_str)
        return Token(TokenType.NUMBER, val, start_pos, self.pos.copy())

    def make_string(self) -> Token:
        start_pos = self.pos.copy()
        quote_char = self.current_char
        self.advance()

        str_val = ""
        escape_map = {
            'n': '\n',
            't': '\t',
            'r': '\r',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }

        while self.current_char is not None and self.current_char != quote_char:
            if self.current_char == '\\':
                self.advance()
                if self.current_char in escape_map:
                    str_val += escape_map[self.current_char]
                elif self.current_char is not None:
                    str_val += self.current_char
                else:
                    break
            else:
                str_val += self.current_char
            self.advance()

        if self.current_char != quote_char:
            raise KuskurenNahawu(
                f"Ba a rufe alamar zance '{quote_char}' na rubutu ba",
                start_pos, self.pos.copy(), self.source
            )

        self.advance()  # pass quote
        return Token(TokenType.STRING, str_val, start_pos, self.pos.copy())

    def make_identifier_or_keyword(self) -> Token:
        start_pos = self.pos.copy()
        ident_str = ""

        # Hausa words can have apostrophes like nau'i, dabi'a, or underscores
        while self.current_char is not None and (
            self.current_char.isalnum() or 
            self.current_char in ('_', "'")
        ):
            ident_str += self.current_char
            self.advance()

        # Check single-word keyword or normalized variant
        normalized = ident_str.lower()
        if normalized in HAUSA_KEYWORDS:
            return Token(HAUSA_KEYWORDS[normalized], ident_str, start_pos, self.pos.copy())
        
        # Check if single word matches special multi-word keywords joined with underscores
        if normalized in ("ko_idan", "koidan"):
            return Token(TokenType.KO_IDAN, "ko idan", start_pos, self.pos.copy())
        if normalized in ("in_ba_haka_ba", "inbahakaba"):
            return Token(TokenType.IN_BA_HAKA_BA, "in ba haka ba", start_pos, self.pos.copy())
        if normalized in ("yayin_da", "yayinda"):
            return Token(TokenType.YAYIN_DA, "yayin da", start_pos, self.pos.copy())
        if normalized in ("a_cikin", "acikin"):
            return Token(TokenType.A_CIKIN, "a cikin", start_pos, self.pos.copy())
        if normalized in ("ci_gaba", "cigaba"):
            return Token(TokenType.CI_GABA, "ci gaba", start_pos, self.pos.copy())
        if normalized in ("shigo_da", "shigoda"):
            return Token(TokenType.SHIGO_DA, "shigo da", start_pos, self.pos.copy())

        return Token(TokenType.IDENTIFIER, ident_str, start_pos, self.pos.copy())

    def combine_multiword_tokens(self, tokens: List[Token]) -> List[Token]:
        """Combine multi-word keywords like 'in ba haka ba', 'ko idan', 'yayin da', 'a cikin', 'ci gaba', 'shigo da'"""
        combined: List[Token] = []
        i = 0
        n = len(tokens)

        while i < n:
            # Check 4 words: "in ba haka ba"
            if i + 3 < n:
                t0, t1, t2, t3 = tokens[i], tokens[i+1], tokens[i+2], tokens[i+3]
                w0 = str(t0.value).lower() if t0.value else ""
                w1 = str(t1.value).lower() if t1.value else ""
                w2 = str(t2.value).lower() if t2.value else ""
                w3 = str(t3.value).lower() if t3.value else ""
                if (w0 == "in" and w1 == "ba" and w2 == "haka" and w3 == "ba" and
                    t0.type in (TokenType.IDENTIFIER, TokenType.BA) and
                    t1.type in (TokenType.IDENTIFIER, TokenType.BA) and
                    t2.type in (TokenType.IDENTIFIER, TokenType.BA) and
                    t3.type in (TokenType.IDENTIFIER, TokenType.BA)):
                    combined.append(Token(TokenType.IN_BA_HAKA_BA, "in ba haka ba", t0.start_pos, t3.end_pos))
                    i += 4
                    continue

            # Check 2 words: "ko idan", "yayin da", "a cikin", "ci gaba", "shigo da"
            if i + 1 < n:
                t0, t1 = tokens[i], tokens[i+1]
                w0 = str(t0.value).lower() if t0.value else ""
                w1 = str(t1.value).lower() if t1.value else ""

                if (w0 == "ko" and w1 == "idan") and (t0.type in (TokenType.IDENTIFIER, TokenType.KO) and t1.type in (TokenType.IDENTIFIER, TokenType.IDAN)):
                    combined.append(Token(TokenType.KO_IDAN, "ko idan", t0.start_pos, t1.end_pos))
                    i += 2
                    continue
                if (w0 == "yayin" and w1 == "da") and (t0.type == TokenType.IDENTIFIER and t1.type == TokenType.IDENTIFIER):
                    combined.append(Token(TokenType.YAYIN_DA, "yayin da", t0.start_pos, t1.end_pos))
                    i += 2
                    continue
                if (w0 == "a" and w1 == "cikin") and (t0.type == TokenType.IDENTIFIER and t1.type == TokenType.IDENTIFIER):
                    combined.append(Token(TokenType.A_CIKIN, "a cikin", t0.start_pos, t1.end_pos))
                    i += 2
                    continue
                if (w0 == "ci" and w1 == "gaba") and (t0.type == TokenType.IDENTIFIER and t1.type == TokenType.IDENTIFIER):
                    combined.append(Token(TokenType.CI_GABA, "ci gaba", t0.start_pos, t1.end_pos))
                    i += 2
                    continue
                if (w0 == "shigo" and w1 == "da") and (t0.type == TokenType.IDENTIFIER and t1.type == TokenType.IDENTIFIER):
                    combined.append(Token(TokenType.SHIGO_DA, "shigo da", t0.start_pos, t1.end_pos))
                    i += 2
                    continue

            combined.append(tokens[i])
            i += 1

        return combined

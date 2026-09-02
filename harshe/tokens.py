"""
Harshe - Tsarin Alamomi (Tokens Module)
Maganar alamomin harshen Harshe (Hausa Programming Language)
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional


class TokenType(Enum):
    # Mahimman Kalmomi (Keywords)
    BARI = auto()            # bari (let/var)
    SAKA = auto()            # saka (var alternate)
    TSAYAYYE = auto()        # tsayayye (const)
    IDAN = auto()            # idan (if)
    KO_IDAN = auto()         # ko idan (else if)
    IN_BA_HAKA_BA = auto()   # in ba haka ba (else)
    YAYIN_DA = auto()        # yayin da (while)
    GA = auto()              # ga (for)
    A_CIKIN = auto()         # a cikin (in)
    AIKI = auto()            # aiki (function)
    KOMA = auto()            # koma (return)
    TSAYA = auto()           # tsaya (break)
    CI_GABA = auto()         # ci_gaba (continue)
    GWADA = auto()           # gwada (try)
    KAMA = auto()            # kama (catch)
    GASKIYA = auto()         # gaskiya (true)
    KARYA = auto()           # karya (false)
    BABU = auto()            # babu (null / nil)
    KUMA = auto()            # kuma (and - keyword)
    KO = auto()              # ko (or - keyword)
    BA = auto()              # ba (not - keyword)
    SHIGO_DA = auto()        # shigo_da (import)
    DAGA = auto()            # daga (from)

    # Nau'o'in Daraja (Literals)
    NUMBER = auto()          # 42, 3.14
    STRING = auto()          # "Sannu", 'Duniya'
    IDENTIFIER = auto()      # suna, x, lissafi

    # Masu Aiki (Operators)
    PLUS = auto()            # +
    MINUS = auto()           # -
    STAR = auto()            # *
    SLASH = auto()           # /
    PERCENT = auto()         # %
    POW = auto()             # ** ko ^
    ASSIGN = auto()          # =
    PLUS_ASSIGN = auto()     # +=
    MINUS_ASSIGN = auto()    # -=
    STAR_ASSIGN = auto()     # *=
    SLASH_ASSIGN = auto()    # /=

    # Masu Kwatantawa (Comparison Operators)
    EQUAL = auto()           # ==
    NOT_EQUAL = auto()       # !=
    LESS = auto()            # <
    LESS_EQUAL = auto()      # <=
    GREATER = auto()         # >
    GREATER_EQUAL = auto()   # >=

    # Masu Hada Hukunci (Logical Symbols)
    AND = auto()             # &&
    OR = auto()              # ||
    NOT = auto()             # !

    # Alamomin Rarrabewa (Delimiters / Punctuation)
    LPAREN = auto()          # (
    RPAREN = auto()          # )
    LBRACE = auto()          # {
    RBRACE = auto()          # }
    LBRACKET = auto()        # [
    RBRACKET = auto()        # ]
    COMMA = auto()           # ,
    COLON = auto()           # :
    SEMICOLON = auto()       # ;
    DOT = auto()             # .
    ARROW = auto()           # ->

    # Na Musamman (Special)
    NEWLINE = auto()
    EOF = auto()


@dataclass
class Position:
    """Matsayin alama a cikin rubutun asali (Line & Column tracker)"""
    line: int
    col: int
    index: int
    filename: str = "<shigarwa>"

    def copy(self) -> "Position":
        return Position(self.line, self.col, self.index, self.filename)

    def advance(self, current_char: Optional[str] = None) -> "Position":
        self.index += 1
        if current_char == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return self

    def __str__(self) -> str:
        return f"{self.filename}:{self.line}:{self.col}"


@dataclass
class Token:
    """Alama guda daya (Token representation)"""
    type: TokenType
    value: Any
    start_pos: Position
    end_pos: Position

    def __repr__(self) -> str:
        if self.value is not None:
            return f"Token({self.type.name}, {repr(self.value)}, layi={self.start_pos.line}, jeri={self.start_pos.col})"
        return f"Token({self.type.name}, layi={self.start_pos.line}, jeri={self.start_pos.col})"


# Taswirar kalmomin Hausa zuwa Alamomi (Hausa Keywords Map)
HAUSA_KEYWORDS = {
    "bari": TokenType.BARI,
    "saka": TokenType.SAKA,
    "tsayayye": TokenType.TSAYAYYE,
    "idan": TokenType.IDAN,
    "aiki": TokenType.AIKI,
    "koma": TokenType.KOMA,
    "tsaya": TokenType.TSAYA,
    "ci_gaba": TokenType.CI_GABA,
    "gwada": TokenType.GWADA,
    "kama": TokenType.KAMA,
    "gaskiya": TokenType.GASKIYA,
    "karya": TokenType.KARYA,
    "babu": TokenType.BABU,
    "kuma": TokenType.KUMA,
    "ko": TokenType.KO,
    "ba": TokenType.BA,
    "ga": TokenType.GA,
    "shigo_da": TokenType.SHIGO_DA,
    "daga": TokenType.DAGA,
}

# Kalmomi masu kalmomi biyu ko fiye (Multi-word phrase keywords)
MULTIWORD_KEYWORDS = {
    "ko idan": TokenType.KO_IDAN,
    "in ba haka ba": TokenType.IN_BA_HAKA_BA,
    "yayin da": TokenType.YAYIN_DA,
    "a cikin": TokenType.A_CIKIN,
    "ci gaba": TokenType.CI_GABA,
    "shigo da": TokenType.SHIGO_DA,
}

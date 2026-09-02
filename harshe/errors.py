"""
Harshe - Tsarin Kurakurai da Gargadi (Errors & Diagnostics Module)
Maganar bayyana kuskure a yaren Hausa tare da nuna inda matsalar take a layi.
"""

from typing import Optional
from .tokens import Position


class HarsheError(Exception):
    """Babban kuskure a cikin Harshe (Base Error Class)"""
    def __init__(self, error_name: str, details: str, start_pos: Optional[Position] = None, end_pos: Optional[Position] = None, source_code: Optional[str] = None):
        self.error_name = error_name
        self.details = details
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.source_code = source_code
        super().__init__(self.format_error())

    def format_error(self) -> str:
        filename = self.start_pos.filename if self.start_pos else "<shigarwa>"
        line_num = self.start_pos.line if self.start_pos else 1
        col_num = self.start_pos.col if self.start_pos else 1

        header = f"\n\033[91m[{self.error_name}]\033[0m: {self.details}"
        location = f"\n  \033[90mA cikin fayil:\033[0m {filename}, \033[90mLayi:\033[0m {line_num}, \033[90mJeri:\033[0m {col_num}"

        snippet = ""
        if self.source_code and self.start_pos:
            lines = self.source_code.splitlines()
            if 0 < line_num <= len(lines):
                target_line = lines[line_num - 1]
                line_str = f"{line_num} | "
                indent = len(line_str)
                caret_pos = max(0, col_num - 1)
                
                # Length of underline
                length = 1
                if self.end_pos and self.end_pos.line == line_num:
                    length = max(1, self.end_pos.col - self.start_pos.col)

                snippet = f"\n\n  \033[36m{line_str}\033[0m{target_line}\n  {' ' * indent}{' ' * caret_pos}\033[91m{'^' * length}\033[0m"

        return f"{header}{location}{snippet}\n"

    def __str__(self) -> str:
        return self.format_error()


class KuskurenNahawu(HarsheError):
    """Kuskuren tsari ko nahawun rubutu (Syntax / Parsing / Lexing Error)"""
    def __init__(self, details: str, start_pos: Optional[Position] = None, end_pos: Optional[Position] = None, source_code: Optional[str] = None):
        super().__init__("Kuskuren Nahawu (Syntax Error)", details, start_pos, end_pos, source_code)


class KuskurenSuna(HarsheError):
    """Kuskuren rashin samun mai canji ko aiki (Name / Variable Error)"""
    def __init__(self, details: str, start_pos: Optional[Position] = None, end_pos: Optional[Position] = None, source_code: Optional[str] = None):
        super().__init__("Kuskuren Suna (Name Error)", details, start_pos, end_pos, source_code)


class KuskurenNaui(HarsheError):
    """Kuskuren nau'in bayanai marar dacewa (Type Error)"""
    def __init__(self, details: str, start_pos: Optional[Position] = None, end_pos: Optional[Position] = None, source_code: Optional[str] = None):
        super().__init__("Kuskuren Nau'i (Type Error)", details, start_pos, end_pos, source_code)


class KuskurenLissafi(HarsheError):
    """Kuskuren lissafi kamar raba lamba da sifili (Math Error)"""
    def __init__(self, details: str, start_pos: Optional[Position] = None, end_pos: Optional[Position] = None, source_code: Optional[str] = None):
        super().__init__("Kuskuren Lissafi (Math Error)", details, start_pos, end_pos, source_code)


class KuskurenMatsayi(HarsheError):
    """Kuskuren matsayi a jeri ko kamus (Index / Key Error)"""
    def __init__(self, details: str, start_pos: Optional[Position] = None, end_pos: Optional[Position] = None, source_code: Optional[str] = None):
        super().__init__("Kuskuren Matsayi (Index / Key Error)", details, start_pos, end_pos, source_code)


class KuskurenAiki(HarsheError):
    """Kuskure yayin gudanar da aiki (Runtime Error)"""
    def __init__(self, details: str, start_pos: Optional[Position] = None, end_pos: Optional[Position] = None, source_code: Optional[str] = None):
        super().__init__("Kuskuren Aiki (Runtime Error)", details, start_pos, end_pos, source_code)


# Alamomin Tsara Gudu (Control Flow Signals - not actual errors)
class KomaSignal(Exception):
    """Alamar komar da daraja daga aiki (Return Statement Signal)"""
    def __init__(self, value):
        self.value = value


class TsayaSignal(Exception):
    """Alamar tsayar da madauki (Break Loop Signal)"""
    pass


class CiGabaSignal(Exception):
    """Alamar ci gaba da madauki na gaba (Continue Loop Signal)"""
    pass

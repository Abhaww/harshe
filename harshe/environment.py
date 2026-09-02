"""
Harshe - Muhallin Ma'aji (Environment & Lexical Scope Module)
Kula da ma'ajiyar sunaye, masu canji, tsayayyu da iyakokin aiki (Scoping).
"""

from typing import Dict, Optional, Any
from dataclasses import dataclass
from .values import HarsheValue, HarsheNull
from .errors import KuskurenSuna, KuskurenNaui


@dataclass
class Symbol:
    """Bayanin mai canji (Symbol Entry)"""
    value: HarsheValue
    is_const: bool = False
    type_hint: Optional[str] = None


class Environment:
    """Muhallin ma'aji na Harshe (Lexical Scope Environment)"""

    def __init__(self, parent: Optional["Environment"] = None):
        self.parent: Optional[Environment] = parent
        self.symbols: Dict[str, Symbol] = {}

    def define(self, name: str, value: HarsheValue, is_const: bool = False, type_hint: Optional[str] = None) -> None:
        """Sanar da sabon mai canji ko tsayayye a cikin wannan muhallin"""
        # Type check if type_hint provided
        if type_hint is not None and not isinstance(value, HarsheNull):
            self._check_type(name, value, type_hint)

        self.symbols[name] = Symbol(value=value, is_const=is_const, type_hint=type_hint)

    def assign(self, name: str, value: HarsheValue) -> None:
        """Sauya darajar mai canji da aka riga aka sanar"""
        if name in self.symbols:
            symbol = self.symbols[name]
            if symbol.is_const:
                raise KuskurenNaui(
                    f"Ba za a iya sauya darajar tsayayye '{name}' ba domin ba mai canzawa ba ne (tsayayye ne)."
                )
            if symbol.type_hint is not None and not isinstance(value, HarsheNull):
                self._check_type(name, value, symbol.type_hint)
            symbol.value = value
            return

        if self.parent is not None:
            self.parent.assign(name, value)
            return

        raise KuskurenSuna(f"Ba a gano mai canji mai suna '{name}' ba da za a sauya masa daraja.")

    def get(self, name: str) -> HarsheValue:
        """Nemo darajar mai canji ta sunansa"""
        if name in self.symbols:
            return self.symbols[name].value

        if self.parent is not None:
            return self.parent.get(name)

        raise KuskurenSuna(f"Ba a gano mai canji ko aiki mai suna '{name}' ba.")

    def exists(self, name: str) -> bool:
        """Duba ko akwai mai canji mai wannan sunan"""
        if name in self.symbols:
            return True
        if self.parent is not None:
            return self.parent.exists(name)
        return False

    def _check_type(self, name: str, value: HarsheValue, expected_type: str) -> None:
        """Tabbatar da nau'in bayanai (Type checking helper)"""
        type_mapping = {
            "lamba": ("lamba",),
            "rubutu": ("rubutu",),
            "dabi'a": ("dabi'a",),
            "dabia": ("dabi'a",),
            "jeri": ("jeri",),
            "kamus": ("kamus",),
            "aiki": ("aiki", "aiki_na_ciki"),
        }
        val_type = value.type_name
        allowed = type_mapping.get(expected_type.lower(), (expected_type.lower(),))
        if val_type not in allowed:
            raise KuskurenNaui(
                f"Nau'in darajar '{name}' ba daidai ba ne: ana bukatar '{expected_type}', amma an sami '{val_type}' ({value.harshe_repr()})"
            )

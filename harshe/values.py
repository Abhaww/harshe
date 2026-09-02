"""
Harshe - Darajojin Aiki (Runtime Values Module)
Nau'o'in bayanai da darajoji a lokacin da shirin Harshe yake gudana.
"""

from typing import Any, List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass


class HarsheValue:
    """Tushen dukkan darajojin Harshe (Base Harshe Runtime Value)"""

    @property
    def type_name(self) -> str:
        return "abu"

    def is_truthy(self) -> bool:
        return True

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, HarsheValue):
            return self is other
        return False

    def harshe_repr(self) -> str:
        return str(self)


class HarsheNumber(HarsheValue):
    """Darajar Lamba (Integer ko Float)"""
    def __init__(self, value: float):
        # Store clean integer if whole number
        if isinstance(value, float) and value.is_integer():
            self.value: int | float = int(value)
        else:
            self.value = value

    @property
    def type_name(self) -> str:
        return "lamba"

    def is_truthy(self) -> bool:
        return self.value != 0

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, HarsheNumber):
            return self.value == other.value
        return False

    def __hash__(self) -> int:
        return hash(self.value)

    def harshe_repr(self) -> str:
        return str(self.value)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"HarsheNumber({self.value})"


class HarsheString(HarsheValue):
    """Darajar Rubutu (String)"""
    def __init__(self, value: str):
        self.value = str(value)

    @property
    def type_name(self) -> str:
        return "rubutu"

    def is_truthy(self) -> bool:
        return len(self.value) > 0

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, HarsheString):
            return self.value == other.value
        return False

    def __hash__(self) -> int:
        return hash(self.value)

    def harshe_repr(self) -> str:
        return f'"{self.value}"'

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"HarsheString({repr(self.value)})"


class HarsheBoolean(HarsheValue):
    """Darajar Dabi'a (Boolean: gaskiya ko karya)"""
    def __init__(self, value: bool):
        self.value = bool(value)

    @property
    def type_name(self) -> str:
        return "dabi'a"

    def is_truthy(self) -> bool:
        return self.value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, HarsheBoolean):
            return self.value == other.value
        return False

    def __hash__(self) -> int:
        return hash(self.value)

    def harshe_repr(self) -> str:
        return "gaskiya" if self.value else "karya"

    def __str__(self) -> str:
        return "gaskiya" if self.value else "karya"

    def __repr__(self) -> str:
        return f"HarsheBoolean({self.value})"


class HarsheNull(HarsheValue):
    """Darajar Babu (Null / None)"""
    @property
    def type_name(self) -> str:
        return "babu"

    def is_truthy(self) -> bool:
        return False

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, HarsheNull)

    def __hash__(self) -> int:
        return hash(None)

    def harshe_repr(self) -> str:
        return "babu"

    def __str__(self) -> str:
        return "babu"

    def __repr__(self) -> str:
        return "HarsheNull()"


class HarsheList(HarsheValue):
    """Darajar Jeri (List / Array)"""
    def __init__(self, elements: Optional[List[HarsheValue]] = None):
        self.elements: List[HarsheValue] = elements if elements is not None else []

    @property
    def type_name(self) -> str:
        return "jeri"

    def is_truthy(self) -> bool:
        return len(self.elements) > 0

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, HarsheList):
            return self.elements == other.elements
        return False

    def harshe_repr(self) -> str:
        items = ", ".join(e.harshe_repr() for e in self.elements)
        return f"[{items}]"

    def __str__(self) -> str:
        items = ", ".join(str(e) for e in self.elements)
        return f"[{items}]"

    def __repr__(self) -> str:
        return f"HarsheList({repr(self.elements)})"


class HarsheDict(HarsheValue):
    """Darajar Kamus (Dictionary / Hash Map)"""
    def __init__(self, pairs: Optional[Dict[str, HarsheValue]] = None):
        self.pairs: Dict[str, HarsheValue] = pairs if pairs is not None else {}

    @property
    def type_name(self) -> str:
        return "kamus"

    def is_truthy(self) -> bool:
        return len(self.pairs) > 0

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, HarsheDict):
            return self.pairs == other.pairs
        return False

    def harshe_repr(self) -> str:
        items = ", ".join(f'"{k}": {v.harshe_repr()}' for k, v in self.pairs.items())
        return f"{{{items}}}"

    def __str__(self) -> str:
        items = ", ".join(f'"{k}": {str(v)}' for k, v in self.pairs.items())
        return f"{{{items}}}"

    def __repr__(self) -> str:
        return f"HarsheDict({repr(self.pairs)})"


class HarsheFunction(HarsheValue):
    """Darajar Aiki (User-Defined Function & Closures)"""
    def __init__(self, name: str, params: List[Tuple[str, Optional[str]]], body: Any, closure_env: Any, return_type: Optional[str] = None):
        self.name = name
        self.params = params
        self.body = body
        self.closure_env = closure_env
        self.return_type = return_type

    @property
    def type_name(self) -> str:
        return "aiki"

    def harshe_repr(self) -> str:
        param_strs = [p[0] for p in self.params]
        return f"<aiki {self.name}({', '.join(param_strs)})>"

    def __str__(self) -> str:
        return self.harshe_repr()

    def __repr__(self) -> str:
        return f"HarsheFunction({self.name})"


class HarsheBuiltinFunction(HarsheValue):
    """Darajar Aiki Na Ciki (Built-in standard function)"""
    def __init__(self, name: str, func: Callable[..., HarsheValue], doc: str = ""):
        self.name = name
        self.func = func
        self.doc = doc

    @property
    def type_name(self) -> str:
        return "aiki_na_ciki"

    def harshe_repr(self) -> str:
        return f"<aiki_na_ciki {self.name}>"

    def __str__(self) -> str:
        return self.harshe_repr()

    def __repr__(self) -> str:
        return f"HarsheBuiltinFunction({self.name})"


# ==========================================
# TAIMAKON SAUYAWA (Conversion Helpers)
# ==========================================

def to_harshe_value(val: Any) -> HarsheValue:
    """Sauya darajar Python zuwa HarsheValue"""
    if isinstance(val, HarsheValue):
        return val
    if val is None:
        return HarsheNull()
    if isinstance(val, bool):
        return HarsheBoolean(val)
    if isinstance(val, (int, float)):
        return HarsheNumber(val)
    if isinstance(val, str):
        return HarsheString(val)
    if isinstance(val, list):
        return HarsheList([to_harshe_value(x) for x in val])
    if isinstance(val, dict):
        return HarsheDict({str(k): to_harshe_value(v) for k, v in val.items()})
    return HarsheString(str(val))


def to_python_value(val: HarsheValue) -> Any:
    """Sauya darajar HarsheValue zuwa Python value"""
    if isinstance(val, HarsheNull):
        return None
    if isinstance(val, (HarsheBoolean, HarsheNumber, HarsheString)):
        return val.value
    if isinstance(val, HarsheList):
        return [to_python_value(x) for x in val.elements]
    if isinstance(val, HarsheDict):
        return {k: to_python_value(v) for k, v in val.pairs.items()}
    return val

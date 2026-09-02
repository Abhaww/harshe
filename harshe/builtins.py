"""
Harshe - Ayyukan Ciki Na Yaren Hausa (Built-in Standard Library)
Ayyukan da aka gina a cikin harshen Harshe domin amfanin yau da kullum.
"""

import math
import time
import os
import sys
import random
import json
from typing import List, Dict, Any
from .values import (
    HarsheValue, HarsheNumber, HarsheString, HarsheBoolean,
    HarsheNull, HarsheList, HarsheDict, HarsheBuiltinFunction,
    to_harshe_value, to_python_value
)
from .errors import KuskurenNaui, KuskurenLissafi, KuskurenMatsayi, KuskurenAiki


def builtin_buga(*args: HarsheValue) -> HarsheNull:
    """Buga darajoji zuwa allon kwamfuta (print)"""
    output = " ".join(str(arg) for arg in args)
    print(output)
    return HarsheNull()


def builtin_karba(prompt: HarsheValue = HarsheString("")) -> HarsheString:
    """Karba rubutu ko lamba daga mai amfani (input)"""
    prompt_str = str(prompt) if prompt else ""
    try:
        user_input = input(prompt_str)
        return HarsheString(user_input)
    except (EOFError, KeyboardInterrupt):
        return HarsheString("")


def builtin_tsawo(obj: HarsheValue) -> HarsheNumber:
    """Nemo tsawon rubutu, jeri, ko kamus (len)"""
    if isinstance(obj, HarsheString):
        return HarsheNumber(len(obj.value))
    elif isinstance(obj, HarsheList):
        return HarsheNumber(len(obj.elements))
    elif isinstance(obj, HarsheDict):
        return HarsheNumber(len(obj.pairs))
    raise KuskurenNaui(f"Ba za a iya kiran 'tsawo' a kan nau'in '{obj.type_name}' ba.")


def builtin_kewayon(*args: HarsheValue) -> HarsheList:
    """Samar da jerin lambobi daga farko zuwa karshe (range)"""
    if len(args) == 1:
        if not isinstance(args[0], HarsheNumber):
            raise KuskurenNaui("Dole ne ma'aunin 'kewayon' ya zama lamba.")
        start, stop, step = 0, int(args[0].value), 1
    elif len(args) == 2:
        if not (isinstance(args[0], HarsheNumber) and isinstance(args[1], HarsheNumber)):
            raise KuskurenNaui("Dole ne ma'aunan 'kewayon' su zama lambobi.")
        start, stop, step = int(args[0].value), int(args[1].value), 1
    elif len(args) == 3:
        if not (isinstance(args[0], HarsheNumber) and isinstance(args[1], HarsheNumber) and isinstance(args[2], HarsheNumber)):
            raise KuskurenNaui("Dole ne ma'aunan 'kewayon' su zama lambobi.")
        start, stop, step = int(args[0].value), int(args[1].value), int(args[2].value)
    else:
        raise KuskurenAiki(f"Kewayon yana karbar ma'auni 1, 2, ko 3, amma an shigar da {len(args)}.")

    if step == 0:
        raise KuskurenLissafi("Matakin 'kewayon' ba zai iya zama sifili (0) ba.")

    result = [HarsheNumber(i) for i in range(start, stop, step)]
    return HarsheList(result)


def builtin_naui(obj: HarsheValue) -> HarsheString:
    """Nemo nau'in daraja (type of value)"""
    return HarsheString(obj.type_name)


def builtin_lamba(obj: HarsheValue) -> HarsheNumber:
    """Sauya rubutu ko dabi'a zuwa lamba (cast to number)"""
    if isinstance(obj, HarsheNumber):
        return obj
    elif isinstance(obj, HarsheBoolean):
        return HarsheNumber(1 if obj.value else 0)
    elif isinstance(obj, HarsheString):
        s = obj.value.strip()
        try:
            val = float(s) if '.' in s else int(s)
            return HarsheNumber(val)
        except ValueError:
            raise KuskurenNaui(f"Ba za a iya sauya rubutun '{obj.value}' zuwa lamba ba.")
    raise KuskurenNaui(f"Ba za a iya sauya nau'in '{obj.type_name}' zuwa lamba ba.")


def builtin_rubutu(obj: HarsheValue) -> HarsheString:
    """Sauya kowane abu zuwa rubutu (str)"""
    return HarsheString(str(obj))


def builtin_dabia(obj: HarsheValue) -> HarsheBoolean:
    """Sauya kowane abu zuwa dabi'a (bool)"""
    return HarsheBoolean(obj.is_truthy())


def builtin_kara(lst: HarsheValue, item: HarsheValue) -> HarsheList:
    """Sanya sabon abu a karshen jeri (append)"""
    if not isinstance(lst, HarsheList):
        raise KuskurenNaui(f"Ba za a iya kiran 'kara' a kan '{lst.type_name}' ba, jeri kawai.")
    lst.elements.append(item)
    return lst


def builtin_cire(lst: HarsheValue, index: HarsheValue = HarsheNull()) -> HarsheValue:
    """Cire abu daga jeri (pop / remove at index)"""
    if not isinstance(lst, HarsheList):
        raise KuskurenNaui(f"Ba za a iya kiran 'cire' a kan '{lst.type_name}' ba, jeri kawai.")
    if len(lst.elements) == 0:
        raise KuskurenMatsayi("Ba za a iya cire abu daga jeri marar kowa ba.")

    if isinstance(index, HarsheNull):
        return lst.elements.pop()
    elif isinstance(index, HarsheNumber):
        idx = int(index.value)
        if -len(lst.elements) <= idx < len(lst.elements):
            return lst.elements.pop(idx)
        raise KuskurenMatsayi(f"Matsayin lamba {idx} ya wuce iyakar jeri (tsawo: {len(lst.elements)}).")
    raise KuskurenNaui("Dole ne matsayin cirewa ya zama lamba.")


def builtin_saka_a(lst: HarsheValue, index: HarsheValue, item: HarsheValue) -> HarsheList:
    """Sanya abu a wani matsayi na musamman a jeri (insert)"""
    if not isinstance(lst, HarsheList):
        raise KuskurenNaui(f"Ba za a iya kiran 'saka_a' a kan '{lst.type_name}' ba.")
    if not isinstance(index, HarsheNumber):
        raise KuskurenNaui("Dole ne matsayin 'saka_a' ya zama lamba.")
    idx = int(index.value)
    lst.elements.insert(idx, item)
    return lst


def builtin_raba(text: HarsheValue, delimiter: HarsheValue = HarsheString(" ")) -> HarsheList:
    """Raba rubutu zuwa jeri ta amfani da mai raba (split)"""
    if not isinstance(text, HarsheString):
        raise KuskurenNaui(f"Ana bukatar rubutu domin kiran 'raba', amma an sami '{text.type_name}'.")
    delim_str = str(delimiter)
    parts = text.value.split(delim_str)
    return HarsheList([HarsheString(p) for p in parts])


def builtin_hade(lst: HarsheValue, separator: HarsheValue = HarsheString("")) -> HarsheString:
    """Hada jerin rubutu zuwa rubutu guda (join)"""
    if not isinstance(lst, HarsheList):
        raise KuskurenNaui(f"Ana bukatar jeri domin kiran 'hade', amma an sami '{lst.type_name}'.")
    sep_str = str(separator)
    joined = sep_str.join(str(e) for e in lst.elements)
    return HarsheString(joined)


def builtin_makullan_kamus(dct: HarsheValue) -> HarsheList:
    """Nemo duk makullan kamus (keys)"""
    if not isinstance(dct, HarsheDict):
        raise KuskurenNaui(f"Ana bukatar kamus domin nemo makullai, amma an sami '{dct.type_name}'.")
    return HarsheList([HarsheString(k) for k in dct.pairs.keys()])


def builtin_darajojin_kamus(dct: HarsheValue) -> HarsheList:
    """Nemo duk darajojin kamus (values)"""
    if not isinstance(dct, HarsheDict):
        raise KuskurenNaui(f"Ana bukatar kamus domin nemo darajoji, amma an sami '{dct.type_name}'.")
    return HarsheList(list(dct.pairs.values()))


def builtin_cikakken_lamba(num: HarsheValue) -> HarsheNumber:
    """Cikakken lamba ba tare da alamar diba ba (abs)"""
    if not isinstance(num, HarsheNumber):
        raise KuskurenNaui(f"Ana bukatar lamba domin kiran 'cikakken_lamba', amma an sami '{num.type_name}'.")
    return HarsheNumber(abs(num.value))


def builtin_zagaye(num: HarsheValue, decimals: HarsheValue = HarsheNumber(0)) -> HarsheNumber:
    """Zagaye lamba zuwa adadin decimal da aka bukata (round)"""
    if not (isinstance(num, HarsheNumber) and isinstance(decimals, HarsheNumber)):
        raise KuskurenNaui("Ana bukatar lambobi domin kiran 'zagaye'.")
    return HarsheNumber(round(num.value, int(decimals.value)))


def builtin_mafi_girma(*args: HarsheValue) -> HarsheValue:
    """Nemo wanda ya fi girma (max)"""
    if len(args) == 0:
        raise KuskurenAiki("Ana bukatar a kalla abu daya a 'mafi_girma'.")
    if len(args) == 1 and isinstance(args[0], HarsheList):
        items = args[0].elements
        if len(items) == 0:
            raise KuskurenMatsayi("Jeri ba shi da kowa a ciki.")
        return max(items, key=lambda x: x.value if hasattr(x, 'value') else 0)
    return max(args, key=lambda x: x.value if hasattr(x, 'value') else 0)


def builtin_mafi_kankanta(*args: HarsheValue) -> HarsheValue:
    """Nemo wanda ya fi kankanta (min)"""
    if len(args) == 0:
        raise KuskurenAiki("Ana bukatar a kalla abu daya a 'mafi_kankanta'.")
    if len(args) == 1 and isinstance(args[0], HarsheList):
        items = args[0].elements
        if len(items) == 0:
            raise KuskurenMatsayi("Jeri ba shi da kowa a ciki.")
        return min(items, key=lambda x: x.value if hasattr(x, 'value') else 0)
    return min(args, key=lambda x: x.value if hasattr(x, 'value') else 0)


def builtin_tushe(num: HarsheValue) -> HarsheNumber:
    """Tushen lamba (Square Root - sqrt)"""
    if not isinstance(num, HarsheNumber):
        raise KuskurenNaui("Ana bukatar lamba domin kiran 'tushe'.")
    if num.value < 0:
        raise KuskurenLissafi("Ba za a iya nemo tushen lamba marar kyau (< 0) ba.")
    return HarsheNumber(math.sqrt(num.value))


def builtin_iko(base: HarsheValue, exp: HarsheValue) -> HarsheNumber:
    """Ikon lamba (Power: a ^ b)"""
    if not (isinstance(base, HarsheNumber) and isinstance(exp, HarsheNumber)):
        raise KuskurenNaui("Ana bukatar lambobi domin kiran 'iko'.")
    return HarsheNumber(math.pow(base.value, exp.value))


def builtin_lokaci() -> HarsheNumber:
    """Lokacin yanzu a dakikoki (timestamp)"""
    return HarsheNumber(time.time())


def builtin_karanta_fayil(path: HarsheValue) -> HarsheString:
    """Karanta rubutun da ke cikin fayil (read file)"""
    if not isinstance(path, HarsheString):
        raise KuskurenNaui("Dole ne hanyar fayil ta zama rubutu.")
    try:
        with open(path.value, 'r', encoding='utf-8') as f:
            content = f.read()
        return HarsheString(content)
    except Exception as e:
        raise KuskurenAiki(f"An samu matsala wajen karanta fayil '{path.value}': {str(e)}")


def builtin_rubuta_fayil(path: HarsheValue, content: HarsheValue) -> HarsheBoolean:
    """Rubuta bayanai a cikin fayil (write file)"""
    if not (isinstance(path, HarsheString) and isinstance(content, HarsheString)):
        raise KuskurenNaui("Hanyar fayil da abun ciki dole ne su zama rubutu.")
    try:
        with open(path.value, 'w', encoding='utf-8') as f:
            f.write(content.value)
        return HarsheBoolean(True)
    except Exception as e:
        raise KuskurenAiki(f"An samu matsala wajen rubuta fayil '{path.value}': {str(e)}")


# ==========================================
# KARIN AYYUKA NA ECOSYSTEM (Expanded Built-ins)
# ==========================================

def builtin_bazuwar_lamba(fara: HarsheValue, karshe: HarsheValue) -> HarsheNumber:
    """Samar da lamba ta bazuwa a tsakanin iyaka biyu (random int in range [fara, karshe])"""
    if not (isinstance(fara, HarsheNumber) and isinstance(karshe, HarsheNumber)):
        raise KuskurenNaui("Ma'aunan 'bazuwar_lamba' dole ne su zama lambobi.")
    val = random.randint(int(fara.value), int(karshe.value))
    return HarsheNumber(val)


def builtin_zabi_a_jeri(lst: HarsheValue) -> HarsheValue:
    """Zabi abu daya a cikin jeri ta hanyar bazuwa (random choice)"""
    if not isinstance(lst, HarsheList):
        raise KuskurenNaui("Ana bukatar jeri domin zabar abu ta bazuwa.")
    if len(lst.elements) == 0:
        raise KuskurenMatsayi("Jeri ba shi da kowa a ciki da za a zaba.")
    return random.choice(lst.elements)


def builtin_karanta_json(rubutu_json: HarsheValue) -> HarsheValue:
    """Fassara rubutun JSON zuwa kamus ko jeri a Harshe (parse JSON)"""
    if not isinstance(rubutu_json, HarsheString):
        raise KuskurenNaui("Ana bukatar rubutu domin kiran 'karanta_json'.")
    try:
        parsed = json.loads(rubutu_json.value)
        return to_harshe_value(parsed)
    except Exception as e:
        raise KuskurenAiki(f"Kuskuren fassara JSON: {str(e)}")


def builtin_rubuta_json(daraja: HarsheValue, mai_kyau: HarsheValue = HarsheBoolean(False)) -> HarsheString:
    """Sauya kamus ko jeri zuwa rubutun JSON (stringify JSON)"""
    py_obj = to_python_value(daraja)
    indent = 2 if mai_kyau.is_truthy() else None
    try:
        json_str = json.dumps(py_obj, ensure_ascii=False, indent=indent)
        return HarsheString(json_str)
    except Exception as e:
        raise KuskurenAiki(f"Kuskuren rubuta JSON: {str(e)}")


def builtin_fita(code: HarsheValue = HarsheNumber(0)) -> HarsheNull:
    """Fita daga shirin gaba daya (exit program)"""
    c = int(code.value) if isinstance(code, HarsheNumber) else 0
    sys.exit(c)


def get_default_builtins() -> Dict[str, HarsheBuiltinFunction]:
    """Samar da dukkan ayyukan cikin Harshe (Register all builtins)"""
    builtins = {
        # Sadarwa da shigarwa (I/O)
        "buga": HarsheBuiltinFunction("buga", builtin_buga, "Buga rubutu ko darajoji zuwa allo"),
        "karba": HarsheBuiltinFunction("karba", builtin_karba, "Karba shigarwa daga mai amfani"),
        
        # Bayani da nau'i (Types & Inspection)
        "tsawo": HarsheBuiltinFunction("tsawo", builtin_tsawo, "Nemo tsawon rubutu, jeri, ko kamus"),
        "kewayon": HarsheBuiltinFunction("kewayon", builtin_kewayon, "Samar da jerin lambobi a tsakanin iyaka"),
        "nau'i": HarsheBuiltinFunction("nau'i", builtin_naui, "Nemo nau'in daraja"),
        "nau_i": HarsheBuiltinFunction("nau_i", builtin_naui, "Nemo nau'in daraja"),
        "lamba": HarsheBuiltinFunction("lamba", builtin_lamba, "Sauya daraja zuwa lamba"),
        "rubutu": HarsheBuiltinFunction("rubutu", builtin_rubutu, "Sauya daraja zuwa rubutu"),
        "dabi'a": HarsheBuiltinFunction("dabi'a", builtin_dabia, "Sauya daraja zuwa dabi'a"),
        "dabi_a": HarsheBuiltinFunction("dabi_a", builtin_dabia, "Sauya daraja zuwa dabi'a"),

        # Ayyukan Jeri da Kamus (Collections)
        "kara": HarsheBuiltinFunction("kara", builtin_kara, "Sanya abu a karshen jeri"),
        "cire": HarsheBuiltinFunction("cire", builtin_cire, "Cire abu daga jeri"),
        "saka_a": HarsheBuiltinFunction("saka_a", builtin_saka_a, "Sanya abu a wani matsayi a jeri"),
        "raba": HarsheBuiltinFunction("raba", builtin_raba, "Raba rubutu zuwa jeri"),
        "hade": HarsheBuiltinFunction("hade", builtin_hade, "Hada jerin rubutu zuwa rubutu guda"),
        "makullan_kamus": HarsheBuiltinFunction("makullan_kamus", builtin_makullan_kamus, "Nemo makullan kamus"),
        "darajojin_kamus": HarsheBuiltinFunction("darajojin_kamus", builtin_darajojin_kamus, "Nemo darajojin kamus"),

        # Lissafi (Math)
        "cikakken_lamba": HarsheBuiltinFunction("cikakken_lamba", builtin_cikakken_lamba, "Nemo cikakken lamba (abs)"),
        "zagaye": HarsheBuiltinFunction("zagaye", builtin_zagaye, "Zagaye lamba (round)"),
        "mafi_girma": HarsheBuiltinFunction("mafi_girma", builtin_mafi_girma, "Nemo wanda ya fi girma (max)"),
        "mafi_kankanta": HarsheBuiltinFunction("mafi_kankanta", builtin_mafi_kankanta, "Nemo wanda ya fi kankanta (min)"),
        "tushe": HarsheBuiltinFunction("tushe", builtin_tushe, "Nemo tushen lamba (sqrt)"),
        "iko": HarsheBuiltinFunction("iko", builtin_iko, "Nemo ikon lamba (power)"),

        # Lokaci da Fayiloli (Time & File I/O)
        "lokaci": HarsheBuiltinFunction("lokaci", builtin_lokaci, "Lokacin yanzu a dakikoki"),
        "karanta_fayil": HarsheBuiltinFunction("karanta_fayil", builtin_karanta_fayil, "Karanta abun cikin fayil"),
        "rubuta_fayil": HarsheBuiltinFunction("rubuta_fayil", builtin_rubuta_fayil, "Rubuta a cikin fayil"),

        # Bazuwa da JSON da Tsari (Random & JSON)
        "bazuwar_lamba": HarsheBuiltinFunction("bazuwar_lamba", builtin_bazuwar_lamba, "Samar da lamba ta bazuwa a tsakanin iyaka"),
        "zabi_a_jeri": HarsheBuiltinFunction("zabi_a_jeri", builtin_zabi_a_jeri, "Zabi abu daya daga jeri ta bazuwa"),
        "karanta_json": HarsheBuiltinFunction("karanta_json", builtin_karanta_json, "Fassara rubutun JSON zuwa kamus/jeri"),
        "rubuta_json": HarsheBuiltinFunction("rubuta_json", builtin_rubuta_json, "Sauya kamus/jeri zuwa rubutun JSON"),
        "fita_daga_shiri": HarsheBuiltinFunction("fita_daga_shiri", builtin_fita, "Fita daga shirin gaba daya"),
    }
    return builtins

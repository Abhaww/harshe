# Harshe (HausaLang) 🚀

<div align="center">

---

## 📖 Gabatarwa (Overview)

**Harshe (HausaLang)** cikakken harshen shirye-shiryen kwamfuta ne (programming language) wanda aka gina shi tun daga tushe domin ba wa al'ummar Hausawa, ɗalibai, malamai, da masu bincike damar koyo da rubuta lambobin kwamfuta (coding) cikin tsantsar yaren Hausa.

Harshe yana kunshe da:

- **Injin Fassara da Gudanarwa (Interpreter & Runtime Engine)**
- **Injin Hada Shirye-shirye zuwa Fayilolin Windows (`.exe` Standalone Compiler)**
- **Dandalin Yanar Gizo na Koyo da Zane (Interactive Web IDE & Canvas Academy)**
- **Karin Kayan Aiki na Visual Studio Code (Official VS Code Extension)**
- **Tsarin Kula da Kunshin Laburare (Package Manager: `kunshi`)**

---

## 🌟 Muhimman Fasaloli (Key Features)

- ✅ **Nahawun Hausa Zalla**: Kalmomi da jimlolin Hausa na asali kamar `bari`, `tsayayye`, `idan`, `ko idan`, `in ba haka ba`, `yayin da`, `ga ... a cikin`, `aiki`, `koma`, `gwada`, da `kama`.
- ✅ **Bayanai Masu Faɗi (Data Types)**: Lambobi (`lamba`), Rubutu (`rubutu`), Dabi'a (`dabi'a` - `gaskiya`/`karya`), Jeri (`jeri`), Kamus (`kamus`), da `babu` (null).
- ✅ **Bayyana Nau'in Bayanai (Optional Type Hints)**: Taimakon bayyana nau'in bayanai kamar `bari suna: rubutu = "Amina"` da `aiki ninka(x: lamba) -> lamba`.
- ✅ **Ayyuka da Rufewar Mahalli (Functions, Recursion & Closures)**: Kirkirar ayyuka, aiki a cikin aiki (closures), da kiran aiki a kansa (recursion).
- ✅ **Kama Kuskure (Try / Catch Exception Handling)**: Kariya daga katsewar shiri ta amfani da `gwada { ... } kama (kuskure) { ... }`.
- ✅ **Tsarin Shigo da Laburare (Modular Imports)**: Rarraba ayyuka ta amfani da `shigo_da` da `daga ... shigo_da ...`.
- ✅ **Laburaren Ciki (Standard Library)**: Laburaren lissafi (`lissafi`), rubutu (`rubutu`), da lokaci (`lokaci`).
- ✅ **Fiye da Ayyukan Ciki 25 (25+ Built-in Functions)**: Sadarwa, lissafi, binciken bayanai, bazuwar lamba (random), JSON, da sarrafa fayiloli.

---

## 📥 Shigarwa (Installation)

### 1. Windows (PowerShell One-Liner)

Bude PowerShell sannan ka manna wannan umarnin:

```powershell
irm https://raw.githubusercontent.com/harshe-lang/harshe/main/install.ps1 | iex
```

### 2. Linux / macOS (Bash One-Liner)

Bude Terminal sannan ka manna wannan umarnin:

```bash
curl -fsSL https://raw.githubusercontent.com/harshe-lang/harshe/main/install.sh | bash
```

### 3. Shigarwa daga Tushe (Manual / Pip Install)

Idan kana da Python 3.10 ko sama da haka:

```bash
git clone https://github.com/harshe-lang/harshe.git
cd harshe
python -m pip install -e .
```

---

## 🚀 Fara Aiki (Quick Start)

Bayan an shigar da Harshe, zaka iya amfani da umarnin `harshe` ko `python harshe_cli.py`:

```bash
# 1. Bude dandalin tattaunawa kai-tsaye (Interactive REPL)
harshe repl

# 2. Gudanar da fayil din Harshe
harshe run examples/01_sannu_duniya.hausa

# 3. Hada shiri zuwa Windows .exe mai zaman kansa (Standalone Binary)
harshe compile examples/01_sannu_duniya.hausa -o sannu_duniya

# 4. Kirkirar sabon aikin Harshe mai cikakken tsari
harshe sabo sabon_aikina
cd sabon_aikina
harshe run babban_shiri.hausa
```

---

## ⌨️ Cikakken Jagorar Nahawu (Syntax Guide)

### 1. Ma'adana da Tsayayyu (Variables & Constants)

```harshe
# Ma'adana mai sauyawa (Variable)
bari sunana = "Aliyu";
saka shekaru = 25;
shekaru = 26; # Za a iya sauyawa

# Tsayayyen da ba ya sauyawa (Constant)
tsayayye KASAR_HAUHAWA = "Najeriya";
# KASAR_HAUHAWA = "Wata Kasa"; # Wannan zai bada kuskure!

# Bayyana Nau'i (Optional Type Annotations)
bari birni: rubutu = "Kano";
bari kudi: lamba = 1500.50;
bari mai_aiki: dabi'a = gaskiya;
```

---

### 2. Sharudda (Conditionals)

```harshe
bari maki = 85;

idan (maki >= 75 kuma maki <= 100) {
    buga("Daraja: 'A' (Mafi Kyau)");
} ko idan (maki >= 60 kuma maki < 75) {
    buga("Daraja: 'B' (Yayi Kyau)");
} ko idan (maki >= 50 kuma maki < 60) {
    buga("Daraja: 'C' (Matsakaici)");
} in ba haka ba {
    buga("Daraja: 'F' (Kuskure/Kasa)");
}
```

---

### 3. Masu Hada Hukunci da Masu Aiki (Operators)

- **Lissafi**: `+` (tara), `-` (debewa), `*` (ninkawa), `/` (rabawa), `%` (sauran rabo), `**` (iko).
- **Kwatantawa**: `==` (daidai), `!=` (ba daidai ba), `<` (kasa da), `<=` (kasa ko daidai), `>` (fiyeda), `>=` (fiyeda ko daidai).
- **Hankali (Logical)**: `kuma` / `&&`, `ko` / `||`, `ba` / `!`.
- **Dabi'a (Booleans)**: `gaskiya` (true), `karya` (false), `babu` (null).

```harshe
bari kudi_a_hannu = 500;
bari yana_da_katin_cire_kudi = gaskiya;

idan (kudi_a_hannu >= 1000 ko yana_da_katin_cire_kudi) {
    buga("Za ka iya yin siyayya.");
}
```

---

### 4. Madaukai (Loops: `ga`, `yayin da`, `kewayon`)

```harshe
# Madaukin For ta amfani da kewayon (Range Loop)
buga("Kirgawa 1 zuwa 5:");
ga i a cikin kewayon(1, 6) {
    buga("  Lamba:", i);
}

# Madaukin While (yayin da)
bari adadi = 3;
yayin da (adadi > 0) {
    buga("  Sauran:", adadi);
    adadi = adadi - 1;
}

# Madauki a kan Jeri da tsallakewa (break / continue)
bari 'ya'yan_itace = ["Mangwaro", "Lemu", "Ayaba", "Kankana"];
ga 'ya'ya a cikin 'ya'yan_itace {
    idan ('ya'ya == "Lemu") {
        ci_gaba; # Tsallake wannan
    }
    buga("Ina son:", 'ya'ya);
}
```

---

### 5. Ayyuka da Rufe Mahalli (Functions & Closures)

```harshe
# Aiki mai karbar ma'auni da komar da daraja
aiki gaisuwa(suna, lokaci) {
    koma "Barka da " + lokaci + ", " + suna + "!";
}

buga(gaisuwa("Fatima", "yamma"));

# Aiki mai komar da kansa (Recursion)
aiki factorial(n) {
    idan (n <= 1) {
        koma 1;
    }
    koma n * factorial(n - 1);
}

buga("5! =", factorial(5)); # 120

# Rufe Mahalli (Closure)
aiki kirkiri_mai_ninkawa(ninki) {
    aiki ninka(lamba) {
        koma lamba * ninki;
    }
    koma ninka;
}

bari ninka_biyar = kirkiri_mai_ninkawa(5);
buga("10 x 5 =", ninka_biyar(10)); # 50
```

---

### 6. Jeri da Kamus (Lists & Dictionaries)

```harshe
# Jeri (Lists)
bari sunaye = ["Zainab", "Musa", "Bello"];
kara(sunaye, "Khadija"); # Sanya a karshe
bari wanda_aka_cire = cire(sunaye); # Cire na karshe
buga("Tsawon jeri:", tsawo(sunaye));
buga("Na farko:", sunaye[0]);

# Kamus (Dictionaries / Key-Value Map)
bari bayanin_dalibi = {
    "suna": "Umar Faruk",
    "shekaru": 22,
    "fanni": "Kimiyyar Kwamfuta",
    "maki": 91.5
};

buga("Sunan dalibi:", bayanin_dalibi["suna"]);
bayanin_dalibi["birni"] = "Zaria"; # Kara sabon maɓalli

buga("Duk maɓallan:", makullan_kamus(bayanin_dalibi));
buga("Duk darajojin:", darajojin_kamus(bayanin_dalibi));
```

---

### 7. Kama Kuskure (Try / Catch Exception Handling)

```harshe
gwada {
    buga("Kokarin raba lamba da sifili...");
    bari sakamako = 100 / 0;
} kama (kuskure) {
    buga("[An kama kuskure]:", kuskure);
    buga("Shirin ya ci gaba da aiki lafiya!");
}
```

---

### 8. Shigo da Laburare (Module Imports)

```harshe
# 1. Shigo da dukkan laburaren
shigo_da "lissafi";
bari mats = matsakaici([10, 20, 30, 40]);
buga("Matsakaici:", mats);

# 2. Shigo da takamaiman ayyuka
daga "rubutu" shigo_da juya_rubutu, ko_palindrome_ne, adadin_kalmomi;
buga("Juyayyen rubutu:", juya_rubutu("harshe"));
buga("Ko 'kayak' palindrome ce?:", ko_palindrome_ne("kayak"));

# 3. Shigo da fayil din dake cikin aikinka
daga "kayan_aiki/taimako.hausa" shigo_da babban_aiki;
```

---

## 🛠️ Ayyukan Ciki (Built-in Functions)

Harshe yana dauke da tarin ayyukan ciki da ba sa bukatar shigo da wani laburare:

| Aiki (Function)                   | Bayani a Hausa                                   | English Description                      |
| :-------------------------------- | :----------------------------------------------- | :--------------------------------------- |
| `buga(...)`                     | Buga bayanai zuwa allon kwamfuta                 | Print values to console                  |
| `karba(tambaya)`                | Karba rubutu ko lamba daga mai amfani            | Receive user input                       |
| `tsawo(obj)`                    | Nemo tsawon rubutu, jeri, ko kamus               | Get length of string, list, or dict      |
| `kewayon(fara, karshe, mataki)` | Samar da jerin lambobi a tsakanin iyaka          | Generate sequence of numbers (`range`) |
| `nau'i(obj)`                    | Nemo sunan nau'in daraja                         | Get data type name                       |
| `lamba(obj)`                    | Sauya daraja zuwa lamba                          | Cast value to number                     |
| `rubutu(obj)`                   | Sauya daraja zuwa rubutu                         | Cast value to string                     |
| `dabi'a(obj)`                   | Sauya daraja zuwa dabi'a (`gaskiya`/`karya`) | Cast value to boolean                    |
| `kara(jeri, abu)`               | Sanya sabon abu a karshen jeri                   | Append item to list                      |
| `cire(jeri, [index])`           | Cire abu daga jeri                               | Pop/remove item from list                |
| `saka_a(jeri, index, abu)`      | Sanya abu a wani matsayi na jeri                 | Insert item at list index                |
| `raba(rubutu, mai_raba)`        | Raba rubutu zuwa jeri                            | Split string into list                   |
| `hade(jeri, mai_hada)`          | Hada jerin rubutu zuwa rubutu guda               | Join list of strings                     |
| `makullan_kamus(kamus)`         | Nemo dukkan maɓallan kamus                      | Get all keys of a dictionary             |
| `darajojin_kamus(kamus)`        | Nemo dukkan darajojin kamus                      | Get all values of a dictionary           |
| `cikakken_lamba(num)`           | Cikakkiyar lamba ba tare da alamar diba ba       | Absolute value (`abs`)                 |
| `zagaye(num, [decimals])`       | Zagaye lamba zuwa adadin decimal                 | Round number                             |
| `mafi_girma(...)`               | Nemo daraja mafi girma                           | Maximum value (`max`)                  |
| `mafi_kankanta(...)`            | Nemo daraja mafi kankanta                        | Minimum value (`min`)                  |
| `tushe(num)`                    | Tushen lamba (Square root)                       | Square root (`sqrt`)                   |
| `iko(base, exp)`                | Ikon lamba ($base^{exp}$)                      | Power function                           |
| `lokaci()`                      | Lokacin yanzu a dakikoki (timestamp)             | Current timestamp in seconds             |
| `karanta_fayil(path)`           | Karanta abun cikin fayil                         | Read text file contents                  |
| `rubuta_fayil(path, text)`      | Rubuta bayanai a cikin fayil                     | Write text to file                       |
| `bazuwar_lamba(fara, karshe)`   | Samar da lamba ta bazuwa a tsakanin iyaka        | Random integer in range                  |
| `zabi_a_jeri(jeri)`             | Zabi abu daya a cikin jeri ta bazuwa             | Random choice from list                  |
| `karanta_json(rubutu)`          | Fassara rubutun JSON zuwa kamus ko jeri          | Parse JSON string                        |
| `rubuta_json(obj, [mai_kyau])`  | Sauya kamus/jeri zuwa rubutun JSON               | Stringify object to JSON                 |
| `fita_daga_shiri([code])`       | Fita daga shirin gaba daya                       | Exit program                             |

---

## 📚 Laburaren Ciki (Standard Library)

Harshe ya zo tare da laburaren ciki masu amfani:

### 1. `lissafi` (Math Library)

- `ko_lamba_marar_rabo_ce(n)`: Bincika ko lamba Prime Number ce.
- `matsakaici(jeri)`: Nemo matsakaicin jerin lambobi (Mean/Average).
- `factorial(n)`: Lissafin factorial ($n!$).
- `fadin_daira(radius)`: Lissafa faɗin da'ira ($\pi r^2$).
- `kewayen_daira(radius)`: Lissafa kewayen da'ira ($2 \pi r$).
- `fadin_kusurwa_hudu(tsawo, fadi)`: Lissafa fadin rectangle.
- `PI`: Tsayayyen lambar $\pi \approx 3.14159265359$.

### 2. `rubutu` (String Processing)

- `juya_rubutu(rubutu)`: Juya haruffan rubutu daga karshe zuwa farko.
- `ko_palindrome_ne(rubutu)`: Bincika ko rubutu yana karantuwa iri daya ta gaba da baya.
- `adadin_kalmomi(rubutu)`: Kirga adadin kalmomin da ke cikin jimla.
- `hada_kalamai(jeri, mai_raba)`: Hada jerin kalmomi.

### 3. `lokaci` (Time & Calendar)

- `KWANAKIN_MAKO`: Jerin kwanakin mako a Hausa (*Litinin, Talata, Laraba, Alhamis, Juma'a, Asabar, Lahadi*).
- `WATANNIN_SHEKARA`: Jerin watannin shekara (*Janairu, Fabrairu, Maris, ...*).
- `gaisuwar_lokaci(awa)`: Bayar da gaisuwa gwargwadon lokaci (*Ina kwana / Barka da rana / Barka da yamma / Barka da dare*).

---

## 🛠️ Kayan Aikin Layin Umarni (CLI Reference)

Ana kiran kayan aikin Harshe ta amfani da `harshe <umarni>` ko `python harshe_cli.py <umarni>`:

| Umarni                  | Misali                                   | Bayani                                                |
| :---------------------- | :--------------------------------------- | :---------------------------------------------------- |
| `run`                 | `harshe run shiri.hausa`               | Gudanar da shirin Harshe                              |
| `repl`                | `harshe repl`                          | Fara dandalin rubuta lambobi kai-tsaye                |
| `compile` / `hada`  | `harshe compile shiri.hausa -o aikina` | Hada shiri zuwa`.exe` na Windows                    |
| `sabo` / `init`     | `harshe sabo sabon_aiki`               | Kirkirar sabon aikin Harshe mai cikakken tsari        |
| `shigar` / `kunshi` | `harshe shigar lissafi_mai_karfi`      | Shigar da kunshin laburare a`kunshiyoyi/`           |
| `tokens`              | `harshe tokens shiri.hausa`            | Bincika alamomin nahawu (Lexer Tokens)                |
| `ast`                 | `harshe ast shiri.hausa`               | Duba bishiyar nahawu ta shirin (Abstract Syntax Tree) |
| `version` / `-v`    | `harshe -v`                            | Duba lambar sigar Harshe                              |

---

## 🌐 Interactive Web IDE & Academy

Harshe yana kunshe da dandalin yanar gizo mai cin gashin kansa don koyo da aiki:

- **Editan Lambobi na Yanar Gizo (Web Code Editor)** tare da haskaka nahawu.
- **Dakin Karatu Mai Darussa 8 (Interactive 8-Lesson Academy)**: Daga *Sannu Duniya* har zuwa *Zanen Allon Kwamfuta (Canvas Graphics)*.
- **Allon Zane Mai Hannu (Interactive Canvas Drawing Output)**.
- **Sauke Fayilolin `.hausa` da Fitar da `.exe` Kai-tsaye**.

Domin budewa a kwamfutarka:

```bash
# Windows
start web/index.html

# Linux
xdg-open web/index.html

# macOS
open web/index.html
```

---

## 💻 VS Code Extension

Harshe yana da kashin kansa na kayan aiki a Visual Studio Code (`vscode-harshe`):

- **Haskaka Nahawu (Syntax Highlighting)** domin fayilolin `.hausa`, `.har`, da `.hsh`.
- **Gajerun Hanyoyin Rubutu (Code Snippets)** kamar `aiki`, `idan`, `yayin_da`, `ga`, `gwada`.
- **Fayil din `.vsix` da aka riga aka shirya**: `harshe-language-1.0.0.vsix`.

### Shigarwa a VS Code:

```bash
code --install-extension harshe-language-1.0.0.vsix
```

Ko kuma a cikin VS Code:

1. Bude shafin **Extensions** (`Ctrl+Shift+X`).
2. Danna alamar ɗigo uku `...` a saman dama.
3. Zabi **Install from VSIX...** sannan ka zabi `harshe-language-1.0.0.vsix`.

---

## 🧪 Gwaje-gwaje (Testing)

Tsarin Harshe yana dauke da cikakken rukunin gwaje-gwajen lafiyar aiki:

```bash
python -m unittest discover tests -v
```

---

## 📂 Tsarin Fayiloli na Aiki (Repository Structure)

```text
harshe/
├── harshe/                     # Babban injin harshen (Core Engine)
│   ├── lexer.py                # Mai raba kalmomi da alamomi
│   ├── parser.py               # Mai gina bishiyar nahawu (AST)
│   ├── interpreter.py          # Injin gudanar da lambobi (Interpreter)
│   ├── builtins.py             # Ayyukan cikin harshe (Built-ins)
│   ├── tokens.py               # Rukunin alamomi da kalmomin Hausa
│   ├── values.py               # Nau'o'in bayanai na Harshe
│   ├── environment.py          # Mahalli da ma'adanar sunaye
│   ├── errors.py               # Sakonnin kuskure a Hausa
│   └── repl.py                 # Dandalin tattaunawa kai-tsaye
├── harshe_stdlib/              # Laburaren ciki na Hausa (Stdlib)
│   ├── lissafi.hausa           # Laburaren lissafi
│   ├── rubutu.hausa            # Laburaren sarrafa rubutu
│   └── lokaci.hausa            # Laburaren lokaci da kwanaki
├── examples/                   # Tarin misalan koyo guda 9
├── tests/                      # Gwaje-gwajen inji (Unit Tests)
├── web/                        # Web IDE & Interactive Academy
├── vscode-harshe/              # Kayan aikin VS Code Extension
├── harshe_cli.py               # Babban layin umarni (CLI)
├── install.ps1                 # Shigarwa a Windows
├── install.sh                  # Shigarwa a Linux/macOS
├── setup.py                    # Tsarin kunshin Python
└── README.md                   # Wannan takardar bayani
```

---

## 🤝 Gudunmawa (Contributing)

Muna maraba da duk wani mai sha'awar bayar da gudunmawa wajen bunkasa harshen Harshe!

1. Yi **Fork** na wannan ma'adanar.
2. Kirkiri reshen fasalinka (`git checkout -b sabuwar-fasala`).
3. Tabbatar dukkan gwaje-gwaje sun yi nasara (`python -m unittest discover tests -v`).
4. Yi **Commit** da tura canje-canjenka (`git commit -m "Kara sabuwar fasala"`).
5. Bude **Pull Request**.

---

## 📄 Lasisi (License)

Wannan aiki yana karkashin lasisin **[MIT License](LICENSE)**. Kowa yana da 'yancin amfani, sauyawa, da rarraba shi kyauta.

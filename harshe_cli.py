#!/usr/bin/env python3
"""
Harshe CLI - Kayan aikin layin umarni na yaren Harshe
Command-line interface for running, compiling, packaging, inspecting, and managing Harshe code.
"""

import sys
import os
import argparse
import json
import shutil
import subprocess
from pprint import pprint

from harshe import __version__, run_file, run_source, start_repl
from harshe.lexer import Lexer
from harshe.parser import Parser
from harshe.errors import HarsheError


def print_banner() -> None:
    print(f"\033[32mHarshe (HausaLang)\033[0m v{__version__} - Harshen Shirye-shiryen Kwamfuta a Yaren Hausa")


def run_tokens_command(filepath: str) -> None:
    if not os.path.exists(filepath):
        print(f"\033[91mKuskure:\033[0m Ba a sami fayil din '{filepath}' ba.")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        lexer = Lexer(source, filepath)
        tokens = lexer.tokenize()
        print(f"\n--- Alamomin Fayil: {filepath} ({len(tokens)} alamomi) ---")
        for idx, tok in enumerate(tokens):
            val_str = f"'{tok.value}'" if tok.value is not None else ""
            print(f"[{idx:03d}] {tok.type.name:<18} {val_str:<25} (Layi: {tok.start_pos.line}, Jeri: {tok.start_pos.col})")
        print()
    except HarsheError as e:
        print(e)
        sys.exit(1)


def run_ast_command(filepath: str) -> None:
    if not os.path.exists(filepath):
        print(f"\033[91mKuskure:\033[0m Ba a sami fayil din '{filepath}' ba.")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        lexer = Lexer(source, filepath)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source)
        ast = parser.parse()
        print(f"\n--- Bishiyar Nahawu (AST) na Fayil: {filepath} ---")
        pprint(ast)
        print()
    except HarsheError as e:
        print(e)
        sys.exit(1)


def run_file_command(filepath: str) -> None:
    if not os.path.exists(filepath):
        print(f"\033[91mKuskure:\033[0m Ba a sami fayil din '{filepath}' ba.")
        sys.exit(1)

    try:
        run_file(filepath)
    except HarsheError as e:
        print(e)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\033[33m(An dakatar da shirin)\033[0m")
        sys.exit(130)


def create_new_project(project_name: str) -> None:
    """Kirkirar sabon aikin Harshe (Create a new Harshe project template)"""
    if os.path.exists(project_name):
        print(f"\033[91mKuskure:\033[0m Jaka ko fayil mai suna '{project_name}' ya riga ya wanzu.")
        sys.exit(1)

    os.makedirs(os.path.join(project_name, "kayan_aiki"), exist_ok=True)
    os.makedirs(os.path.join(project_name, "gwaje_gwaje"), exist_ok=True)
    os.makedirs(os.path.join(project_name, ".vscode"), exist_ok=True)

    # VS Code Tasks configuration (Run with Ctrl + Shift + B)
    vscode_tasks = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Gudanar da Harshe (Run Project)",
                "type": "shell",
                "command": "harshe run babban_shiri.hausa",
                "group": {
                    "kind": "build",
                    "isDefault": True
                },
                "presentation": {
                    "reveal": "always",
                    "panel": "shared"
                },
                "problemMatcher": []
            }
        ]
    }
    with open(os.path.join(project_name, ".vscode", "tasks.json"), "w", encoding="utf-8") as f:
        json.dump(vscode_tasks, f, indent=2, ensure_ascii=False)


    config = {
        "suna": project_name,
        "siga": "1.0.0",
        "marubuci": "Mai Amfani da Harshe",
        "babban_fayil": "babban_shiri.hausa",
        "harshe_version": __version__
    }
    with open(os.path.join(project_name, "tsari.json"), "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    main_code = f"""# ==========================================
# Babban Shirin {project_name}
# ==========================================

daga "kayan_aiki/taimako.hausa" shigo_da gaisuwa, hada_bayanai;

buga("========================================");
buga("  Barka da zuwa Aikin: {project_name}  ");
buga("========================================");

bari sakon_gaisuwa = gaisuwa("Aboki");
buga(sakon_gaisuwa);

bari bayanin_aikina = hada_bayanai("{project_name}", "1.0.0");
buga("Bayanin Aiki:", bayanin_aikina);
"""
    with open(os.path.join(project_name, "babban_shiri.hausa"), "w", encoding="utf-8") as f:
        f.write(main_code)

    helper_code = """# ==========================================
# Laburaren Taimako (Helper Module)
# ==========================================

aiki gaisuwa(suna) {
    koma "Sannu da zuwa, " + suna + "!";
}

aiki hada_bayanai(sunan_aiki, siga) {
    koma {
        "aiki": sunan_aiki,
        "siga": siga,
        "harshe": "Harshe (HausaLang)"
    };
}
"""
    with open(os.path.join(project_name, "kayan_aiki", "taimako.hausa"), "w", encoding="utf-8") as f:
        f.write(helper_code)

    test_code = """# ==========================================
# Gwajin Aiki (Unit Tests)
# ==========================================

daga "../kayan_aiki/taimako.hausa" shigo_da gaisuwa;

bari g = gaisuwa("Zainab");
idan (g == "Sannu da zuwa, Zainab!") {
    buga("[MADALLA]: Gwajin aikin gaisuwa ya yi nasara!");
} in ba haka ba {
    buga("[KUSKURE]: Gwajin aiki ya gaza!");
}
"""
    with open(os.path.join(project_name, "gwaje_gwaje", "gwada_aiki.hausa"), "w", encoding="utf-8") as f:
        f.write(test_code)

    readme_content = f"""# {project_name}

Wannan aiki ne da aka kirkira ta amfani da **Harshe (HausaLang)**.

## Gudanar da Shirin (Running the Project)
```bash
python harshe_cli.py run {project_name}/babban_shiri.hausa
```
"""
    with open(os.path.join(project_name, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"\n\033[32m[Madalla!]\033[0m An kirkiri sabon aikin Harshe mai suna '\033[1m{project_name}\033[0m' cikin nasara!\n")
    print("Domin gudanar da sabon aikinka:")
    print(f"  \033[36mpython harshe_cli.py run {project_name}/babban_shiri.hausa\033[0m\n")


def compile_to_exe(filepath: str, output_name: str = None) -> None:
    """Hadawa zuwa Standalone Windows Executable (.exe)"""
    if not os.path.exists(filepath):
        print(f"\033[91mKuskure:\033[0m Ba a sami fayil din '{filepath}' ba.")
        sys.exit(1)

    base_name = output_name if output_name else os.path.splitext(os.path.basename(filepath))[0]
    print(f"\033[32m[Harshe Compiler]\033[0m Ana hada fayil din '{filepath}' zuwa '{base_name}.exe'...")

    with open(filepath, "r", encoding="utf-8") as f:
        source_code = f.read()

    build_dir = os.path.abspath(os.path.join(os.getcwd(), "_harshe_build"))
    os.makedirs(build_dir, exist_ok=True)

    # Generate standalone entry python script
    entry_file = os.path.join(build_dir, "entry_point.py")
    harshe_pkg_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "harshe"))
    stdlib_pkg_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "harshe_stdlib"))

    entry_content = f'''import sys
import os

# Embedded Harshe Source
SOURCE_CODE = {repr(source_code)}

from harshe import run_source

def main():
    try:
        run_source(SOURCE_CODE, {repr(filepath)})
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    with open(entry_file, "w", encoding="utf-8") as f:
        f.write(entry_content)

    # Invoke PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", base_name,
        "--distpath", os.path.abspath("dist"),
        "--workpath", os.path.join(build_dir, "work"),
        "--specpath", build_dir,
        f"--paths={os.path.dirname(os.path.abspath(__file__))}",
        entry_file
    ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            exe_path = os.path.join("dist", f"{base_name}.exe" if os.name == 'nt' else base_name)
            print(f"\n\033[32m[MADALLA!]\033[0m An kammala hada shirin cikin nasara!")
            print(f"Fayil din .exe yana nan a: \033[36m{exe_path}\033[0m\n")
        else:
            print(f"\033[91mKuskuren Hada Shirin:\033[0m\n{res.stderr}")
    finally:
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir, ignore_errors=True)


def package_manager(command: str, package_name: str = None) -> None:
    """Tsarin Kula da Kunshin Laburare (Package Manager: kunshi)"""
    kunshiyoyi_dir = os.path.abspath("kunshiyoyi")
    os.makedirs(kunshiyoyi_dir, exist_ok=True)

    if command in ("shigar", "install"):
        if not package_name:
            print("\033[91mKuskure:\033[0m Shigar da sunan kunshi: python harshe_cli.py shigar <sunan_kunshi>")
            sys.exit(1)
        print(f"\033[32m[Kunshi]\033[0m Ana shigar da kunshin '{package_name}' a cikin 'kunshiyoyi/'...")
        pkg_file = os.path.join(kunshiyoyi_dir, f"{package_name}.hausa")
        if not os.path.exists(pkg_file):
            with open(pkg_file, "w", encoding="utf-8") as f:
                f.write(f"# Kunshin Harshe: {package_name}\n# An shigar ta hanyar Harshe Package Manager\n\nbari kunshi_suna = \"{package_name}\";\n")
        print(f"\033[32m[Madalla!]\033[0m An shigar da kunshin '{package_name}' cikin nasara!")

    elif command in ("jerin", "list"):
        print(f"\n--- Kunshiyoyin Da Aka Shigar a Cikin 'kunshiyoyi/' ---")
        items = os.listdir(kunshiyoyi_dir)
        if not items:
            print("  (Babu wani kunshi da aka shigar tukuna)")
        else:
            for it in items:
                print(f"  📦 {it}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Harshe - Injin Harshen Shirye-shiryen Kwamfuta a Yaren Hausa",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Misalai na amfani (Examples):
  python harshe_cli.py run program.hausa     # Gudanar da shirin
  python harshe_cli.py compile prog.hausa    # Hada shirin zuwa .exe
  python harshe_cli.py sabo aikina           # Kirkirar sabon aikin Harshe
  python harshe_cli.py shigar lissafi_mai_iko # Shigar da kunshin laburare
  python harshe_cli.py repl                  # Fara tattaunawa kai-tsaye
  python harshe_cli.py tokens program.hausa  # Bincika alamomin shirin
  python harshe_cli.py ast program.hausa     # Duba bishiyar nahawu (AST)
        """
    )

    parser.add_argument("command_or_file", nargs="?", default="repl", help="Umarni (run, compile, sabo, shigar, repl, tokens, ast, version)")
    parser.add_argument("file_arg", nargs="?", default=None, help="Hanyar fayil ko sunan aiki")
    parser.add_argument("-o", "--output", default=None, help="Sunan fayil din da za a fitar a lokacin 'compile'")
    parser.add_argument("-v", "--version", action="store_true", help="Nuna lambar sigar Harshe")

    args = parser.parse_args()

    if args.version or args.command_or_file == "version":
        print_banner()
        return

    cmd = args.command_or_file

    if cmd == "repl":
        start_repl()
    elif cmd in ("sabo", "new", "init"):
        if not args.file_arg:
            print("\033[91mKuskure:\033[0m Ana bukatar shigar da sunan aiki: python harshe_cli.py sabo <sunan_aiki>")
            sys.exit(1)
        create_new_project(args.file_arg)
    elif cmd in ("compile", "hada"):
        if not args.file_arg:
            print("\033[91mKuskure:\033[0m Ana bukatar shigar da sunan fayil: python harshe_cli.py compile <fayil.hausa>")
            sys.exit(1)
        compile_to_exe(args.file_arg, args.output)
    elif cmd in ("shigar", "install", "kunshi"):
        sub_cmd = "shigar" if cmd in ("shigar", "install") else (args.file_arg or "jerin")
        pkg = args.file_arg if cmd in ("shigar", "install") else args.output
        package_manager(sub_cmd, pkg)
    elif cmd == "run":
        if not args.file_arg:
            print("\033[91mKuskure:\033[0m Ana bukatar shigar da sunan fayil: python harshe_cli.py run <fayil.hausa>")
            sys.exit(1)
        run_file_command(args.file_arg)
    elif cmd == "tokens":
        if not args.file_arg:
            print("\033[91mKuskure:\033[0m Ana bukatar shigar da sunan fayil: python harshe_cli.py tokens <fayil.hausa>")
            sys.exit(1)
        run_tokens_command(args.file_arg)
    elif cmd == "ast":
        if not args.file_arg:
            print("\033[91mKuskure:\033[0m Ana bukatar shigar da sunan fayil: python harshe_cli.py ast <fayil.hausa>")
            sys.exit(1)
        run_ast_command(args.file_arg)
    else:
        if os.path.exists(cmd) or cmd.endswith(".hausa") or cmd.endswith(".har") or cmd.endswith(".hsh"):
            run_file_command(cmd)
        else:
            print(f"\033[91mKuskure:\033[0m Umarnin da ba a sani ba: '{cmd}'")
            parser.print_help()
            sys.exit(1)


if __name__ == "__main__":
    main()

"""
Harshe - Tattaunawa Mai Amsawa (Interactive REPL Module)
Allon tattaunawa kai-tsaye na yaren Hausa (Read-Eval-Print Loop).
"""

import sys
import os
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .environment import Environment
from .values import HarsheNull
from .errors import HarsheError

# Enable Windows ANSI virtual terminal colors
if os.name == 'nt':
    os.system('')

BANNER = """\033[38;2;40;180;120m  _    _                _           
 | |  | |              | |          
 | |__| | __ _ _ __ ___| |__   ___  
 |  __  |/ _` | '__/ __| '_ \\ / _ \\ 
 | |  | | (_| | |  \\__ \\ | | |  __/ 
 |_|  |_|\\__,_|_|  |___/_| |_|\\___| \033[0m

 \033[1mBarka da zuwa Harshe (HausaLang) v1.0.0\033[0m
 Tsarin Harshen Shirye-shiryen Kwamfuta a Yaren Hausa.
 Rubuta \033[33m'taimako'\033[0m domin samun bayanai, ko \033[31m'fita'\033[0m domin rufewa.
"""

HELP_TEXT = """
\033[1mBAYANIN AMFANIN HARSHE (HAUSA QUICK REFERENCE)\033[0m
======================================================
1. \033[32mMasu Canji (Variables):\033[0m
   bari suna = "Aliyu";
   tsayayye PI = 3.14159;

2. \033[32mBuga Bayani (Printing):\033[0m
   buga("Sannu Duniya!");
   buga("Sunana:", suna);

3. \033[32mSharadi (Conditionals):\033[0m
   idan (shekaru >= 18) {
       buga("Babba ne");
   } ko idan (shekaru >= 13) {
       buga("Matashi ne");
   } in ba haka ba {
       buga("Yaro ne");
   }

4. \033[32mMadauki (Loops):\033[0m
   ga i a cikin kewayon(1, 6) {
       buga("Lamba:", i);
   }
   
   bari x = 1;
   yayin da (x <= 5) {
       buga(x);
       x += 1;
   }

5. \033[32mAyyuka (Functions):\033[0m
   aiki gaisuwa(suna) {
       koma "Sannu da aiki, " + suna + "!";
   }
   buga(gaisuwa("Amina"));

6. \033[32mJeri da Kamus (Lists & Dictionaries):\033[0m
   bari 'ya'ya = ["Mangwaro", "Lemu", "Ayaba"];
   kara('ya'ya, "Kankana");
   bari mutum = {"suna": "Umar", "shekaru": 30};
   buga(mutum["suna"]);

7. \033[32mGwada da Kama Kuskure (Try/Catch):\033[0m
   gwada {
       bari r = 10 / 0;
   } kama (kuskure) {
       buga("An samu matsala:", kuskure);
   }

\033[33mUmarnin REPL:\033[0m
- \033[36mtaimako\033[0m         : Nuna wannan bayanin
- \033[36mshare\033[0m           : Share allon rubutu
- \033[36msabo <aiki>\033[0m     : Kirkirar sabon aikin Harshe
- \033[36mmuhalli\033[0m         : Nuna dukkan masu canji da aka ajiye
- \033[36mfita\033[0m            : Fita daga shirin
======================================================
"""


def start_repl() -> None:
    """Fara tattaunawa kai-tsaye"""
    print(BANNER)
    global_env = Environment()
    interpreter = Interpreter(global_env=global_env)

    # Multi-line buffer
    buffer = ""

    while True:
        try:
            prompt = "harshe > " if not buffer else "...     "
            line = input(prompt)

            # Special commands when buffer is empty
            if not buffer:
                trimmed = line.strip()
                trimmed_lower = trimmed.lower()
                
                # Check for exit
                if trimmed_lower in ("fita", "exit", "quit", ":q"):
                    print("\nSai an jima! Mun gode da amfani da Harshe.")
                    break
                elif trimmed_lower in ("taimako", "help"):
                    print(HELP_TEXT)
                    continue
                elif trimmed_lower in ("share", "clear", "cls"):
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue
                elif trimmed_lower in ("muhalli", "env"):
                    user_symbols = {k: v for k, v in global_env.symbols.items() if not v.is_const or k not in interpreter.globals.symbols}
                    print("\nMasu Canjin Muhalli (User Environment):")
                    for k, sym in user_symbols.items():
                        print(f"  {k} = {sym.value.harshe_repr()}")
                    print()
                    continue

                # Handle CLI-style commands inside REPL (e.g. 'harshe sabo <name>' or 'sabo <name>')
                parts = trimmed.split()
                if parts:
                    first = parts[0].lower()
                    
                    # If prefixed with 'harshe', strip it
                    if first == "harshe" and len(parts) > 1:
                        parts = parts[1:]
                        first = parts[0].lower()

                    if first in ("sabo", "new", "init"):
                        project_name = parts[1].rstrip(';') if len(parts) > 1 else None
                        if not project_name:
                            print("\033[91mKuskure:\033[0m Shigar da sunan aiki: sabo <sunan_aiki>")
                        else:
                            try:
                                import harshe_cli
                                harshe_cli.create_new_project(project_name)
                            except Exception as ex:
                                print(f"\033[91mKuskure:\033[0m {ex}")
                        continue
                    elif first in ("shigar", "install"):
                        pkg_name = parts[1].rstrip(';') if len(parts) > 1 else None
                        if not pkg_name:
                            print("\033[91mKuskure:\033[0m Shigar da sunan kunshi: shigar <sunan_kunshi>")
                        else:
                            try:
                                import harshe_cli
                                harshe_cli.package_manager("shigar", pkg_name)
                            except Exception as ex:
                                print(f"\033[91mKuskure:\033[0m {ex}")
                        continue

            buffer += line + "\n"

            # Check if braces, parentheses or quotes are open
            open_braces = buffer.count('{') - buffer.count('}')
            open_parens = buffer.count('(') - buffer.count(')')
            open_brackets = buffer.count('[') - buffer.count(']')

            if open_braces > 0 or open_parens > 0 or open_brackets > 0:
                continue

            # Code is complete, let's run it
            code_to_run = buffer.strip()
            buffer = ""

            if not code_to_run:
                continue

            try:
                # 1. Lexing
                lexer = Lexer(code_to_run, "<tattaunawa>")
                tokens = lexer.tokenize()

                # 2. Parsing
                parser = Parser(tokens, code_to_run)
                ast = parser.parse()

                # 3. Executing
                interpreter.source_code = code_to_run
                result = interpreter.interpret(ast)

                # In REPL, if the last statement was a pure expression returning non-null, display it
                if not isinstance(result, HarsheNull):
                    print(f"\033[32m=>\033[0m {result.harshe_repr()}")

            except HarsheError as e:
                print(e)
            except Exception as e:
                print(f"\n\033[91m[Kuskuren Tsari]\033[0m: {str(e)}\n")

        except KeyboardInterrupt:
            print("\n(An soke shigarwa - Rubuta 'fita' domin rufewa)")
            buffer = ""
        except EOFError:
            print("\nSai an jima!")
            break

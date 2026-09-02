#!/usr/bin/env bash
# ==============================================================================
# Harshe (HausaLang) - Linux / macOS One-Line Installer
# Usage: curl -sSL https://raw.githubusercontent.com/harshe-lang/harshe/main/install.sh | bash
# ==============================================================================

set -e

echo ""
echo -e "\033[32m========================================\033[0m"
echo -e "\033[32m  Shigar da Harshe (HausaLang) a Linux/Mac\033[0m"
echo -e "\033[32m========================================\033[0m"
echo ""

if ! command -v python3 &> /dev/null; then
    echo -e "\033[31m[Kuskure]: Ba a sami python3 a wannan na'ura ba.\033[0m"
    exit 1
fi

INSTALL_DIR="$HOME/.harshe"
rm -rf "$INSTALL_DIR"

echo -e "\033[36m-> Ana saukar da tsarin Harshe daga GitHub...\033[0m"
git clone --depth 1 https://github.com/harshe-lang/harshe.git "$INSTALL_DIR"

echo -e "\033[36m-> Ana shigar da umarnin 'harshe'...\033[0m"
cd "$INSTALL_DIR"
python3 -m pip install -e . --user

echo ""
echo -e "\033[32m========================================================\033[0m"
echo -e "\033[32m[MADALLA!] An shigar da Harshe cikin nasara a kwamfutarka!\033[0m"
echo -e "\033[32m========================================================\033[0m"
echo ""
echo -e "\033[33mDomin fara amfani da Harshe, rubuta:\033[0m"
echo "   harshe repl                       # Domin fara tattaunawa"
echo "   harshe run shiri.hausa            # Domin gudanar da shiri"
echo "   harshe sabo aikina                # Domin kirkirar sabon aiki"
echo ""

# ==============================================================================
# Harshe (HausaLang) - Windows One-Line Installer
# Usage: irm https://raw.githubusercontent.com/harshe-lang/harshe/main/install.ps1 | iex
# ==============================================================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "  ========================================" -ForegroundColor Green
Write-Host "    Shigar da Harshe (HausaLang) a Windows" -ForegroundColor Green
Write-Host "  ========================================" -ForegroundColor Green
Write-Host ""

# Check Python installation
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "[Kuskure]: Ba a sami Python a kwamfutarka ba." -ForegroundColor Red
    Write-Host "Da fatan za a sauke tare da shigar da Python daga: https://www.python.org" -ForegroundColor Yellow
    exit 1
}

Write-Host "-> Ana saukar da tsarin Harshe daga GitHub..." -ForegroundColor Cyan
$installDir = Join-Path $HOME ".harshe"

if (Test-Path $installDir) {
    Remove-Item -Recurse -Force $installDir -ErrorAction SilentlyContinue
}

# Clone or download repository
git clone --depth 1 https://github.com/harshe-lang/harshe.git $installDir

if (-not (Test-Path $installDir)) {
    Write-Host "[Kuskure]: Saukar da fayilolin Harshe ya gaza." -ForegroundColor Red
    exit 1
}

Write-Host "-> Ana shigar da umarnin 'harshe'..." -ForegroundColor Cyan
Set-Location $installDir
python -m pip install -e .

Write-Host ""
Write-Host "  ========================================================" -ForegroundColor Green
Write-Host "  [MADALLA!] An shigar da Harshe cikin nasara a kwamfutarka!" -ForegroundColor Green
Write-Host "  ========================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Domin fara amfani da Harshe, rubuta:" -ForegroundColor Yellow
Write-Host "   harshe repl                       # Domin fara tattaunawa" -ForegroundColor White
Write-Host "   harshe run shiri.hausa            # Domin gudanar da shiri" -ForegroundColor White
Write-Host "   harshe sabo aikina                # Domin kirkirar sabon aiki" -ForegroundColor White
Write-Host ""

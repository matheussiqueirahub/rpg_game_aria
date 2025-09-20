param(
    [switch]$NoConsole
)

if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "Instalando PyInstaller..." -ForegroundColor Yellow
    pip install pyinstaller | Out-Null
}

$consoleFlag = ""
if ($NoConsole) { $consoleFlag = "--noconsole" }

pyinstaller --onefile $consoleFlag --name Aria --icon Aria/assets/aria.ico Aria/main.py

Write-Host "Executável gerado em dist/Aria.exe" -ForegroundColor Green


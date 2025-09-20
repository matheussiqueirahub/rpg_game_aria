param(
    [string]$ZipName = "Aria_Package.zip"
)

# Build
& "$PSScriptRoot/build.ps1" -NoConsole

# Prepare staging folder
$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$staging = Join-Path $root "_staging"
if (Test-Path $staging) { Remove-Item -Recurse -Force $staging }
New-Item -ItemType Directory -Path $staging | Out-Null

# Copy executable
$exe = Join-Path $root "dist\Aria.exe"
if (Test-Path $exe) { Copy-Item $exe -Destination $staging }

# Copy project files
Copy-Item (Join-Path $root "Aria") -Destination $staging -Recurse -Force
if (Test-Path (Join-Path $root "README.md")) { Copy-Item (Join-Path $root "README.md") -Destination $staging }
if (Test-Path (Join-Path $root "LICENSE")) { Copy-Item (Join-Path $root "LICENSE") -Destination $staging }
if (Test-Path (Join-Path $root ".gitignore")) { Copy-Item (Join-Path $root ".gitignore") -Destination $staging }
if (Test-Path (Join-Path $root "requirements-dev.txt")) { Copy-Item (Join-Path $root "requirements-dev.txt") -Destination $staging }

# Create zip in project root
$zipPath = Join-Path $root $ZipName
if (Test-Path $zipPath) { Remove-Item -Force $zipPath }
Compress-Archive -Path "$staging\*" -DestinationPath $zipPath

Write-Host "Pacote gerado:" $zipPath -ForegroundColor Green

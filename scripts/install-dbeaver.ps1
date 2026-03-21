# install-dbeaver.ps1
$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "=== DBeaver Installation startet ===" -ForegroundColor Cyan
Write-Host ""

if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Host "FEHLER: winget ist auf diesem System nicht verfügbar." -ForegroundColor Red
    exit 1
}

$packageId = "dbeaver.dbeaver"

Write-Host "Prüfe, ob DBeaver bereits installiert ist..." -ForegroundColor Yellow
$installed = winget list --id $packageId --exact 2>$null

if ($LASTEXITCODE -eq 0 -and $installed -match "dbeaver") {
    Write-Host "DBeaver ist bereits installiert." -ForegroundColor Green
} else {
    Write-Host "Installiere DBeaver..." -ForegroundColor Yellow
    winget install --id $packageId --exact --accept-package-agreements --accept-source-agreements

    if ($LASTEXITCODE -ne 0) {
        Write-Host "FEHLER: DBeaver konnte nicht installiert werden." -ForegroundColor Red
        exit 1
    }

    Write-Host "DBeaver wurde erfolgreich installiert." -ForegroundColor Green
}

$paths = @(
    "$Env:ProgramFiles\DBeaver\dbeaver.exe",
    "$Env:ProgramFiles\DBeaver Community\dbeaver.exe",
    "$Env:LOCALAPPDATA\Programs\DBeaver\dbeaver.exe"
)

$exe = $paths | Where-Object { Test-Path $_ } | Select-Object -First 1

if ($exe) {
    Write-Host "Starte DBeaver..." -ForegroundColor Yellow
    Start-Process $exe
    Write-Host "FERTIG: DBeaver wurde gestartet." -ForegroundColor Green
} else {
    Write-Host "DBeaver wurde installiert, aber die EXE wurde nicht automatisch gefunden." -ForegroundColor Yellow
    Write-Host "Bitte starte DBeaver einmal manuell über das Startmenü." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Installation abgeschlossen ===" -ForegroundColor Cyan
Write-Host ""
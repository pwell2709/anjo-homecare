$ErrorActionPreference = "Stop"

$sourceFolder = "src/assets/images/locations"
$targetWidth = 600
$quality = 82

if (-not (Test-Path $sourceFolder)) {
    Write-Error "Ordner nicht gefunden: $sourceFolder"
}

$magickCmd = Get-Command magick -ErrorAction SilentlyContinue
if (-not $magickCmd) {
    Write-Error "ImageMagick wurde nicht gefunden. Bitte zuerst installieren."
}

$files = Get-ChildItem -Path $sourceFolder -Filter *.webp -File

if (-not $files) {
    Write-Host "Keine .webp-Dateien gefunden in $sourceFolder"
    exit 0
}

foreach ($file in $files) {

    Write-Host ""
    Write-Host "Prüfe: $($file.Name)"

    $widthOutput = & magick identify -format "%w" $file.FullName 2>$null
    if (-not $widthOutput) {
        Write-Warning "Breite konnte nicht gelesen werden: $($file.Name)"
        continue
    }

    $currentWidth = [int]$widthOutput

    if ($currentWidth -le $targetWidth) {
        Write-Host "Übersprungen: bereits $currentWidth px breit"
        continue
    }

    $tempFile = Join-Path $file.DirectoryName ($file.BaseName + ".__tmp__.webp")

    & magick $file.FullName `
        -resize "${targetWidth}x" `
        -quality $quality `
        -define webp:method=6 `
        -define webp:auto-filter=true `
        $tempFile

    if (-not (Test-Path $tempFile)) {
        Write-Warning "Fehler beim Verarbeiten: $($file.Name)"
        continue
    }

    Move-Item -Force $tempFile $file.FullName

    $newWidth = & magick identify -format "%w" $file.FullName
    Write-Host "Verkleinert: $currentWidth px -> $newWidth px"
}

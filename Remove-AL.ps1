# Root-Verzeichnis deines Projekts
$root = "_site"

Write-Host "Suche nach allen /al Ordnern im Projekt..." -ForegroundColor Cyan

# Alle Ordner finden, die exakt 'al' heißen
$alFolders = Get-ChildItem -Path $root -Recurse -Directory | Where-Object { $_.Name -eq "al" }

if ($alFolders.Count -eq 0) {
    Write-Host "Keine /al Ordner gefunden. Alles sauber." -ForegroundColor Green
    return
}

foreach ($folder in $alFolders) {
    Write-Host "Lösche: $($folder.FullName)" -ForegroundColor Yellow
    Remove-Item -Path $folder.FullName -Recurse -Force
}

Write-Host "Fertig. Alle /al Ordner wurden vollständig entfernt." -ForegroundColor Green

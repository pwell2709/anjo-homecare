# ============================================
# SLUG AUDIT
# Prüft Projekt auf alte Landing-Strukturen
# ============================================

$patterns = @(
"/al/",
"al-madeira",
"cleaning-for-al",
"nettoyage-al",
"limpeza-al"
)

Write-Host ""
Write-Host "Checking project for forbidden slugs..."
Write-Host ""

foreach ($pattern in $patterns) {

    $results = Select-String -Path "src\**\*.njk","src\**\*.js" -Pattern $pattern

    if ($results) {

        Write-Host ""
        Write-Host "Found: $pattern"
        $results | ForEach-Object {
            Write-Host $_.Path ":" $_.LineNumber
        }

    }

}

Write-Host ""
Write-Host "Audit finished."
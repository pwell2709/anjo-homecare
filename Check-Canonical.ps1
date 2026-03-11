$root = "_site"

Write-Host ""
Write-Host "Checking canonical tags..."
Write-Host ""

$files = Get-ChildItem -Path $root -Recurse -Include index.html

foreach ($f in $files) {

    $file = $f.FullName
    $content = Get-Content $file -Raw

    # Canonical extrahieren
    $canonical = $null
    if ($content -match '<link rel="canonical" href="([^"]+)"') {
        $canonical = $matches[1]
    }

    if ($canonical -eq $null) {
        Write-Host "ERROR: No canonical tag in $file"
        continue
    }

    # Sprache aus Pfad extrahieren
    $lang = $null
    if ($file -match "\\en\\") { $lang = "en" }
    elseif ($file -match "\\de\\") { $lang = "de" }
    elseif ($file -match "\\fr\\") { $lang = "fr" }
    elseif ($file -match "\\pt\\") { $lang = "pt" }

    if ($lang -eq $null) {
        Write-Host "SKIPPED (no language folder): $file"
        continue
    }

    # Web-Pfad extrahieren

# Fall 1: /lang/unterordner/index.html
if ($file -match "\\(en|de|fr|pt)\\(.+)\\index\.html$") {
    $lang = $matches[1]
    $rest = $matches[2]

    # Backslashes ersetzen
    $rest = $rest -replace "\\", "/"

    $webPath = "/" + $lang + "/" + $rest + "/"
}
# Fall 2: /lang/index.html
elseif ($file -match "\\(en|de|fr|pt)\\index\.html$") {
    $lang = $matches[1]
    $webPath = "/" + $lang + "/"
}
else {
    Write-Host "SKIPPED (cannot parse path): $file"
    continue
}



    # Erwartete absolute URL
    $expectedCanonical = "https://anjo-cleaning.com" + $webPath

    # Vergleich
    if ($canonical -eq $expectedCanonical) {
        Write-Host "OK: $file"
    } else {
        Write-Host "ERROR in $file"
        Write-Host "  Expected: $expectedCanonical"
        Write-Host "  Found:    $canonical"
    }
}

Write-Host ""
Write-Host "Canonical check completed."

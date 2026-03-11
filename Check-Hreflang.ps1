$root = "_site"   # <-- anpassen, falls dein Output-Ordner anders heißt

Write-Host ""
Write-Host "Checking hreflang tags..."
Write-Host ""

$files = Get-ChildItem -Path $root -Recurse -Include *.html

foreach ($f in $files) {

    $file = $f.FullName
    $content = Get-Content $file -Raw

    # Alle hreflang-Tags extrahieren
    $matches = Select-String -InputObject $content -Pattern 'rel="alternate"' -AllMatches

    if ($matches.Count -eq 0) {
        Write-Host "ERROR: No hreflang tags in $file"
        continue
    }

    # Dictionary für gefundene Werte
    $found = @{
        en = $null
        de = $null
        fr = $null
        pt = $null
        "x-default" = $null
    }

    # Zeilenweise prüfen
    $lines = $content -split "`n"

    foreach ($line in $lines) {

        if ($line -match 'hreflang="([^"]+)"') {
            $lang = $matches[1]

            if ($line -match 'href="([^"]+)"') {
                $url = $matches[1]

                if ($found.ContainsKey($lang)) {
                    $found[$lang] = $url
                }
            }
        }
    }

    # Prüfen, ob alle Sprachen vorhanden sind
    $errors = @()

    foreach ($code in @("en","de","fr","pt","x-default")) {
        if ($found[$code] -eq $null) {
            $errors += ("Missing hreflang: " + $code)
        }
    }

    if ($errors.Count -eq 0) {
        Write-Host "OK: $file"
    } else {
        Write-Host "ERRORS in $file"
        foreach ($err in $errors) {
            Write-Host "  -> $err"
        }
    }
}

Write-Host ""
Write-Host "Hreflang check completed."

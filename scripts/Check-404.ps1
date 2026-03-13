$root = "_site"
$domain = "https://anjo-cleaning.com"

Write-Host ""
Write-Host "Checking URLs for 404 errors..."
Write-Host ""

# Funktion: URL testen
function Test-Url {
    param([string]$url)

    # Basic Auth Credentials (NUR LOKAL EINTRAGEN)
    $username = "florian"
    $password = "madeira26"

    # Basic Auth Header erzeugen
    $pair = "$username`:$password"
    $bytes = [System.Text.Encoding]::ASCII.GetBytes($pair)
    $base64 = [System.Convert]::ToBase64String($bytes)
    $authHeader = "Basic $base64"

    try {
        $response = Invoke-WebRequest `
            -Uri $url `
            -Method Head `
            -Headers @{ Authorization = $authHeader } `
            -TimeoutSec 10 `
            -ErrorAction Stop

        return $response.StatusCode
    }
    catch {
        return 404
    }
}


# HTML-Dateien sammeln
$files = Get-ChildItem -Path $root -Recurse -Include *.html

foreach ($f in $files) {

    $file = $f.FullName
    $content = Get-Content $file -Raw

    Write-Host ""
    Write-Host "FILE: $file"

    $urls = @()

    # Canonical extrahieren
    if ($content -match '<link rel="canonical" href="([^"]+)"') {
        $urls += $matches[1]
    }

    # hreflang extrahieren
    $hreflangMatches = Select-String -InputObject $content -Pattern 'rel="alternate"' -AllMatches
    foreach ($m in $hreflangMatches) {
        if ($m.Line -match 'href="([^"]+)"') {
            $urls += $matches[1]
        }
    }

    # interne Links extrahieren
    $linkMatches = Select-String -InputObject $content -Pattern '<a\s+[^>]*href="([^"]+)"' -AllMatches
    foreach ($m in $linkMatches) {
        if ($m.Line -match 'href="([^"]+)"') {
            $href = $matches[1]

            # Nur interne Links prüfen
            if ($href.StartsWith("/")) {
                $urls += ($domain + $href)
            }
        }
    }

    # Duplikate entfernen
    $urls = $urls | Sort-Object -Unique

    # URLs testen
    foreach ($url in $urls) {
        $status = Test-Url $url

        if ($status -eq 200) {
            Write-Host "  OK   $url"
        }
        else {
            Write-Host "  404  $url"
        }
    }
}

Write-Host ""
Write-Host "404 check completed."

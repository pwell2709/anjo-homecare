$ErrorActionPreference = "Stop"

$Root = (Get-Location).Path

$TextExtensions = @(
    ".html", ".htm", ".njk", ".md", ".txt", ".xml", ".json",
    ".js", ".mjs", ".cjs", ".css", ".scss", ".yml", ".yaml",
    ".php"
)

$SkipDirs = @(
    "\.git\",
    "\node_modules\",
    "\.cache\",
    "\.parcel-cache\"
)

$ChangedFiles = 0
$RemainingHits = New-Object System.Collections.Generic.List[string]

function Test-IsTextFile {
    param([System.IO.FileInfo]$File)

    if ($File.Name -eq ".eleventy.js") {
        return $true
    }

    return $TextExtensions -contains $File.Extension.ToLower()
}

function Test-IsSkippedPath {
    param([string]$Path)

    foreach ($skip in $SkipDirs) {
        if ($Path -like "*$skip*") {
            return $true
        }
    }
    return $false
}

function Add-KeyholdingToKeywords {
    param([string]$Content)

    $pattern = '<meta\s+name\s*=\s*["'']keywords["'']\s+content\s*=\s*(["''])(.*?)\1'

    return [regex]::Replace(
        $Content,
        $pattern,
        {
            param($match)

            $quote = $match.Groups[1].Value
            $keywords = $match.Groups[2].Value

            $items = @()
            foreach ($item in ($keywords -split ",")) {
                $trimmed = $item.Trim()
                if ($trimmed.Length -gt 0) {
                    $items += $trimmed
                }
            }

            $hasKeyholding = $false
            foreach ($item in $items) {
                if ($item.Trim().ToLower() -eq "keyholding") {
                    $hasKeyholding = $true
                    break
                }
            }

            if (-not $hasKeyholding) {
                $items = @("Keyholding") + $items
            }

            $newKeywords = ($items -join ", ")
            return '<meta name="keywords" content=' + $quote + $newKeywords + $quote
        },
        [System.Text.RegularExpressions.RegexOptions]::IgnoreCase
    )
}

function Replace-HomeCareTextOnly {
    param([string]$Content)

    $updated = $Content

    # Harte Ersetzung aller normalen Schreibweisen
    $updated = [regex]::Replace($updated, '(?i)\bhome[\s\-]+care\b', 'Property Care')

    # Falls irgendwo exakt "HOME CARE" komplett groß erwischt werden soll
    $updated = $updated.Replace("PROPERTY CARE", "Property Care")

    return $updated
}

$Files = Get-ChildItem -Path $Root -Recurse -File

foreach ($file in $Files) {
    if (Test-IsSkippedPath -Path $file.FullName) {
        continue
    }

    if (-not (Test-IsTextFile -File $file)) {
        continue
    }

    try {
        $original = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
    }
    catch {
        continue
    }

    $updated = $original

    # Nur Textinhalt ändern, keine Dateinamen/Ordnernamen
    $updated = Replace-HomeCareTextOnly -Content $updated

    # Keywords ergänzen
    $updated = Add-KeyholdingToKeywords -Content $updated

    if ($updated -ne $original) {
        [System.IO.File]::WriteAllText($file.FullName, $updated, [System.Text.UTF8Encoding]::new($false))
        $ChangedFiles++
    }
}

$CheckFiles = Get-ChildItem -Path $Root -Recurse -File

foreach ($file in $CheckFiles) {
    if (Test-IsSkippedPath -Path $file.FullName) {
        continue
    }

    if (-not (Test-IsTextFile -File $file)) {
        continue
    }

    try {
        $content = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
    }
    catch {
        continue
    }

    if ($content -match '(?i)\bhome[\s\-]+care\b') {
        $RemainingHits.Add($file.FullName)
    }
}

Write-Host ""
Write-Host "Geänderte Dateien: $ChangedFiles"

if ($RemainingHits.Count -gt 0) {
    Write-Host ""
    Write-Host "WARNUNG: Noch Treffer gefunden in:"
    $RemainingHits | ForEach-Object { Write-Host $_ }
}
else {
    Write-Host ""
    Write-Host "Erfolg: Kein 'Home Care' / 'Home-Care' mehr in Textdateien gefunden."
}
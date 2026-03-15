$ErrorActionPreference = "Stop"

$cssFile = "src/assets/css/components.css"

$locationDirs = @(
    "src/de/orte",
    "src/en/locations",
    "src/fr/lieux",
    "src/pt/locais"
)

function Get-LocationImageFile {
    param([string]$Href)

    $slug = ($Href.TrimEnd("/") -split "/")[-1].ToLowerInvariant()

    $map = @{
        "boaventura"          = "Boaventura.webp"
        "calheta"             = "Calheta.webp"
        "camara-de-lobos"     = "Camara_de_Lobos.webp"
        "campanario"          = "Campanario.webp"
        "canico"              = "Canico.webp"
        "curral-das-freiras"  = "Curral_das_Freiras.webp"
        "funchal"             = "Funchal.webp"
        "jardim-do-mar"       = "Jardim_do_Mar.webp"
        "paul-do-mar"         = "Paul_do_Mar.webp"
        "ponta-do-pargo"      = "Ponta_do_Pargo.webp"
        "ponta-do-sol"        = "Ponta_do_Sol.webp"
        "porto-moniz"         = "Porto_Moniz.webp"
        "ribeira-brava"       = "Ribeira_Brava.webp"
        "santa-cruz"          = "Santa_Cruz.webp"
        "santana"             = "Santana.webp"
        "sao-jorge"           = "Sao_Jorge.webp"
        "sao-vicente"         = "Sao_Vicente.webp"
    }

    if ($map.ContainsKey($slug)) {
        return $map[$slug]
    }

    throw "Kein Bild-Mapping gefunden für Slug: $slug"
}

function Update-LocationPreviewMarkup {
    param([string]$Content)

    if ($Content -notmatch 'sectionList--locationsGrid') {
        return $Content
    }

    if ($Content -match 'location-preview-card') {
        return $Content
    }

    $pattern = '<li><a class="cta-link" href="(?<href>[^"]+)">(?<label>.*?)</a></li>'

    $updated = [regex]::Replace(
        $Content,
        $pattern,
        [System.Text.RegularExpressions.MatchEvaluator]{
            param($match)

            $href  = $match.Groups["href"].Value
            $label = $match.Groups["label"].Value
            $img   = Get-LocationImageFile -Href $href

            return @"
<li class="location-preview-card"><img class="location-preview-image" src="/assets/images/locations/$img" alt="$label" loading="lazy" decoding="async"><a class="cta-link" href="$href">$label</a></li>
"@
        }
    )

    return $updated
}

function Ensure-LocationPreviewCss {
    param([string]$CssPath)

    if (-not (Test-Path $CssPath)) {
        throw "CSS-Datei nicht gefunden: $CssPath"
    }

    $css = Get-Content $CssPath -Raw -Encoding UTF8

    if ($css -match 'LOCATION PREVIEW IMAGES') {
        Write-Host "CSS bereits vorhanden: $CssPath"
        return
    }

    $cssBlock = @"

/* === LOCATION PREVIEW IMAGES === */
.prose-page ul.sectionList.sectionList--locationsGrid li.location-preview-card{
  display:flex;
  flex-direction:column;
  align-items:stretch;
}

.prose-page ul.sectionList.sectionList--locationsGrid img.location-preview-image{
  display:block;
  width:100%;
  height:auto;
  aspect-ratio: 16 / 10;
  object-fit: cover;
  border-radius: 16px;
  margin: 0 0 8px 0;
}
"@

    Set-Content -Path $CssPath -Value ($css.TrimEnd() + "`r`n`r`n" + $cssBlock.Trim() + "`r`n") -Encoding UTF8
    Write-Host "CSS ergänzt: $CssPath"
}

Ensure-LocationPreviewCss -CssPath $cssFile

foreach ($dir in $locationDirs) {
    if (-not (Test-Path $dir)) {
        throw "Ordner nicht gefunden: $dir"
    }

    $files = Get-ChildItem -Path $dir -Recurse -Filter index.njk -File

    foreach ($file in $files) {
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        $updated = Update-LocationPreviewMarkup -Content $content

        if ($updated -ne $content) {
            Set-Content -Path $file.FullName -Value $updated -Encoding UTF8
            Write-Host "Aktualisiert: $($file.FullName)"
        }
        else {
            Write-Host "Unverändert: $($file.FullName)"
        }
    }
}

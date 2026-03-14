# check-meta-seo-strict.ps1
# Prüft 6 Live-URLs auf Title, Meta Description und Canonical

$urls = @(
    "https://anjo-cleaning.com/de/",
    "https://anjo-cleaning.com/en/",
    "https://anjo-cleaning.com/fr/",
    "https://anjo-cleaning.com/pt/",
    "https://anjo-cleaning.com/en/contact/",
    "https://anjo-cleaning.com/de/services/"
)

function Get-Matches {
    param(
        [string]$Html,
        [string]$Pattern
    )

    return [regex]::Matches(
        $Html,
        $Pattern,
        [System.Text.RegularExpressions.RegexOptions]::IgnoreCase -bor
        [System.Text.RegularExpressions.RegexOptions]::Singleline
    )
}

function Get-AttributeValue {
    param(
        [string]$Tag,
        [string]$AttributeName
    )

    $pattern = $AttributeName + '\s*=\s*["''](.*?)["'']'
    $m = [regex]::Match(
        $Tag,
        $pattern,
        [System.Text.RegularExpressions.RegexOptions]::IgnoreCase -bor
        [System.Text.RegularExpressions.RegexOptions]::Singleline
    )

    if ($m.Success) {
        return [System.Net.WebUtility]::HtmlDecode($m.Groups[1].Value).Trim()
    }

    return $null
}

$results = foreach ($url in $urls) {
    try {
        $response = Invoke-WebRequest -Uri $url -MaximumRedirection 10 -ErrorAction Stop
        $html = $response.Content

        $finalUrl = $response.BaseResponse.ResponseUri.AbsoluteUri
        $statusCode = [int]$response.StatusCode

        # TITLE
        $titleMatch = [regex]::Match(
            $html,
            '<title[^>]*>(.*?)</title>',
            [System.Text.RegularExpressions.RegexOptions]::IgnoreCase -bor
            [System.Text.RegularExpressions.RegexOptions]::Singleline
        )

        $title = ""
        $titleLength = 0
        $titleCheck = ""

        if ($titleMatch.Success) {
            $title = [System.Net.WebUtility]::HtmlDecode($titleMatch.Groups[1].Value).Trim()
            $titleLength = $title.Length

            if ($titleLength -eq 0) {
                $titleCheck = "TITLE LEER"
            }
            elseif ($titleLength -le 60) {
                $titleCheck = "OK"
            }
            else {
                $titleCheck = "ZU LANG"
            }
        }
        else {
            $titleCheck = "FEHLT"
        }

        # META DESCRIPTION
        $metaMatches = Get-Matches -Html $html -Pattern '<meta\b[^>]*>'
        $descriptionTags = @()

        foreach ($tagMatch in $metaMatches) {
            $tag = $tagMatch.Value
            $nameAttr = Get-AttributeValue -Tag $tag -AttributeName 'name'

            if ($nameAttr -and $nameAttr.ToLower() -eq 'description') {
                $descriptionTags += $tag
            }
        }

        $metaCount = $descriptionTags.Count
        $description = ""
        $descriptionLength = 0
        $descriptionCheck = ""

        if ($metaCount -eq 0) {
            $descriptionCheck = "FEHLT"
        }
        elseif ($metaCount -gt 1) {
            $descriptionCheck = "MEHRFACH"
            $description = (Get-AttributeValue -Tag $descriptionTags[0] -AttributeName 'content')
            if ($description) {
                $descriptionLength = $description.Length
            }
        }
        else {
            $description = Get-AttributeValue -Tag $descriptionTags[0] -AttributeName 'content'
            if (-not $description) {
                $description = ""
            }

            $descriptionLength = $description.Length

            if ($descriptionLength -eq 0) {
                $descriptionCheck = "LEER"
            }
            elseif ($descriptionLength -le 135) {
                $descriptionCheck = "OK"
            }
            else {
                $descriptionCheck = "ZU LANG"
            }
        }

        # CANONICAL
        $linkMatches = Get-Matches -Html $html -Pattern '<link\b[^>]*>'
        $canonicalTags = @()

        foreach ($tagMatch in $linkMatches) {
            $tag = $tagMatch.Value
            $relAttr = Get-AttributeValue -Tag $tag -AttributeName 'rel'

            if ($relAttr -and $relAttr.ToLower() -eq 'canonical') {
                $canonicalTags += $tag
            }
        }

        $canonicalCount = $canonicalTags.Count
        $canonicalHref = ""
        $canonicalCheck = ""

        if ($canonicalCount -eq 0) {
            $canonicalCheck = "FEHLT"
        }
        elseif ($canonicalCount -gt 1) {
            $canonicalCheck = "MEHRFACH"
            $canonicalHref = Get-AttributeValue -Tag $canonicalTags[0] -AttributeName 'href'
        }
        else {
            $canonicalHref = Get-AttributeValue -Tag $canonicalTags[0] -AttributeName 'href'
            if ([string]::IsNullOrWhiteSpace($canonicalHref)) {
                $canonicalCheck = "LEER"
            }
            else {
                $canonicalCheck = "OK"
            }
        }

        # GESAMTWERTUNG
        $issues = @()

        if ($statusCode -ne 200) { $issues += "HTTP" }
        if ($titleCheck -ne "OK") { $issues += "TITLE" }
        if ($descriptionCheck -ne "OK") { $issues += "DESC" }
        if ($canonicalCheck -ne "OK") { $issues += "CANONICAL" }

        $overall = if ($issues.Count -eq 0) { "OK" } else { $issues -join ", " }

        [PSCustomObject]@{
            URL                 = $url
            FinalURL            = $finalUrl
            StatusCode          = $statusCode
            TitleLength         = $titleLength
            TitleCheck          = $titleCheck
            MetaDescCount       = $metaCount
            MetaDescLength      = $descriptionLength
            MetaDescCheck       = $descriptionCheck
            CanonicalCount      = $canonicalCount
            CanonicalCheck      = $canonicalCheck
            Overall             = $overall
            Title               = $title
            MetaDescription     = $description
            CanonicalHref       = $canonicalHref
        }
    }
    catch {
        [PSCustomObject]@{
            URL                 = $url
            FinalURL            = ""
            StatusCode          = ""
            TitleLength         = ""
            TitleCheck          = "REQUEST FEHLER"
            MetaDescCount       = ""
            MetaDescLength      = ""
            MetaDescCheck       = "REQUEST FEHLER"
            CanonicalCount      = ""
            CanonicalCheck      = "REQUEST FEHLER"
            Overall             = "REQUEST FEHLER"
            Title               = ""
            MetaDescription     = $_.Exception.Message
            CanonicalHref       = ""
        }
    }
}

Write-Host ""
Write-Host "===== KOMPAKTE ÜBERSICHT =====" -ForegroundColor Cyan
$results | Select-Object URL, StatusCode, TitleLength, TitleCheck, MetaDescCount, MetaDescLength, MetaDescCheck, CanonicalCount, CanonicalCheck, Overall | Format-Table -AutoSize

Write-Host ""
Write-Host "===== NUR PROBLEME =====" -ForegroundColor Yellow
$problemRows = $results | Where-Object { $_.Overall -ne "OK" }

if ($problemRows) {
    $problemRows | Select-Object URL, StatusCode, TitleCheck, MetaDescCheck, CanonicalCheck, Overall | Format-Table -AutoSize
}
else {
    Write-Host "Keine Probleme gefunden." -ForegroundColor Green
}

Write-Host ""
Write-Host "===== DETAILS =====" -ForegroundColor Cyan
foreach ($row in $results) {
    Write-Host "------------------------------------------------------------"
    Write-Host "URL:              $($row.URL)"
    Write-Host "FinalURL:         $($row.FinalURL)"
    Write-Host "StatusCode:       $($row.StatusCode)"
    Write-Host "TitleCheck:       $($row.TitleCheck)"
    Write-Host "TitleLength:      $($row.TitleLength)"
    Write-Host "MetaDescCount:    $($row.MetaDescCount)"
    Write-Host "MetaDescCheck:    $($row.MetaDescCheck)"
    Write-Host "MetaDescLength:   $($row.MetaDescLength)"
    Write-Host "CanonicalCount:   $($row.CanonicalCount)"
    Write-Host "CanonicalCheck:   $($row.CanonicalCheck)"
    Write-Host "Overall:          $($row.Overall)"
    Write-Host "Title:            $($row.Title)"
    Write-Host "Description:      $($row.MetaDescription)"
    Write-Host "CanonicalHref:    $($row.CanonicalHref)"
}

# Optional CSV Export
$csvPath = ".\meta-seo-check-results.csv"
$results | Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8
Write-Host ""
Write-Host "CSV gespeichert: $csvPath" -ForegroundColor Green
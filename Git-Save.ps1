param(
    [string]$message = "Update"
)

Write-Host "🔵 Git: Änderungen hinzufügen..." -ForegroundColor Cyan
git add .

Write-Host "🟣 Git: Commit erstellen..." -ForegroundColor Cyan
git commit -m "$message"

Write-Host "🟡 Git: Remote-Änderungen holen (rebase)..." -ForegroundColor Cyan
git pull --rebase

Write-Host "🟢 Git: Änderungen hochladen..." -ForegroundColor Cyan
git push

Write-Host "✅ Fertig! Alles gespeichert und gepusht." -ForegroundColor Green

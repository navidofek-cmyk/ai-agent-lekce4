# Testovací PowerShell skript pro AI Agenta
# Spuštění: .\test_agent.ps1

$webhookUrl = "http://localhost:5678/webhook/ask-agent"

$questions = @(
    "Kolik máme celkem produktů?",
    "Jaká je průměrná cena všech produktů?",
    "Které produkty máme v kategorii Elektronika?",
    "Který produkt je nejdražší?",
    "Které produkty mají zásoby menší než 10 kusů?",
    "Jaká je celková hodnota skladových zásob?",
    "Porovnej kategorii Elektronika a Oblečení",
    "Udělej analýzu produktového portfolia"
)

Write-Host "`n=== Test AI Agenta s Databází ===" -ForegroundColor Green
Write-Host "Webhook URL: $webhookUrl" -ForegroundColor Gray
Write-Host "Počet testů: $($questions.Count)" -ForegroundColor Gray
Write-Host ""

$successCount = 0
$errorCount = 0

for ($i = 0; $i -lt $questions.Count; $i++) {
    $question = $questions[$i]
    $testNum = $i + 1
    
    Write-Host "[$testNum/$($questions.Count)] " -NoNewline -ForegroundColor Magenta
    Write-Host "Q: " -NoNewline -ForegroundColor Cyan
    Write-Host $question
    
    $body = @{
        question = $question
    } | ConvertTo-Json -Compress
    
    try {
        $response = Invoke-RestMethod -Uri $webhookUrl -Method Post -Body $body -ContentType "application/json" -TimeoutSec 30
        
        Write-Host "A: " -NoNewline -ForegroundColor Yellow
        Write-Host $response -ForegroundColor White
        $successCount++
    } 
    catch {
        Write-Host "ERROR: " -NoNewline -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        $errorCount++
    }
    
    Write-Host ("-" * 80) -ForegroundColor DarkGray
    
    if ($i -lt $questions.Count - 1) {
        Start-Sleep -Seconds 2
    }
}

Write-Host ""
Write-Host "=== Souhrn testování ===" -ForegroundColor Green
Write-Host "Úspěšné: $successCount/$($questions.Count)" -ForegroundColor Green
Write-Host "Chybné: $errorCount/$($questions.Count)" -ForegroundColor $(if ($errorCount -gt 0) { "Red" } else { "Green" })
Write-Host ""

if ($errorCount -eq 0) {
    Write-Host "✓ Všechny testy proběhly úspěšně!" -ForegroundColor Green
} else {
    Write-Host "✗ Některé testy selhaly. Zkontrolujte konfiguraci." -ForegroundColor Yellow
}

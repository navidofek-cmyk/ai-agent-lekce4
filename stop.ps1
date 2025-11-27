# Zastavit AI Agenta
# Použití: .\stop.ps1

Write-Host "`n🛑 Zastavuji AI Agenta..." -ForegroundColor Yellow

docker-compose down

Write-Host "✅ Zastaveno!" -ForegroundColor Green
Write-Host "`nPro spuštění:" -ForegroundColor Gray
Write-Host "  SIMULATOR: .\start-simulator.ps1" -ForegroundColor Cyan
Write-Host "  OPENAI:    .\start-openai.ps1" -ForegroundColor Cyan

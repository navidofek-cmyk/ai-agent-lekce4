# Spustit AI Agenta v SIMULATOR režimu (ZDARMA, žádný API klíč)
# Použití: .\start-simulator.ps1

Write-Host "`n🤖 Spouštím AI Agenta - SIMULATOR režim (ZDARMA)" -ForegroundColor Green
Write-Host $("-"*60) -ForegroundColor Gray

# Zastavit běžící kontejnery
Write-Host "`n1️⃣ Zastavuji běžící kontejnery..." -ForegroundColor Cyan
docker-compose down 2>$null

# Nastavit SIMULATOR režim
Write-Host "2️⃣ Konfiguruji SIMULATOR režim..." -ForegroundColor Cyan
$env:LLM_MODE = "simulator"
Remove-Item .env -ErrorAction SilentlyContinue
"LLM_MODE=simulator" | Out-File -FilePath .env -Encoding utf8

# Spustit s původním Dockerfile (bez OpenAI)
Write-Host "3️⃣ Sestavuji a spouštím kontejner..." -ForegroundColor Cyan

# Dočasně změnit Dockerfile
Copy-Item Dockerfile Dockerfile.backup -Force
@"
FROM python:3.11-slim
WORKDIR /app
COPY python_agent_extended.py .
RUN mkdir -p /app/data
ENV PYTHONUNBUFFERED=1
ENV LLM_MODE=simulator
EXPOSE 8000
CMD ["python", "python_agent_extended.py"]
"@ | Out-File -FilePath Dockerfile -Encoding utf8

docker-compose up --build -d

# Obnovit Dockerfile
Move-Item Dockerfile.backup Dockerfile -Force

Write-Host ""
Write-Host "SIMULATOR rezim bezi!" -ForegroundColor Green
Write-Host "Zadny API klic neni potreba" -ForegroundColor Yellow
Write-Host "Web rozhrani: http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "Pro zastaveni: docker-compose down" -ForegroundColor Gray
Write-Host $("-"*60) -ForegroundColor Gray

Start-Sleep -Seconds 2
docker-compose logs --tail 15 ai-agent

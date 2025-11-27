# Spustit AI Agenta s OpenAI API (vyzaduje API klic)
# Pouziti: .\start-openai.ps1

Write-Host ""
Write-Host "Spoustim AI Agenta - OPENAI rezim (GPT)" -ForegroundColor Green
Write-Host $("-"*60) -ForegroundColor Gray

# Zastavit bezici kontejnery
Write-Host ""
Write-Host "1) Zastavuji bezici kontejnery..." -ForegroundColor Cyan
docker-compose down 2>$null

# Nacist API klic
$apiKeyFile = "my_api_key.py"
if (Test-Path $apiKeyFile) {
    Write-Host "2) Nacitam API klic z $apiKeyFile..." -ForegroundColor Cyan
    $content = Get-Content $apiKeyFile -Raw
    if ($content -match 'API_KEY\s*=\s*"([^"]+)"') {
        $apiKey = $matches[1]
        Write-Host "   API klic nalezen" -ForegroundColor Green
    } elseif ($content -match '"(sk-[^"]+)"') {
        $apiKey = $matches[1]
        Write-Host "   API klic nalezen" -ForegroundColor Green
    } else {
        Write-Host "   API klic nenalezen v souboru!" -ForegroundColor Red
        $apiKey = Read-Host "Zadejte API klic rucne"
    }
} else {
    Write-Host "2) Soubor $apiKeyFile neexistuje" -ForegroundColor Yellow
    $apiKey = Read-Host "Zadejte vas OpenAI API klic"
}

# Vytvorit .env
Write-Host "3) Konfiguruji OPENAI rezim..." -ForegroundColor Cyan
@"
LLM_MODE=openai
OPENAI_API_KEY=$apiKey
"@ | Out-File -FilePath .env -Encoding utf8

# Spustit s OpenAI podporou
Write-Host "4) Sestavuji a spoustim kontejner..." -ForegroundColor Cyan

# Dočasně změnit Dockerfile s OpenAI
Copy-Item Dockerfile Dockerfile.backup -Force
@"
FROM python:3.11-slim
WORKDIR /app
COPY python_agent_extended.py .
RUN pip install --no-cache-dir openai
RUN mkdir -p /app/data
ENV PYTHONUNBUFFERED=1
ENV LLM_MODE=openai
EXPOSE 8000
CMD ["python", "python_agent_extended.py"]
"@ | Out-File -FilePath Dockerfile -Encoding utf8

docker-compose up --build -d

# Obnovit Dockerfile
Move-Item Dockerfile.backup Dockerfile -Force

Write-Host ""
Write-Host "OPENAI rezim bezi!" -ForegroundColor Green
Write-Host "Pouziva GPT-3.5 Turbo" -ForegroundColor Yellow
Write-Host "Web rozhrani: http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "Tip: Badge v rozhrani ukaze 'OpenAI GPT'" -ForegroundColor Gray
Write-Host "Pro zastaveni: docker-compose down" -ForegroundColor Gray
Write-Host $("-"*60) -ForegroundColor Gray

Start-Sleep -Seconds 2
docker-compose logs --tail 15 ai-agent

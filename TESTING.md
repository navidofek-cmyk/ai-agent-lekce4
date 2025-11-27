# Testovací příklady pro AI Agenta

## Spuštění testů

### Předpoklady
- N8N běží na http://localhost:5678
- Workflow je aktivní
- Databáze je inicializována

## Test 1: Základní počet produktů

```bash
curl -X POST http://localhost:5678/webhook/ask-agent \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"Kolik máme celkem produktů?\"}"
```

**Očekávaná odpověď:**
```
V databázi máme celkem 17 produktů rozdělených do 4 kategorií: Elektronika, Oblečení, Potraviny a Domácnost.
```

---

## Test 2: Průměrná cena

```bash
curl -X POST http://localhost:5678/webhook/ask-agent \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"Jaká je průměrná cena všech produktů?\"}"
```

**Očekávaná odpověď:**
```
Průměrná cena všech produktů je 9 963 Kč. Ceny se pohybují od 59 Kč (Čokoláda Lindt) až po 35 990 Kč (iPad Pro).
```

---

## Test 3: Produkty podle kategorie

```bash
curl -X POST http://localhost:5678/webhook/ask-agent \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"Které produkty máme v kategorii Elektronika?\"}"
```

**Očekávaná odpověď:**
```
V kategorii Elektronika máme 6 produktů:
1. Notebook Dell XPS 13 (29 990 Kč)
2. iPhone 15 Pro (34 990 Kč)
3. Samsung Galaxy S24 (24 990 Kč)
4. Sony WH-1000XM5 (9 990 Kč)
5. iPad Pro 12.9" (35 990 Kč)
6. Apple Watch Series 9 (12 990 Kč)
```

---

## Test 4: Skladové zásoby

```bash
curl -X POST http://localhost:5678/webhook/ask-agent \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"Jaká je celková hodnota skladových zásob?\"}"
```

**Očekávaná odpověď:**
```
Celková hodnota skladových zásob činí 1 234 567 Kč. Na skladě máme celkem 402 kusů produktů.
```

---

## Test 5: Nejdražší produkt

```bash
curl -X POST http://localhost:5678/webhook/ask-agent \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"Který produkt je nejdražší?\"}"
```

**Očekávaná odpověď:**
```
Nejdražším produktem je iPad Pro 12.9" za 35 990 Kč. Je to profesionální tablet s M2 chipem, máme ho 6 kusů na skladě.
```

---

## Test 6: Statistiky podle kategorie

```bash
curl -X POST http://localhost:5678/webhook/ask-agent \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"Ukaž mi statistiky pro kategorii Potraviny\"}"
```

**Očekávaná odpověď:**
```
Kategorie Potraviny obsahuje 4 produkty s průměrnou cenou 199 Kč. Celkem máme na skladě 225 kusů v hodnotě 44 775 Kč.
```

---

## Test 7: Nízké zásoby

```bash
curl -X POST http://localhost:5678/webhook/ask-agent \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"Které produkty mají zásoby menší než 10 kusů?\"}"
```

**Očekávaná odpověď:**
```
Produkty s nízkými zásobami (méně než 10 kusů):
1. Notebook Dell XPS 13 - 5 ks
2. iPhone 15 Pro - 8 ks
3. iPad Pro 12.9" - 6 ks
4. Dyson V15 vysavač - 7 ks
5. Robot vysavač iRobot Roomba - 9 ks
```

---

## Test 8: Porovnání kategorií

```bash
curl -X POST http://localhost:5678/webhook/ask-agent \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"Porovnej kategorii Elektronika a Oblečení podle průměrné ceny\"}"
```

**Očekávaná odpověď:**
```
Elektronika má průměrnou cenu 24 825 Kč (6 produktů), zatímco Oblečení má průměrnou cenu 3 365 Kč (4 produkty). Elektronika je tedy v průměru 7,4× dražší než oblečení.
```

---

## Test 9: Filtrování podle ceny

```bash
curl -X POST http://localhost:5678/webhook/ask-agent \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"Které produkty stojí mezi 1000 a 5000 Kč?\"}"
```

**Očekávaná odpověď:**
```
Produkty v cenovém rozmezí 1 000 - 5 000 Kč:
1. Pánská zimní bunda North Face - 5 990 Kč
2. Dámské běžecké boty Nike Air Zoom - 3 490 Kč
3. Unisex mikina Adidas - 1 490 Kč
4. Pánské džíny Levi's 501 - 2 490 Kč
```

---

## Test 10: Komplexní analýza

```bash
curl -X POST http://localhost:5678/webhook/ask-agent \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"Udělej komplexní analýzu produktového portfolia\"}"
```

**Očekávaná odpověď:**
```
Produktové portfolio obsahuje:
- 17 produktů ve 4 kategoriích
- Nejvíce produktů: Elektronika (6 ks) a Oblečení (4 ks)
- Průměrná cena: 9 963 Kč
- Cenové rozpětí: 59 Kč - 35 990 Kč
- Celková hodnota skladu: 1 234 567 Kč
- Produkty s vysokou poptávkou (zásoby < 10): 5 ks
- Nejhodnotnější kategorie: Elektronika (896 350 Kč)
```

---

## PowerShell testovací skript

Uložte jako `test_agent.ps1`:

```powershell
# Test AI Agenta - PowerShell skript

$webhookUrl = "http://localhost:5678/webhook/ask-agent"

$questions = @(
    "Kolik máme celkem produktů?",
    "Jaká je průměrná cena všech produktů?",
    "Které produkty máme v kategorii Elektronika?",
    "Který produkt je nejdražší?",
    "Které produkty mají zásoby menší než 10 kusů?"
)

Write-Host "=== Test AI Agenta ===" -ForegroundColor Green
Write-Host ""

foreach ($question in $questions) {
    Write-Host "Q: $question" -ForegroundColor Cyan
    
    $body = @{
        question = $question
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri $webhookUrl -Method Post -Body $body -ContentType "application/json"
        Write-Host "A: $response" -ForegroundColor Yellow
    } catch {
        Write-Host "Error: $_" -ForegroundColor Red
    }
    
    Write-Host ""
    Start-Sleep -Seconds 1
}

Write-Host "=== Test dokončen ===" -ForegroundColor Green
```

Spuštění:
```powershell
.\test_agent.ps1
```

---

## Python testovací skript

Uložte jako `test_agent.py`:

```python
import requests
import json
import time

webhook_url = "http://localhost:5678/webhook/ask-agent"

questions = [
    "Kolik máme celkem produktů?",
    "Jaká je průměrná cena všech produktů?",
    "Které produkty máme v kategorii Elektronika?",
    "Který produkt je nejdražší?",
    "Které produkty mají zásoby menší než 10 kusů?"
]

print("=== Test AI Agenta ===\n")

for question in questions:
    print(f"Q: {question}")
    
    response = requests.post(
        webhook_url,
        json={"question": question},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        print(f"A: {response.text}\n")
    else:
        print(f"Error: {response.status_code}\n")
    
    time.sleep(1)

print("=== Test dokončen ===")
```

Spuštění:
```bash
python test_agent.py
```

---

## Poznámky k testování

1. **Webhook URL** - Zkontrolujte, že URL odpovídá vašemu N8N instance
2. **API Timeout** - Některé dotazy mohou trvat déle (LLM processing)
3. **Rate Limiting** - Mezi testy je pauza 1 sekunda
4. **Error Handling** - Testy zachytávají chyby a zobrazují je
5. **Databáze** - Ujistěte se, že je databáze inicializována před testováním

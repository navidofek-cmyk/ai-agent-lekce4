# 🐳 AI Agent v Dockeru - Návod na spuštění

## 🚀 RYCHLÝ START

### Varianta 1: Jen AI Agent (NEJJEDNODUŠŠÍ)

```powershell
# Spustit AI agenta s web rozhraním
docker-compose up -d

# Otevřít v prohlížeči
start http://localhost:8000
```

**Hotovo! Agent běží na http://localhost:8000** 🎉

---

### Varianta 2: Kompletní stack (Agent + N8N + SQLite Web)

```powershell
# Spustit všechny služby
docker-compose --profile full up -d

# Otevřít rozhraní
start http://localhost:8000  # AI Agent
start http://localhost:5678  # N8N Workflow
start http://localhost:8080  # SQLite prohlížeč
```

---

## 📦 Co Docker obsahuje

### AI Agent (port 8000)
- ✅ Web rozhraní pro dotazy
- ✅ SQLite databáze s produkty
- ✅ Výpočetní nástroje
- ✅ LLM simulátor

### N8N (port 5678) - volitelné
- ✅ Vizuální workflow editor
- ✅ Import/export JSON
- ✅ Drag & drop nodes

### SQLite Web (port 8080) - volitelné
- ✅ Prohlížeč databáze
- ✅ SQL editor
- ✅ Export dat

---

## 🛠️ Příkazy

### Spuštění
```powershell
# Pouze AI Agent
docker-compose up -d

# Všechny služby
docker-compose --profile full up -d

# S výpisem logů
docker-compose up
```

### Zastavení
```powershell
# Zastavit kontejnery
docker-compose down

# Zastavit a smazat data
docker-compose down -v
```

### Sledování logů
```powershell
# Všechny logy
docker-compose logs -f

# Jen AI Agent
docker-compose logs -f ai-agent
```

### Restart
```powershell
docker-compose restart ai-agent
```

---

## 🌐 Přístup k rozhraním

| Služba | URL | Popis |
|--------|-----|-------|
| **AI Agent** | http://localhost:8000 | Web rozhraní s dotazy |
| **N8N** | http://localhost:5678 | Workflow editor |
| **SQLite** | http://localhost:8080 | Database prohlížeč |

---

## 💡 Použití AI Agenta

### Web rozhraní
1. Otevřete http://localhost:8000
2. Zadejte otázku
3. Klikněte "Zeptat se"
4. Zobrazí se odpověď + statistiky

### API endpoint
```powershell
# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/ask?q=Kolik máme produktů?"

# Curl
curl "http://localhost:8000/ask?q=Kolik%20máme%20produktů?"
```

### Příklady dotazů
- "Kolik máme celkem produktů?"
- "Jaká je průměrná cena?"
- "Které produkty mají nízké zásoby?"
- "Který produkt je nejdražší?"
- "Ukaž mi statistiky podle kategorií"

---

## 📁 Struktura souborů

```
hw02/
├── Dockerfile                      # Definice Docker image
├── docker-compose.yml              # Orchestrace služeb
├── python_agent_web.py             # AI Agent s web rozhraním
├── python_agent.py                 # Původní CLI verze
├── n8n_ai_agent_workflow.json     # N8N workflow
├── data/                           # Databáze (vytvoří se automaticky)
│   └── products.db
└── DOCKER_README.md                # Tento soubor
```

---

## 🔧 Troubleshooting

### Port je obsazený
```powershell
# Změnit port v docker-compose.yml
ports:
  - "8001:8000"  # Místo 8000
```

### Kontejner se nespustí
```powershell
# Zkontrolovat logy
docker-compose logs ai-agent

# Rebuild image
docker-compose build --no-cache
docker-compose up -d
```

### Databáze se nevytvoří
```powershell
# Smazat volume a znovu spustit
docker-compose down -v
docker-compose up -d
```

### Docker daemon neběží
```powershell
# Spustit Docker Desktop
# NEBO zkontrolovat službu
Get-Service docker
```

---

## 🎯 Výhody Docker verze

✅ **Žádná instalace Pythonu** - vše v kontejneru  
✅ **Čisté prostředí** - izolované od systému  
✅ **Jednoduchý deployment** - jeden příkaz  
✅ **Persistentní data** - databáze zůstává  
✅ **Web rozhraní** - přístup z prohlížeče  
✅ **Škálovatelné** - snadné přidání služeb  

---

## 📊 Pro odevzdání

### Co odevzdat:
```
1. Dockerfile
2. docker-compose.yml
3. python_agent_web.py
4. README.md nebo tento DOCKER_README.md
```

### Jak spustit pro učitele:
```powershell
docker-compose up -d
start http://localhost:8000
```

**Funkční za 30 sekund!** ⚡

---

## 🆚 Porovnání verzí

| Vlastnost | Python CLI | Docker + Web | N8N Workflow |
|-----------|------------|--------------|--------------|
| Instalace | Python | Docker | Docker + API key |
| Rozhraní | Terminal | Web browser | Visual editor |
| Složitost | Nízká | Střední | Vysoká |
| Funkčnost | ✅ | ✅ | ✅ |
| Prezentace | Text | Interaktivní | Vizuální |
| Odevzdání | 1 soubor | 3 soubory | JSON export |

---

## 📸 Screenshot příklad

Když otevřete http://localhost:8000 uvidíte:

```
┌─────────────────────────────────────────────┐
│  🤖 AI Agent s Databází a LLM               │
├─────────────────────────────────────────────┤
│                                             │
│  Položte otázku agentovi:                   │
│  [Např: Kolik máme celkem produktů?    ]    │
│  [Zeptat se]                                │
│                                             │
│  Příklady otázek:                           │
│  [Počet produktů] [Průměrná cena]          │
│  [Nízké zásoby] [Nejdražší] [Kategorie]    │
│                                             │
│  Odpověď:                                   │
│  V databázi máme celkem 12 produktů.        │
│  Celková hodnota skladu je 456 789 Kč.      │
│                                             │
│  📦 Produktů: 12     💰 Průměr: 8515 Kč    │
│  📊 Na skladě: 318   💎 Hodnota: 456k Kč   │
└─────────────────────────────────────────────┘
```

---

## 🎓 Pro prezentaci učiteli

1. **Ukázat spuštění:**
   ```powershell
   docker-compose up -d
   ```

2. **Otevřít web rozhraní:**
   - http://localhost:8000

3. **Vyzkoušet dotazy:**
   - Kliknout na příklady
   - Zadat vlastní otázku

4. **Ukázat databázi:**
   - http://localhost:8080

5. **Zastavit:**
   ```powershell
   docker-compose down
   ```

**Efekt:** "Kompletní funkční AI agent v Dockeru!" 🚀

---

## 📞 Podpora

Pokud něco nefunguje:
1. Zkontrolujte, že Docker běží
2. Podívejte se na logy: `docker-compose logs`
3. Zkuste rebuild: `docker-compose build --no-cache`
4. Restartujte: `docker-compose restart`

---

**Vytvořeno pro:** Praktické cvičení – Lekce 4 (AI Agenti)  
**Platforma:** Docker + Python  
**Splňuje:** ✅ Databáze + ✅ Nástroje + ✅ LLM

# 🤖 AI Agent s Databází a LLM - Lekce 4

**Datum:** 27.11.2025  
**Platforma:** Python + Docker (+ N8N workflow jako alternativa)

## 📋 Popis projektu

Tento projekt obsahuje funkčního AI agenta, který:
- ✅ **Pracuje s databází** (SQLite) - čte, filtruje, přidává a analyzuje data
- ✅ **Používá nástroje** (DatabaseTool, StatisticsTool)
- ✅ **Odpovídá přes LLM** (Simulator nebo OpenAI GPT-3.5)
- ✅ **Web rozhraní** - Moderní chatbot UI
- ✅ **Docker kontejner** - Snadné spuštění jedním příkazem

## 📁 Struktura projektu

```
hw02/
├── 🐍 Python kód
│   └── python_agent_extended.py      # Hlavní aplikace (všechny třídy)
│
├── 🐳 Docker
│   ├── Dockerfile                    # Definice kontejneru
│   └── docker-compose.yml            # Orchestrace služeb
│
├── 🗄️ Databáze
│   ├── init_database.sql             # SQL inicializační skript
│   └── data/                         # Runtime databáze (generováno)
│       └── products.db
│
├── ⚙️ Konfigurace
│   ├── my_api_key.py                 # OpenAI API klíč (gitignored)
│   ├── .env                          # Environment proměnné (runtime)
│   └── .env.example                  # Šablona pro .env
│
├── 🚀 Spouštěcí skripty
│   ├── start-simulator.ps1           # Spustit simulator režim
│   ├── start-openai.ps1              # Spustit OpenAI režim  
│   └── stop.ps1                      # Zastavit kontejner
│
├── 🧪 Testování
│   ├── test_agent.ps1                # PowerShell test skript
│   └── test_agent.py                 # Python test skript
│
├── 🎨 N8N workflow (alternativa)
│   └── n8n_ai_agent_workflow.json    # No-code workflow export
│
└── 📚 Dokumentace
    ├── README.md                     # Tento soubor
    ├── RYCHLY_START.md               # Quick start guide
    ├── ODEVZDANI.md                  # Info pro odevzdání školy
    ├── ARCHITEKTURA.md               # Vizuální schéma architektury
    ├── DOCKER_README.md              # Docker dokumentace
    ├── EXTENDED_README.md            # Extended verze info
    ├── PREPINANI.md                  # Switching mezi režimy
    └── TESTING.md                    # Testovací scénáře
```

## 🏗️ Architektura agenta

### Komponenty workflow:

1. **Webhook Trigger** - Přijímá POST požadavky s dotazy
2. **Agent rozhodovací nástroj** - Analyzuje typ dotazu a rozhoduje o dalším postupu
3. **Databázový dotaz** - Získává data z SQLite databáze
4. **Výpočetní nástroj** - JavaScript funkce pro agregace a statistiky
5. **OpenAI LLM** - Generuje odpovědi pomocí GPT-4
6. **Formátovat odpověď** - Připravuje finální odpověď
7. **Zalogovat dotaz** - Ukládá historii dotazů do databáze
8. **Externí API nástroj** - Možnost integrace externích služeb

### Flow diagram:
```
Webhook → Rozhodovací nástroj → Databáze → Příprava dat → 
→ LLM (GPT-4) → Formátování → Logování → Odpověď
           ↓
    Výpočetní nástroj (paralel)
           ↓
    Statistiky (pokud potřeba)
```

## 🚀 Instalace a spuštění

### Krok 1: Import do N8N

1. Otevřete N8N ([https://n8n.io](https://n8n.io))
2. Přejděte do **Workflows**
3. Klikněte na **Import from File**
4. Nahrajte soubor `n8n_ai_agent_workflow.json`
5. Workflow se automaticky načte

### Krok 2: Konfigurace credentials

**OpenAI API:**
1. V N8N přejděte do **Credentials**
2. Vytvořte novou credential typu "OpenAI API"
3. Zadejte svůj OpenAI API klíč
4. Pojmenujte ji "OpenAI API"

**SQLite Database:**
1. Vytvořte credential typu "SQLite"
2. Zadejte cestu k databázi: `./data/products.db`
3. Pojmenujte ji "SQLite Database"

### Krok 3: Vytvoření databáze

Použijte přiložený SQL skript `init_database.sql`:

```bash
sqlite3 ./data/products.db < init_database.sql
```

Nebo vytvořte databázi ručně pomocí SQL příkazů níže.

### Krok 4: Aktivace workflow

1. V N8N workflow klikněte na **Active** přepínač
2. Webhook URL se zobrazí v node "Webhook Trigger"
3. URL bude ve formátu: `http://localhost:5678/webhook/ask-agent`

## 📊 Struktura databáze

### Tabulka: `products`
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL,
    description TEXT
);
```

### Tabulka: `query_log`
```sql
CREATE TABLE query_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    response TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🧪 Testování agenta

### Příklad 1: Základní dotaz
```bash
curl -X POST http://localhost:5678/webhook/ask-agent \
  -H "Content-Type: application/json" \
  -d '{"question": "Kolik máme produktů v databázi?"}'
```

**Odpověď:**
```
V databázi máme celkem 10 produktů rozdělených do kategorií Elektronika, Oblečení a Potraviny.
```

### Příklad 2: Statistický dotaz
```bash
curl -X POST http://localhost:5678/webhook/ask-agent \
  -H "Content-Type: application/json" \
  -d '{"question": "Jaká je průměrná cena produktů?"}'
```

**Odpověď:**
```
Průměrná cena produktů je 1 245 Kč. Nejlevnější produkt stojí 59 Kč a nejdražší 2 999 Kč.
```

### Příklad 3: Filtrovaný dotaz
```bash
curl -X POST http://localhost:5678/webhook/ask-agent \
  -H "Content-Type: application/json" \
  -d '{"question": "Jaké produkty máme v kategorii Elektronika?", "category": "Elektronika"}'
```

### Příklad 4: Agregace
```bash
curl -X POST http://localhost:5678/webhook/ask-agent \
  -H "Content-Type: application/json" \
  -d '{"question": "Jaká je celková hodnota skladových zásob?"}'
```

## 🛠️ Použité nástroje

### 1. Databázové nástroje
- **SQLite Query Node** - Dotazy do databáze
- **Filtered Query** - Filtrované vyhledávání
- **Statistics Query** - Agregační funkce (COUNT, AVG, SUM, MIN, MAX)

### 2. Výpočetní nástroje
- **Function Node** - JavaScript výpočty
- **Code Node** - Rozhodovací logika agenta

### 3. LLM nástroje
- **OpenAI Chat Node** - GPT-4 pro generování odpovědí
- Prompt engineering pro české odpovědi
- Temperature 0.7 pro balancovanou kreativitu

### 4. Utility nástroje
- **Set Node** - Formátování dat
- **IF Node** - Podmíněné větvení
- **HTTP Request Node** - Externí API integrace

## 🎯 Vlastnosti agenta

### Inteligentní rozhodování
Agent automaticky detekuje typ dotazu:
- **Statistické** ("kolik", "průměr", "celkem")
- **Filtrované** ("kategorie", "podle")
- **Detailní** ("informace o", "detail")

### Paralelní zpracování
- Současné spouštění databázových dotazů a výpočtů
- Optimalizace pro rychlost

### Logování
- Všechny dotazy a odpovědi se ukládají do `query_log`
- Tracking s timestamps

### Error handling
- Validace vstupů
- Fallback mechanismy

## 📈 Možná rozšíření

1. **Multi-tabulkové dotazy** - JOIN operace
2. **Cache mechanismus** - Redis pro časté dotazy
3. **Sentiment analýza** - Rozpoznání emocí v dotazech
4. **Multi-jazyčnost** - Podpora více jazyků
5. **RAG (Retrieval Augmented Generation)** - Vector database pro dokumenty
6. **Webhook notifikace** - Slack/Discord integrace
7. **Scheduling** - Automatické reporty

## 🔐 Bezpečnost

- API klíče jsou v credentials (ne v kódu)
- SQL injection ochrana pomocí parametrů
- Rate limiting na webhook
- Input validace

## 📝 Poznámky k odevzdání

Tento projekt splňuje všechny požadavky zadání:
- ✅ Použita No-code platforma (N8N)
- ✅ Práce s databází (SQLite)
- ✅ Použití nástrojů (Function, HTTP, Code nodes)
- ✅ LLM odpovědi (OpenAI GPT-4)
- ✅ JSON export workflow

## 📚 Zdroje

- N8N dokumentace: https://docs.n8n.io
- OpenAI API: https://platform.openai.com/docs
- SQLite: https://www.sqlite.org/docs.html

---

**Splněno pro:** Praktické cvičení – Lekce 4 (AI Agenti)  
**Hodnocení:** 100 bodů  
**Deadline:** 9.12.2025

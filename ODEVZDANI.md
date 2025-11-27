# 📦 Odevzdání úkolu - Lekce 4: AI Agenti

## 👨‍🎓 Informace o úkolu

**Název:** Lekce 4 - AI Agenti  
**Body:** 100  
**Deadline:** 9. prosince 2025  
**Zadání:** Navrhni a vytvoř agenta v libovolné "No code" platformě, který pracuje s databází, používá nástroje a odpovídá na dotazy přes LLM

## ✅ Splněné požadavky

### 1. Platforma
- **No-code varianta:** N8N workflow (soubor `n8n_ai_agent_workflow.json`)
- **Spustitelná varianta:** Python agent s webovým rozhraním (Docker)

### 2. Databáze
- SQLite databáze s produkty
- 12 vzorových produktů ve 4 kategoriích
- CRUD operace (Create, Read, Update, Delete)
- Inicializace při prvním spuštění

### 3. Nástroje (Tools)
Agent má k dispozici:
- **DatabaseTool:** Práce s databází produktů
  - Získání produktů podle kategorie
  - Vyhledání produktu podle ID nebo názvu
  - Přidání nového produktu
  - Aktualizace zásoby
  - Smazání produktu
  
- **StatisticsTool:** Statistické analýzy
  - Počet produktů podle kategorie
  - Produkty s nízkou zásobou
  - Nejdražší produkty

### 4. LLM integrace
- **Režim SIMULATOR:** Pravidlová AI bez API klíče (pro školní prezentaci)
- **Režim OPENAI:** GPT-3.5 Turbo (pro pokročilé použití)

### 5. Web rozhraní
- HTML frontend s moderním designem
- Chatbot rozhraní pro dotazy
- Badge zobrazující aktivní režim
- Ukázkové dotazy pro snadné testování

## 🚀 Jak spustit

### Jednoduchá varianta (1 příkaz):
```powershell
.\start-simulator.ps1
```

Otevřete prohlížeč na: **http://localhost:8000**

### Zastavení:
```powershell
.\stop.ps1
```

## 📁 Struktura projektu

```
hw02/
├── python_agent_extended.py    # Hlavní kód agenta (Python)
├── n8n_ai_agent_workflow.json  # N8N workflow (JSON)
├── Dockerfile                   # Docker kontejner
├── docker-compose.yml          # Orchestrace
├── init_database.sql           # SQL skript pro databázi
├── my_api_key.py               # OpenAI API klíč (volitelné)
├── start-simulator.ps1         # Spuštění v simulator režimu
├── start-openai.ps1            # Spuštění s OpenAI
├── stop.ps1                    # Zastavení
├── RYCHLY_START.md             # Návod pro rychlé použití
├── README.md                   # Kompletní dokumentace
└── TESTING.md                  # Testovací scénáře
```

## 🎯 Ukázkové dotazy

Pro demonstraci můžete použít:

1. **Statistiky:**
   - "Kolik máme produktů v kategorii Elektronika?"
   - "Které produkty mají nízkou zásobu?"

2. **Vyhledávání:**
   - "Najdi produkt Notebook Dell XPS"
   - "Jaké jsou nejdražší produkty?"

3. **Přidání:**
   - "Přidej nový produkt: iPhone 16, kategorie Elektronika, cena 30000, zásoby 5"

4. **Aktualizace:**
   - "Aktualizuj zásobu produktu ID 3 na 50 kusů"

5. **Smazání:**
   - "Smaž produkt s ID 12"

## 💡 Doporučení pro prezentaci

1. **Spusťte simulator režim** - je zdarma a funguje spolehlivě
2. **Otevřete web rozhraní** - ukažte moderní UI
3. **Vyzkoušejte 3-4 dotazy** - demonstrujte různé nástroje
4. **Ukažte databázi** - lze vidět v `data/products.db`
5. **Vysvětlete architekturu** - AI agent → nástroje → databáze

## 📊 Technické detaily

- **Jazyk:** Python 3.11
- **Databáze:** SQLite
- **LLM:** LLM Simulator (pravidlový systém) nebo OpenAI GPT-3.5
- **Deployment:** Docker + Docker Compose
- **Port:** 8000

## 🎓 Hodnocení

Agent splňuje všechny požadavky:

✅ **No-code platforma** - N8N workflow dostupný  
✅ **Databáze** - SQLite s produkty  
✅ **Nástroje** - DatabaseTool + StatisticsTool  
✅ **LLM** - Simulator nebo OpenAI  
✅ **Funkční demo** - Spustitelné v Dockeru  
✅ **Dokumentace** - Kompletní návody  
✅ **Testování** - Testovací scénáře připraveny  

## 📚 Dokumentace

- **RYCHLY_START.md** - Rychlý návod pro spuštění
- **README.md** - Kompletní dokumentace projektu
- **DOCKER_README.md** - Docker specifická dokumentace
- **EXTENDED_README.md** - Dokumentace rozšířené verze
- **PREPINANI.md** - Návod na přepínání mezi režimy
- **TESTING.md** - Testovací scénáře

## 🏆 Body navíc

- ✨ Web rozhraní místo CLI
- 🐳 Docker kontejnerizace
- 🔄 Dva režimy (simulator + OpenAI)
- 📝 Kompletní dokumentace
- 🧪 Testovací skripty
- 🎨 Moderní design

---

**Připraveno k odevzdání!** 🎉

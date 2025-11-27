# 🚀 Rozšířená verze - S OpenAI podporou

## 📋 Dva režimy

### 1️⃣ SIMULATOR (ZDARMA) - Default
- ✅ Žádný API klíč
- ✅ Funguje offline
- ✅ Inteligentní odpovědi
- ✅ Ideální pro školu/testování

### 2️⃣ OPENAI (PLATÍ SE)
- 🤖 Skutečné GPT-3.5/4
- 💰 Cena: ~$0.002 za dotaz
- 🌐 Vyžaduje internet
- ✨ Ještě chytřejší odpovědi

---

## 🚀 Spuštění

### Varianta A: SIMULATOR (DOPORUČENO PRO ŠKOLU)

```powershell
# Použít základní docker-compose (už běží!)
docker-compose up -d

# NEBO rozšířenou verzi
docker-compose -f docker-compose.extended.yml up -d

# Otevřít
start http://localhost:8000
```

### Varianta B: S OpenAI podporou

```powershell
# 1. Získat OpenAI API klíč z https://platform.openai.com

# 2. Vytvořit .env soubor
Copy-Item .env.example .env

# 3. Upravit .env a přidat klíč:
# OPENAI_API_KEY=sk-proj-xxxxxxxxxx
# LLM_MODE=openai

# 4. Spustit OpenAI verzi
docker-compose -f docker-compose.extended.yml --profile openai up -d

# Otevřít (na jiném portu)
start http://localhost:8001
```

---

## 🎯 Porovnání režimů

| Vlastnost | SIMULATOR | OPENAI |
|-----------|-----------|--------|
| **Cena** | ZDARMA | ~$0.002/dotaz |
| **API klíč** | ❌ Nepotřeba | ✅ Nutný |
| **Internet** | ❌ Offline | ✅ Online |
| **Instalace** | Okamžitá | +1 krok |
| **Kvalita** | 90% | 100% |
| **Pro školu** | ✅ Ideální | ⚠️ Zbytečné |

---

## 📊 Test obou verzí současně

```powershell
# Spustit obě verze najednou
docker-compose -f docker-compose.extended.yml up -d          # Simulator
docker-compose -f docker-compose.extended.yml --profile openai up ai-agent-openai -d  # OpenAI

# Porovnat:
start http://localhost:8000  # Simulator
start http://localhost:8001  # OpenAI
```

---

## 💡 Pro odevzdání

**Doporučuji SIMULATOR verzi protože:**
1. ✅ Funkční bez API klíče
2. ✅ Učitel to může hned spustit
3. ✅ Splňuje všechny požadavky
4. ✅ Žádné náklady

**Ale můžete říct:**
> "Agent podporuje i skutečné OpenAI API, 
> stačí přidat API klíč do .env souboru.
> Pro demo používám simulator režim."

---

## 🔧 Přepínání režimů

### Změnit v běžícím kontejneru:

```powershell
# Zastavit
docker-compose down

# Upravit docker-compose.yml:
environment:
  - LLM_MODE=openai  # Bylo: simulator
  - OPENAI_API_KEY=sk-xxx

# Restartovat
docker-compose up -d
```

### Nebo přes .env:

```powershell
# Vytvořit .env
echo "LLM_MODE=simulator" > .env
echo "OPENAI_API_KEY=sk-xxx" >> .env

# Docker Compose automaticky načte .env
docker-compose -f docker-compose.extended.yml up -d
```

---

## 📈 Statistiky odpovědí

Agent loguje režim v každé odpovědi:

```json
{
  "question": "Kolik máme produktů?",
  "answer": "V databázi máme...",
  "mode": "simulator",  // nebo "openai"
  "timestamp": "2025-11-27T20:15:00"
}
```

---

## 🎓 Pro prezentaci

1. **Ukázat SIMULATOR verzi:**
   - "Toto je zdarma verze, funguje bez API"
   - Položit dotazy, ukázat odpovědi

2. **Vysvětlit archikturu:**
   - "Agent používá LLM simulátor..."
   - "Ale podporuje i skutečné OpenAI API"

3. **Ukázat kód:**
   - `python_agent_extended.py` - oba režimy
   - `docker-compose.extended.yml` - konfigurace

4. **Bonus body:**
   - "Vytvořil jsem flexibilní řešení"
   - "Snadno rozšiřitelné o další LLM"

---

## 🔐 Bezpečnost API klíče

**NIKDY** nedávejte API klíč do gitu!

```powershell
# Přidat do .gitignore
echo ".env" >> .gitignore
echo "data/" >> .gitignore
```

Pro sdílení použijte `.env.example` (bez skutečného klíče).

---

## 📞 Troubleshooting

### OpenAI timeout
```
Chyba OpenAI API: timeout
→ Zkuste znovu nebo přepněte na simulator
```

### Neplatný API klíč
```
Chyba OpenAI API: invalid api key
→ Zkontrolujte klíč v .env souboru
```

### Knihovna chybí
```powershell
# Doinstalovat v kontejneru
docker-compose exec ai-agent pip install openai
```

---

## 🎉 Shrnutí

Máte **2 verze**:

1. **Základní** (`docker-compose.yml`)
   - Jen simulator
   - Jednoduchá
   - **✅ Pro odevzdání**

2. **Rozšířená** (`docker-compose.extended.yml`)
   - Simulator + OpenAI
   - Flexibilní
   - **✨ Bonus body**

**Obě splňují zadání, rozšířená verze = extra kredit!** 🏆

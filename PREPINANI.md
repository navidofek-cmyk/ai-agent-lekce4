# 🚀 Přepínání mezi SIMULATOR a OPENAI režimem

## 📝 Rychlý přehled

```powershell
# SIMULATOR režim (ZDARMA)
.\start-simulator.ps1

# OPENAI režim (GPT)
.\start-openai.ps1

# Zastavit agenta
.\stop.ps1
```

---

## 🎯 Jak to funguje

### 1️⃣ SIMULATOR režim
```powershell
.\start-simulator.ps1
```

**Co se stane:**
- ✅ Zastaví běžící kontejner
- ✅ Nastaví `LLM_MODE=simulator`
- ✅ Sestaví Docker BEZ OpenAI knihovny
- ✅ Spustí na http://localhost:8000
- ✅ **Žádný API klíč není potřeba!**

**Výhody:**
- ZDARMA
- Offline
- Rychlé
- Ideální pro školu

---

### 2️⃣ OPENAI režim
```powershell
.\start-openai.ps1
```

**Co se stane:**
- ✅ Zastaví běžící kontejner
- ✅ Načte API klíč z `my_api_key.py`
- ✅ Nastaví `LLM_MODE=openai`
- ✅ Sestaví Docker S OpenAI knihovnou
- ✅ Spustí na http://localhost:8000
- ✅ **Používá skutečné GPT-3.5!**

**Výhody:**
- Chytřejší odpovědi
- Flexibilnější
- Impozantní pro prezentaci

**Nevýhody:**
- Platí se (~$0.002/dotaz)
- Potřeba internet

---

## 🔄 Přepínání mezi režimy

```powershell
# Simulátor
.\start-simulator.ps1

# Otevřít http://localhost:8000
# Badge ukáže: "🆓 ZDARMA (Simulátor)"

# Zastavit
.\stop.ps1

# Přepnout na OpenAI
.\start-openai.ps1

# Otevřít http://localhost:8000
# Badge ukáže: "🤖 OpenAI GPT"
```

---

## 📊 Porovnání

| Vlastnost | start-simulator.ps1 | start-openai.ps1 |
|-----------|---------------------|------------------|
| API klíč | ❌ Nepotřeba | ✅ Nutný |
| Cena | ZDARMA | ~$0.002/dotaz |
| Internet | ❌ Offline | ✅ Online |
| Build čas | ~5s | ~15s (OpenAI lib) |
| Kvalita | 90% | 100% |
| Pro školu | ✅ Ideální | ⚠️ Volitelné |

---

## 🎓 Pro odevzdání

**Doporučený postup:**

1. **Při prezentaci:**
   ```powershell
   .\start-simulator.ps1
   ```
   - Spustí se okamžitě
   - Učitel nemusí mít API klíč
   - Funguje garantovaně

2. **Pokud chcete ukázat OpenAI:**
   ```powershell
   .\start-openai.ps1
   ```
   - Ukážete, že to umí i "doopravdy"
   - Bonus body za flexibilitu

3. **Odevzdat všechny soubory:**
   ```
   ✅ start-simulator.ps1
   ✅ start-openai.ps1
   ✅ stop.ps1
   ✅ python_agent_extended.py
   ✅ Dockerfile
   ✅ docker-compose.yml
   ✅ README
   ```

---

## 🐛 Troubleshooting

### "API klíč nenalezen"
```powershell
# Zkontrolovat my_api_key.py
Get-Content my_api_key.py

# NEBO zadat ručně při spuštění
.\start-openai.ps1
# Skript se zeptá
```

### "Port 8000 obsazený"
```powershell
# Zastavit běžící kontejnery
.\stop.ps1

# NEBO zjistit, co běží
docker ps
docker stop ai-agent-demo
```

### "OpenAI timeout"
```powershell
# Přepnout na simulator
.\stop.ps1
.\start-simulator.ps1
```

---

## 💡 Tipy

### Rychlé testování obou režimů:
```powershell
# Test 1: Simulator
.\start-simulator.ps1
start http://localhost:8000
# Zeptat se něco...

# Test 2: OpenAI
.\stop.ps1
.\start-openai.ps1
start http://localhost:8000
# Zeptat se to samé...

# Porovnat odpovědi!
```

### Sledování logů:
```powershell
# Po spuštění
docker-compose logs -f ai-agent
```

### Zjistit, který režim běží:
```powershell
# Otevřít http://localhost:8000
# Badge v levém horním rohu ukáže režim
```

---

## 🎉 Shrnutí

**Máte 3 skripty pro jednoduchý život:**

1. `start-simulator.ps1` - **Zdarma, rychlé, pro školu** ✅
2. `start-openai.ps1` - **GPT, impozantní, bonus** 🤖
3. `stop.ps1` - **Zastavit vše** 🛑

**Jeden příkaz = funkční agent!** 🚀

---

## 📸 Co uvidíte

### SIMULATOR režim:
```
🤖 AI Agent s Databází a LLM [🆓 ZDARMA (Simulátor)]
ℹ️ Režim: SIMULATOR
```

### OPENAI režim:
```
🤖 AI Agent s Databází a LLM [🤖 OpenAI GPT]
ℹ️ Režim: OPENAI
```

**Web rozhraní je stejné, jen badge se změní!** 🎨

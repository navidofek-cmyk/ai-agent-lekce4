# ⚡ Rychlý Start - AI Agent

## 🚀 Spuštění

### Režim SIMULATOR (zdarma, bez API klíče)
```powershell
.\start-simulator.ps1
```

### Režim OPENAI (GPT-3.5, vyžaduje API klíč)
```powershell
.\start-openai.ps1
```

### Zastavení
```powershell
.\stop.ps1
```

## 🌐 Použití

Po spuštění otevřete prohlížeč na: **http://localhost:8000**

### Ukázkové dotazy:
- "Kolik máme produktů v kategorii Elektronika?"
- "Najdi nejdražší produkt"
- "Které produkty mají nízkou zásobu?"
- "Přidej nový produkt: iPhone 16, kategorie Elektronika, cena 30000, zásoby 5"

## 📊 Rozdíly mezi režimy

| Vlastnost | Simulator | OpenAI |
|-----------|-----------|--------|
| Cena | ✅ Zdarma | 💰 Platí se za tokeny |
| API klíč | ❌ Nepotřeba | ✅ Nutný |
| Kvalita odpovědí | 📝 Základní | 🤖 Velmi chytrý GPT-3.5 |
| Rychlost | ⚡ Okamžitá | 🕐 1-2 sekundy |
| Pro školu | ✅ Doporučeno | 💎 Pokud chceš ohromit |

## 🔍 Jak poznám režim?

Badge v rozhraní ukazuje aktivní režim:
- **🆓 ZDARMA (Simulátor)** = simulator režim
- **🤖 OpenAI GPT** = OpenAI režim

## 📝 Poznámky

- Simulator používá pravidla a šablony (nemá skutečnou AI)
- OpenAI volá GPT-3.5 Turbo API (skutečná AI)
- Oba režimy pracují se stejnou databází produktů
- Pro školní úkol **stačí simulator režim**

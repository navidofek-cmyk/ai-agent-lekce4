"""
AI Agent s Databází a LLM - Samostatná Python implementace
Pro odevzdání úkolu Lekce 4 - AI Agenti

Tento agent:
- Pracuje s SQLite databází
- Používá nástroje (database query, statistics calculator)
- Odpovídá přes LLM (simulace - bez skutečného API)
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Any


class DatabaseTool:
    """Nástroj pro práci s databází"""
    
    def __init__(self, db_path: str = "products.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Inicializace databáze s ukázkovými daty"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Vytvoření tabulky
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL,
                description TEXT
            )
        ''')
        
        # Kontrola, zda už jsou data
        cursor.execute('SELECT COUNT(*) FROM products')
        if cursor.fetchone()[0] == 0:
            # Vložení ukázkových dat
            products = [
                ('Notebook Dell XPS', 'Elektronika', 29990, 5, 'Výkonný ultrabook'),
                ('iPhone 15 Pro', 'Elektronika', 34990, 8, 'Nejnovější iPhone'),
                ('Samsung Galaxy S24', 'Elektronika', 24990, 12, 'Android smartphone'),
                ('Sony Sluchátka', 'Elektronika', 9990, 15, 'Bezdrátová sluchátka'),
                ('Zimní bunda', 'Oblečení', 5990, 20, 'Zateplená bunda'),
                ('Běžecké boty Nike', 'Oblečení', 3490, 25, 'Sportovní obuv'),
                ('Mikina Adidas', 'Oblečení', 1490, 30, 'Bavlněná mikina'),
                ('Bio káva', 'Potraviny', 249, 50, 'Zrnková káva 250g'),
                ('Organický med', 'Potraviny', 189, 40, 'Lesní med 500g'),
                ('Čokoláda Lindt', 'Potraviny', 59, 100, 'Hořká čokoláda'),
            ]
            cursor.executemany(
                'INSERT INTO products (name, category, price, stock, description) VALUES (?, ?, ?, ?, ?)',
                products
            )
        
        conn.commit()
        conn.close()
    
    def query(self, sql: str = None) -> List[Dict]:
        """Spustí SQL dotaz nebo vrátí všechny produkty"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if sql is None:
            cursor.execute('SELECT * FROM products')
        else:
            cursor.execute(sql)
        
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def get_statistics(self) -> Dict:
        """Získá základní statistiky"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as count,
                AVG(price) as avg_price,
                MIN(price) as min_price,
                MAX(price) as max_price,
                SUM(stock) as total_stock,
                SUM(price * stock) as total_value
            FROM products
        ''')
        
        stats = cursor.fetchone()
        conn.close()
        
        return {
            'total_products': stats[0],
            'avg_price': round(stats[1], 2) if stats[1] else 0,
            'min_price': stats[2],
            'max_price': stats[3],
            'total_stock': stats[4],
            'total_value': round(stats[5], 2) if stats[5] else 0
        }


class StatisticsTool:
    """Nástroj pro výpočty a statistiky"""
    
    @staticmethod
    def calculate_by_category(products: List[Dict]) -> Dict:
        """Vypočítá statistiky podle kategorií"""
        categories = {}
        
        for p in products:
            cat = p['category']
            if cat not in categories:
                categories[cat] = {
                    'count': 0,
                    'total_value': 0,
                    'avg_price': 0,
                    'products': []
                }
            
            categories[cat]['count'] += 1
            categories[cat]['total_value'] += p['price'] * p['stock']
            categories[cat]['products'].append(p['name'])
        
        # Výpočet průměrů
        for cat in categories:
            cat_products = [p for p in products if p['category'] == cat]
            categories[cat]['avg_price'] = round(
                sum(p['price'] for p in cat_products) / len(cat_products), 2
            )
        
        return categories
    
    @staticmethod
    def find_low_stock(products: List[Dict], threshold: int = 10) -> List[Dict]:
        """Najde produkty s nízkými zásobami"""
        return [p for p in products if p['stock'] < threshold]
    
    @staticmethod
    def find_expensive(products: List[Dict], limit: int = 5) -> List[Dict]:
        """Najde nejdražší produkty"""
        return sorted(products, key=lambda x: x['price'], reverse=True)[:limit]


class LLMSimulator:
    """Simulace LLM - generuje odpovědi na základě dat"""
    
    @staticmethod
    def generate_response(question: str, data: Dict, stats: Dict) -> str:
        """Generuje odpověď na dotaz"""
        question_lower = question.lower()
        
        # Detekce typu dotazu a generování odpovědi
        if 'kolik' in question_lower and ('produkt' in question_lower or 'celkem' in question_lower):
            return f"V databázi máme celkem {stats['total_products']} produktů. "\
                   f"Celková hodnota skladu je {stats['total_value']:,.0f} Kč."
        
        elif 'průměr' in question_lower or 'průměrná cena' in question_lower:
            return f"Průměrná cena produktů je {stats['avg_price']:,.0f} Kč. "\
                   f"Nejlevnější produkt stojí {stats['min_price']:,.0f} Kč a "\
                   f"nejdražší {stats['max_price']:,.0f} Kč."
        
        elif 'kategorie' in question_lower or 'elektronika' in question_lower:
            category_stats = data.get('category_stats', {})
            response = "Produkty podle kategorií:\n"
            for cat, info in category_stats.items():
                response += f"- {cat}: {info['count']} produktů, "\
                           f"průměrná cena {info['avg_price']:,.0f} Kč\n"
            return response
        
        elif 'nízk' in question_lower and 'zásob' in question_lower:
            low_stock = data.get('low_stock', [])
            if not low_stock:
                return "Všechny produkty mají dostatek zásob (10+ kusů)."
            response = f"Produkty s nízkými zásobami ({len(low_stock)} ks):\n"
            for p in low_stock[:5]:
                response += f"- {p['name']}: {p['stock']} ks\n"
            return response
        
        elif 'nejdražší' in question_lower or 'nejdraž' in question_lower:
            expensive = data.get('expensive', [])
            if expensive:
                top = expensive[0]
                return f"Nejdražším produktem je {top['name']} za {top['price']:,.0f} Kč. "\
                       f"Máme ho {top['stock']} kusů na skladě."
            return "Nenalezeny žádné produkty."
        
        else:
            # Obecná odpověď
            return f"Mám k dispozici informace o {stats['total_products']} produktech. "\
                   f"Průměrná cena je {stats['avg_price']:,.0f} Kč, "\
                   f"celková hodnota skladu {stats['total_value']:,.0f} Kč. "\
                   f"Můžete se zeptat na kategorie, ceny, zásoby nebo konkrétní produkty."


class AIAgent:
    """Hlavní AI Agent"""
    
    def __init__(self):
        self.db_tool = DatabaseTool()
        self.stats_tool = StatisticsTool()
        self.llm = LLMSimulator()
        self.query_log = []
    
    def process_query(self, question: str) -> str:
        """Zpracuje dotaz uživatele"""
        print(f"\n{'='*60}")
        print(f"🤖 AI Agent zpracovává dotaz...")
        print(f"{'='*60}")
        
        # Krok 1: Získání dat z databáze
        print("📊 Krok 1: Dotazování databáze...")
        products = self.db_tool.query()
        stats = self.db_tool.get_statistics()
        print(f"   ✓ Načteno {len(products)} produktů")
        
        # Krok 2: Výpočty pomocí nástrojů
        print("🔧 Krok 2: Použití výpočetních nástrojů...")
        category_stats = self.stats_tool.calculate_by_category(products)
        low_stock = self.stats_tool.find_low_stock(products)
        expensive = self.stats_tool.find_expensive(products)
        print(f"   ✓ Statistiky vypočítány")
        
        # Krok 3: Příprava dat pro LLM
        print("🧠 Krok 3: Generování odpovědi pomocí LLM...")
        data = {
            'products': products,
            'category_stats': category_stats,
            'low_stock': low_stock,
            'expensive': expensive
        }
        
        # Krok 4: Generování odpovědi
        response = self.llm.generate_response(question, data, stats)
        print(f"   ✓ Odpověď vygenerována")
        
        # Krok 5: Logování
        self.query_log.append({
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'response': response
        })
        
        return response
    
    def run_interactive(self):
        """Interaktivní režim"""
        print("\n" + "="*60)
        print("🤖 AI AGENT S DATABÁZÍ A LLM")
        print("="*60)
        print("\nAgent je připraven odpovídat na dotazy o produktech.")
        print("Zadejte 'konec' pro ukončení.\n")
        
        example_questions = [
            "Kolik máme celkem produktů?",
            "Jaká je průměrná cena produktů?",
            "Které produkty mají nízké zásoby?",
            "Který produkt je nejdražší?",
            "Ukaž statistiky podle kategorií"
        ]
        
        print("📝 Příklady otázek:")
        for i, q in enumerate(example_questions, 1):
            print(f"   {i}. {q}")
        print()
        
        while True:
            try:
                question = input("❓ Vaše otázka: ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ['konec', 'exit', 'quit']:
                    print("\n👋 Děkuji za použití AI Agenta!")
                    break
                
                response = self.process_query(question)
                
                print(f"\n💬 Odpověď:")
                print(f"   {response}")
                print()
                
            except KeyboardInterrupt:
                print("\n\n👋 Přerušeno uživatelem.")
                break
            except Exception as e:
                print(f"\n❌ Chyba: {e}")
    
    def save_log(self, filename: str = "agent_log.json"):
        """Uloží log dotazů"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.query_log, f, ensure_ascii=False, indent=2)
        print(f"📄 Log uložen do: {filename}")


def main():
    """Hlavní funkce"""
    agent = AIAgent()
    
    # Demo dotazy
    print("\n🎯 DEMO REŽIM - Automatické testování agenta\n")
    
    demo_questions = [
        "Kolik máme celkem produktů?",
        "Jaká je průměrná cena produktů?",
        "Které produkty mají nízké zásoby?",
        "Který produkt je nejdražší?",
        "Ukaž mi statistiky podle kategorií"
    ]
    
    for question in demo_questions:
        print(f"\n{'─'*60}")
        print(f"❓ {question}")
        response = agent.process_query(question)
        print(f"\n💬 {response}")
        print(f"{'─'*60}")
    
    # Uložení logu
    agent.save_log()
    
    # Interaktivní režim
    print("\n\n")
    choice = input("Chcete pokračovat v interaktivním režimu? (a/n): ")
    if choice.lower() in ['a', 'y', 'ano', 'yes']:
        agent.run_interactive()


if __name__ == "__main__":
    main()

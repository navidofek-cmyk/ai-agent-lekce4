"""
AI Agent s Databází a LLM - Rozšířená verze s OpenAI podporou
Podporuje dva režimy:
1. SIMULATOR (default) - funguje bez API klíče
2. OPENAI - používá skutečné GPT API (vyžaduje klíč)
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os


class DatabaseTool:
    """Nástroj pro práci s databází"""
    
    def __init__(self, db_path: str = "./data/products.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Inicializace databáze s ukázkovými daty"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
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
        
        cursor.execute('SELECT COUNT(*) FROM products')
        if cursor.fetchone()[0] == 0:
            products = [
                ('Notebook Dell XPS', 'Elektronika', 29990, 5, 'Výkonný ultrabook'),
                ('iPhone 15 Pro', 'Elektronika', 34990, 8, 'Nejnovější iPhone'),
                ('Samsung Galaxy S24', 'Elektronika', 24990, 12, 'Android smartphone'),
                ('Sony Sluchátka', 'Elektronika', 9990, 15, 'Bezdrátová sluchátka'),
                ('iPad Pro', 'Elektronika', 35990, 6, 'Tablet s M2 chipem'),
                ('Zimní bunda', 'Oblečení', 5990, 20, 'Zateplená bunda'),
                ('Běžecké boty Nike', 'Oblečení', 3490, 25, 'Sportovní obuv'),
                ('Mikina Adidas', 'Oblečení', 1490, 30, 'Bavlněná mikina'),
                ('Bio káva', 'Potraviny', 249, 50, 'Zrnková káva 250g'),
                ('Organický med', 'Potraviny', 189, 40, 'Lesní med 500g'),
                ('Čokoláda Lindt', 'Potraviny', 59, 100, 'Hořká čokoláda'),
                ('Dyson vysavač', 'Domácnost', 18990, 7, 'Bezdrátový vysavač'),
            ]
            cursor.executemany(
                'INSERT INTO products (name, category, price, stock, description) VALUES (?, ?, ?, ?, ?)',
                products
            )
        
        conn.commit()
        conn.close()
    
    def query(self, sql: str = None) -> List[Dict]:
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
    """Nástroj pro výpočty"""
    
    @staticmethod
    def calculate_by_category(products: List[Dict]) -> Dict:
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
        
        for cat in categories:
            cat_products = [p for p in products if p['category'] == cat]
            categories[cat]['avg_price'] = round(
                sum(p['price'] for p in cat_products) / len(cat_products), 2
            )
        
        return categories
    
    @staticmethod
    def find_low_stock(products: List[Dict], threshold: int = 10) -> List[Dict]:
        return [p for p in products if p['stock'] < threshold]
    
    @staticmethod
    def find_expensive(products: List[Dict], limit: int = 5) -> List[Dict]:
        return sorted(products, key=lambda x: x['price'], reverse=True)[:limit]


class LLMSimulator:
    """Simulace LLM - ZDARMA, žádné API"""
    
    @staticmethod
    def generate_response(question: str, data: Dict, stats: Dict) -> str:
        question_lower = question.lower()
        
        if 'kolik' in question_lower and ('produkt' in question_lower or 'celkem' in question_lower):
            return f"V databázi máme celkem {stats['total_products']} produktů. "\
                   f"Celková hodnota skladu je {stats['total_value']:,.0f} Kč."
        
        elif 'průměr' in question_lower or 'průměrná cena' in question_lower:
            return f"Průměrná cena produktů je {stats['avg_price']:,.0f} Kč. "\
                   f"Nejlevnější produkt stojí {stats['min_price']:,.0f} Kč a "\
                   f"nejdražší {stats['max_price']:,.0f} Kč."
        
        elif 'kategorie' in question_lower:
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
        
        elif 'nejdražší' in question_lower:
            expensive = data.get('expensive', [])
            if expensive:
                top = expensive[0]
                return f"Nejdražším produktem je {top['name']} za {top['price']:,.0f} Kč. "\
                       f"Máme ho {top['stock']} kusů na skladě."
            return "Nenalezeny žádné produkty."
        
        else:
            return f"Mám k dispozici informace o {stats['total_products']} produktech. "\
                   f"Průměrná cena je {stats['avg_price']:,.0f} Kč, "\
                   f"celková hodnota skladu {stats['total_value']:,.0f} Kč. "\
                   f"Můžete se zeptat na kategorie, ceny, zásoby nebo konkrétní produkty."


class OpenAILLM:
    """Skutečné OpenAI API - vyžaduje klíč"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.available = False
        
        try:
            import openai
            self.openai = openai
            self.openai.api_key = api_key
            self.available = True
            print("✅ OpenAI API připojeno")
        except ImportError:
            print("⚠️  OpenAI knihovna není nainstalovaná. Spusťte: pip install openai")
        except Exception as e:
            print(f"⚠️  OpenAI API chyba: {e}")
    
    def generate_response(self, question: str, data: Dict, stats: Dict) -> str:
        if not self.available:
            return "OpenAI API není dostupné. Použijte SIMULATOR režim."
        
        try:
            # Připrava kontextu pro GPT
            context = f"""Jsi AI asistent pracující s databází produktů.

Statistiky databáze:
- Celkem produktů: {stats['total_products']}
- Průměrná cena: {stats['avg_price']} Kč
- Cenové rozpětí: {stats['min_price']} - {stats['max_price']} Kč
- Celková hodnota skladu: {stats['total_value']} Kč

Produkty s nízkými zásobami:
{json.dumps([p['name'] + f" ({p['stock']} ks)" for p in data.get('low_stock', [])[:5]], ensure_ascii=False)}

Top nejdražší produkty:
{json.dumps([p['name'] + f" ({p['price']} Kč)" for p in data.get('expensive', [])[:3]], ensure_ascii=False)}

Kategorie:
{json.dumps(data.get('category_stats', {}), ensure_ascii=False)}

Odpověz na otázku uživatele v češtině, konkrétně a na základě těchto dat."""

            response = self.openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Chyba OpenAI API: {str(e)}. Zkuste SIMULATOR režim."


class AIAgent:
    """Hlavní AI Agent s podporou obou režimů"""
    
    def __init__(self, mode: str = "simulator"):
        self.db_tool = DatabaseTool()
        self.stats_tool = StatisticsTool()
        self.mode = mode.lower()
        
        # Inicializace LLM podle režimu
        if self.mode == "openai":
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.llm = OpenAILLM(api_key)
                if not self.llm.available:
                    print("⚠️  OpenAI nedostupné, přepínám na SIMULATOR")
                    self.llm = LLMSimulator()
                    self.mode = "simulator"
            else:
                print("⚠️  OPENAI_API_KEY není nastavený, používám SIMULATOR")
                self.llm = LLMSimulator()
                self.mode = "simulator"
        else:
            self.llm = LLMSimulator()
            self.mode = "simulator"
        
        self.query_log = []
        print(f"🤖 AI Agent režim: {self.mode.upper()}")
    
    def process_query(self, question: str) -> Dict:
        products = self.db_tool.query()
        stats = self.db_tool.get_statistics()
        
        category_stats = self.stats_tool.calculate_by_category(products)
        low_stock = self.stats_tool.find_low_stock(products)
        expensive = self.stats_tool.find_expensive(products)
        
        data = {
            'products': products,
            'category_stats': category_stats,
            'low_stock': low_stock,
            'expensive': expensive
        }
        
        response = self.llm.generate_response(question, data, stats)
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'response': response,
            'mode': self.mode
        }
        self.query_log.append(log_entry)
        
        return {
            'question': question,
            'answer': response,
            'timestamp': log_entry['timestamp'],
            'stats': stats,
            'mode': self.mode
        }


# Globální instance agenta
mode = os.getenv('LLM_MODE', 'simulator')
agent = AIAgent(mode=mode)


class AgentHTTPHandler(BaseHTTPRequestHandler):
    """HTTP handler pro web API"""
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            mode_badge = "🆓 ZDARMA (Simulátor)" if agent.mode == "simulator" else "🤖 OpenAI GPT"
            mode_color = "#27ae60" if agent.mode == "simulator" else "#3498db"
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>AI Agent s Databází</title>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial; max-width: 900px; margin: 50px auto; padding: 20px; }}
                    h1 {{ color: #2c3e50; }}
                    .mode-badge {{ background: {mode_color}; color: white; padding: 5px 15px; border-radius: 20px; font-size: 14px; }}
                    .container {{ background: #f8f9fa; padding: 20px; border-radius: 10px; }}
                    input[type="text"] {{ width: 70%; padding: 10px; font-size: 16px; }}
                    button {{ padding: 10px 20px; font-size: 16px; background: #3498db; color: white; border: none; cursor: pointer; border-radius: 5px; }}
                    button:hover {{ background: #2980b9; }}
                    .response {{ margin-top: 20px; padding: 15px; background: white; border-left: 4px solid #3498db; }}
                    .examples {{ margin: 20px 0; }}
                    .examples button {{ margin: 5px; background: #95a5a6; padding: 8px 15px; font-size: 14px; }}
                    .stats {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 20px 0; }}
                    .stat-box {{ background: white; padding: 15px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                    .info {{ background: #e8f4f8; padding: 10px; border-radius: 5px; margin: 10px 0; }}
                </style>
            </head>
            <body>
                <h1>🤖 AI Agent s Databází a LLM <span class="mode-badge">{mode_badge}</span></h1>
                
                <div class="info">
                    <strong>ℹ️ Režim:</strong> {agent.mode.upper()}<br>
                    <strong>📊 Databáze:</strong> SQLite s produkty<br>
                    <strong>🔧 Nástroje:</strong> Výpočetní funkce, statistiky, agregace
                </div>
                
                <div class="container">
                    <h3>Položte otázku agentovi:</h3>
                    <input type="text" id="question" placeholder="Např: Kolik máme celkem produktů?">
                    <button onclick="askAgent()">Zeptat se</button>
                    
                    <div class="examples">
                        <h4>Příklady otázek:</h4>
                        <button onclick="askExample('Kolik máme celkem produktů?')">Počet produktů</button>
                        <button onclick="askExample('Jaká je průměrná cena?')">Průměrná cena</button>
                        <button onclick="askExample('Které produkty mají nízké zásoby?')">Nízké zásoby</button>
                        <button onclick="askExample('Který produkt je nejdražší?')">Nejdražší</button>
                        <button onclick="askExample('Ukaž kategorie')">Kategorie</button>
                    </div>
                    
                    <div id="response" class="response" style="display: none;">
                        <h4>Odpověď:</h4>
                        <p id="answer"></p>
                        <div class="stats" id="stats"></div>
                    </div>
                </div>
                
                <script>
                    function askAgent() {{
                        const question = document.getElementById('question').value;
                        if (!question) return;
                        
                        fetch('/ask?q=' + encodeURIComponent(question))
                            .then(r => r.json())
                            .then(data => {{
                                document.getElementById('answer').innerText = data.answer;
                                document.getElementById('response').style.display = 'block';
                                
                                const stats = data.stats;
                                document.getElementById('stats').innerHTML = `
                                    <div class="stat-box">📦 Produktů: ${{stats.total_products}}</div>
                                    <div class="stat-box">💰 Průměr: ${{stats.avg_price}} Kč</div>
                                    <div class="stat-box">📊 Na skladě: ${{stats.total_stock}}</div>
                                    <div class="stat-box">💎 Hodnota: ${{stats.total_value}} Kč</div>
                                `;
                            }})
                            .catch(err => {{
                                alert('Chyba: ' + err);
                            }});
                    }}
                    
                    function askExample(q) {{
                        document.getElementById('question').value = q;
                        askAgent();
                    }}
                    
                    document.getElementById('question').addEventListener('keypress', function(e) {{
                        if (e.key === 'Enter') askAgent();
                    }});
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        
        elif self.path.startswith('/ask'):
            query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            question = query_components.get('q', [''])[0]
            
            result = agent.process_query(question)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")


def run_server(port=8000):
    """Spustí HTTP server"""
    server = HTTPServer(('0.0.0.0', port), AgentHTTPHandler)
    print(f"\n{'='*60}")
    print(f"🤖 AI Agent běží!")
    print(f"{'='*60}")
    print(f"\n🌐 Web rozhraní: http://localhost:{port}")
    print(f"📡 API endpoint: http://localhost:{port}/ask?q=<otázka>")
    print(f"🔧 Režim: {agent.mode.upper()}")
    print(f"\nStiskněte Ctrl+C pro zastavení\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Agent ukončen")


if __name__ == "__main__":
    run_server(8000)

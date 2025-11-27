"""
Testovací Python skript pro AI Agenta
Spuštění: python test_agent.py
"""

import requests
import json
import time
from datetime import datetime

WEBHOOK_URL = "http://localhost:5678/webhook/ask-agent"

QUESTIONS = [
    "Kolik máme celkem produktů?",
    "Jaká je průměrná cena všech produktů?",
    "Které produkty máme v kategorii Elektronika?",
    "Který produkt je nejdražší?",
    "Které produkty mají zásoby menší než 10 kusů?",
    "Jaká je celková hodnota skladových zásob?",
    "Porovnej kategorii Elektronika a Oblečení",
    "Udělej analýzu produktového portfolia"
]

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GRAY = '\033[90m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def print_colored(text, color):
    print(f"{color}{text}{Colors.RESET}")

def test_agent():
    print(f"\n{Colors.GREEN}=== Test AI Agenta s Databází ==={Colors.RESET}")
    print(f"{Colors.GRAY}Webhook URL: {WEBHOOK_URL}{Colors.RESET}")
    print(f"{Colors.GRAY}Počet testů: {len(QUESTIONS)}{Colors.RESET}")
    print(f"{Colors.GRAY}Čas spuštění: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}\n")
    
    success_count = 0
    error_count = 0
    results = []
    
    for i, question in enumerate(QUESTIONS, 1):
        test_num = f"[{i}/{len(QUESTIONS)}]"
        print(f"{Colors.MAGENTA}{test_num}{Colors.RESET} {Colors.CYAN}Q:{Colors.RESET} {question}")
        
        start_time = time.time()
        
        try:
            response = requests.post(
                WEBHOOK_URL,
                json={"question": question},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                answer = response.text
                print(f"{Colors.YELLOW}A:{Colors.RESET} {Colors.WHITE}{answer}{Colors.RESET}")
                print(f"{Colors.GRAY}⏱ Čas odpovědi: {elapsed:.2f}s{Colors.RESET}")
                
                results.append({
                    "question": question,
                    "answer": answer,
                    "time": elapsed,
                    "status": "success"
                })
                success_count += 1
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                print(f"{Colors.RED}ERROR: {error_msg}{Colors.RESET}")
                results.append({
                    "question": question,
                    "error": error_msg,
                    "status": "error"
                })
                error_count += 1
                
        except requests.exceptions.Timeout:
            print(f"{Colors.RED}ERROR: Request timeout (30s){Colors.RESET}")
            results.append({
                "question": question,
                "error": "Timeout",
                "status": "error"
            })
            error_count += 1
            
        except requests.exceptions.ConnectionError:
            print(f"{Colors.RED}ERROR: Connection failed. Je N8N spuštěný?{Colors.RESET}")
            results.append({
                "question": question,
                "error": "Connection Error",
                "status": "error"
            })
            error_count += 1
            
        except Exception as e:
            print(f"{Colors.RED}ERROR: {str(e)}{Colors.RESET}")
            results.append({
                "question": question,
                "error": str(e),
                "status": "error"
            })
            error_count += 1
        
        print(f"{Colors.GRAY}{'-' * 80}{Colors.RESET}")
        
        if i < len(QUESTIONS):
            time.sleep(2)
    
    # Souhrn
    print(f"\n{Colors.GREEN}=== Souhrn testování ==={Colors.RESET}")
    print(f"{Colors.GREEN}Úspěšné: {success_count}/{len(QUESTIONS)}{Colors.RESET}")
    
    if error_count > 0:
        print(f"{Colors.RED}Chybné: {error_count}/{len(QUESTIONS)}{Colors.RESET}")
    else:
        print(f"{Colors.GREEN}Chybné: {error_count}/{len(QUESTIONS)}{Colors.RESET}")
    
    # Průměrný čas odpovědi
    successful_times = [r["time"] for r in results if r["status"] == "success"]
    if successful_times:
        avg_time = sum(successful_times) / len(successful_times)
        print(f"{Colors.GRAY}Průměrný čas odpovědi: {avg_time:.2f}s{Colors.RESET}")
    
    print()
    
    if error_count == 0:
        print(f"{Colors.GREEN}✓ Všechny testy proběhly úspěšně!{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}✗ Některé testy selhaly. Zkontrolujte konfiguraci.{Colors.RESET}")
    
    # Uložení výsledků
    with open("test_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(QUESTIONS),
            "successful": success_count,
            "failed": error_count,
            "results": results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n{Colors.GRAY}Výsledky uloženy do: test_results.json{Colors.RESET}\n")

if __name__ == "__main__":
    test_agent()

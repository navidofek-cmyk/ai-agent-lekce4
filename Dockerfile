# Použijeme oficiální Python image
FROM python:3.11-slim

# Nastavíme pracovní adresář
WORKDIR /app

# Zkopírujeme rozšířenou verzi s OpenAI podporou
COPY python_agent_extended.py .

# Instalace OpenAI knihovny
RUN pip install --no-cache-dir openai

# SQLite je už součástí Python image, není potřeba instalovat

# Vytvoříme adresář pro databázi
RUN mkdir -p /app/data

# Nastavíme proměnné prostředí
ENV PYTHONUNBUFFERED=1
ENV LLM_MODE=simulator

# Exponujeme port pro web interface
EXPOSE 8000

# Spustíme agenta s web rozhraním
CMD ["python", "python_agent_extended.py"]

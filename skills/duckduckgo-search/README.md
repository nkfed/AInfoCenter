# DuckDuckGo Search Skill

Web search через DuckDuckGo без API ключів та реєстрації.

## Встановлення

```bash
# 1. Встановити залежності
pip install -r skills/duckduckgo-search/requirements.txt

# Або напряму
pip install duckduckgo-search

# 2. Перевірити встановлення
python skills/duckduckgo-search/duckduckgo_search.py "test" 3
```

## Тестування

```bash
# Windows PowerShell
python skills\duckduckgo-search\duckduckgo_search.py "weather Sambir Ukraine" 3

# Linux/WSL
python3 skills/duckduckgo-search/duckduckgo_search.py "weather Sambir Ukraine" 3
```

## Приклад виводу

```json
{
  "query": "weather Sambir Ukraine",
  "num_results": 3,
  "results": [
    {
      "title": "Weather in Sambir - AccuWeather",
      "url": "https://www.accuweather.com/...",
      "snippet": "Current weather conditions and forecast for Sambir...",
      "position": 1
    }
  ]
}
```

## Інтеграція з OpenClaw

Skill автоматично підхопиться OpenClaw при наступному запуску:

```bash
# Перезапустити gateway
systemctl --user restart clawdbot-gateway.service

# Або в Windows (foreground)
cd /root/clawd
./run.sh
```

## Використання ботом

Приклади запитів користувача, які активують цей skill:

- "Знайди інформацію про..."
- "Пошукай в інтернеті..."
- "Яка зараз погода в...?"
- "Останні новини про..."
- "Search for documentation on..."

Бот автоматично розпізнає необхідність веб-пошуку та використає цей skill.

## Переваги

✅ Безкоштовний  
✅ Без реєстрації та API ключів  
✅ Працює одразу  
✅ Приватність (DuckDuckGo не відстежує)  
✅ JSON вивід для легкої інтеграції

## Обмеження

- Тільки текстовий пошук (без зображень)
- ~10 результатів максимум
- Потрібен парсинг HTML (може зламатись якщо DDG змінить структуру)
- Rate limiting від DuckDuckGo (розумне використання)

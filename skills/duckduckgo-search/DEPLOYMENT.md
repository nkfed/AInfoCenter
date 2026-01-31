# Deployment на Production (WSL)

Цей файл містить інструкції для deployment DuckDuckGo Search skill на production сервер у WSL.

## Передумови

- Git налаштований на обох серверах
- SSH доступ до WSL
- Python 3.8+ встановлений на WSL

## Крок 1: Commit та Push з Dev (Windows)

```powershell
# На Windows (dev сервер)
cd D:\Projects\AInfoCenter

# Додати зміни
git add skills/duckduckgo-search/
git add memory/2026-01-31.md
git add MEMORY.md
git add .gitignore

# Commit
git commit -m "feat: add DuckDuckGo search skill

- Created skill for free web search without API keys
- Uses ddgs Python library
- Tested successfully on dev
- Auto-activates in OpenClaw/Clawdbot"

# Push to GitHub
git push origin main
```

## Крок 2: Pull та встановлення на Production (WSL)

```bash
# SSH до WSL або у WSL терміналі
cd /root/clawd

# Pull останні зміни
git pull origin main

# Перевірити що skill з'явився
ls -la skills/duckduckgo-search/

# Зробити скрипт виконуваним
chmod +x skills/duckduckgo-search/search.sh
chmod +x skills/duckduckgo-search/duckduckgo_search.py
```

## Крок 3: Встановлення залежностей

```bash
# Встановити ddgs бібліотеку
pip3 install ddgs

# Або через requirements.txt
pip3 install -r skills/duckduckgo-search/requirements.txt
```

## Крок 4: Тестування skill

```bash
# Тест через wrapper
./skills/duckduckgo-search/search.sh "test query" 3

# Або напряму
python3 skills/duckduckgo-search/duckduckgo_search.py "weather Sambir" 5
```

**Очікуваний результат:**
```json
{
  "query": "weather Sambir",
  "num_results": 5,
  "results": [
    {
      "position": 1,
      "title": "...",
      "url": "...",
      "snippet": "..."
    }
  ]
}
```

## Крок 5: Перезапуск Clawdbot Gateway

```bash
# Перезапустити systemd сервіс
systemctl --user restart clawdbot-gateway.service

# Перевірити статус
systemctl --user status clawdbot-gateway.service

# Подивитися логи
clawdbot logs --follow
```

## Крок 6: Перевірка активації skill

```bash
# Перевірити що skill підхоплено
clawdbot doctor

# Або через прямий запит у Telegram
# Напиши боту: "Пошукай інформацію про OpenAI"
```

## Troubleshooting

### Помилка: "ddgs not found"
```bash
# Переконайся що встановлено для правильного Python
which python3
python3 -c "from ddgs import DDGS; print('OK')"

# Якщо не працює, встанови знову
pip3 install --upgrade ddgs
```

### Помилка: "Permission denied"
```bash
# Зробити файли виконуваними
chmod +x skills/duckduckgo-search/*.sh
chmod +x skills/duckduckgo-search/*.py
```

### Skill не активується у боті
```bash
# Перевірити логи gateway
journalctl --user -u clawdbot-gateway.service -n 50

# Повний перезапуск
systemctl --user stop clawdbot-gateway.service
sleep 2
systemctl --user start clawdbot-gateway.service
```

### Conflict при git pull
```bash
# Якщо конфлікт у .gitignore або інших файлах
git status
git stash
git pull origin main
git stash pop
```

## Верифікація

Після deployment перевірити:

1. ✅ Skill файли присутні в `/root/clawd/skills/duckduckgo-search/`
2. ✅ Python може імпортувати `ddgs`
3. ✅ Тестовий запит повертає результати
4. ✅ Gateway перезапущено без помилок
5. ✅ Бот відповідає на запит "пошукай в інтернеті"

## Rollback (якщо щось не так)

```bash
# Повернутися до попередньої версії
cd /root/clawd
git log --oneline -5  # Знайти попередній commit
git reset --hard <commit-hash>
systemctl --user restart clawdbot-gateway.service
```

---

**Час deployment:** ~5-10 хвилин  
**Downtime:** ~5-10 секунд (час рестарту gateway)

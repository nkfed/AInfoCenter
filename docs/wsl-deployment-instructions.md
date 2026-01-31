# WSL Deployment: DuckDuckGo Search Skill

> **Дата:** 2026-01-31  
> **Версія:** 1.0  
> **Середовище:** WSL2 Ubuntu 24.04.3 LTS

---

## 📋 Огляд

Після `git pull` на production сервері (WSL) потрібно виконати наступні кроки для активації DuckDuckGo Search skill у Clawdbot.

**Що змінилося:**
- ➕ Додано новий skill: `skills/duckduckgo-search/`
- ✅ Безкоштовний веб-пошук без API ключів
- 📝 Оновлено документацію: `MEMORY.md`, `memory/2026-01-31.md`
- 🔒 Виправлено `.gitignore` (додано Python patterns)

**Час виконання:** 5-10 хвилин  
**Downtime:** 5-10 секунд (restart gateway)

---

## Крок 1: Перевірка файлів після git pull

```bash
cd /root/clawd

# Перевірити що skill з'явився
ls -la skills/duckduckgo-search/
```

**Очікувані файли:**
```
DEPLOYMENT.md           # Детальні інструкції
README.md              # Опис skill
SKILL.md               # Опис для OpenClaw
duckduckgo_search.py   # Python скрипт
requirements.txt       # Залежності
search.sh              # Linux wrapper
search.bat             # Windows wrapper (не використовується)
```

---

## Крок 2: Надання прав виконання

```bash
# Зробити скрипти виконуваними
chmod +x skills/duckduckgo-search/search.sh
chmod +x skills/duckduckgo-search/duckduckgo_search.py
```

---

## Крок 3: Встановлення Python залежностей

```bash
# Перевірити версію Python
python3 --version
# Має бути >= 3.8

# Встановити ddgs бібліотеку
pip3 install ddgs

# Альтернативно через requirements
pip3 install -r skills/duckduckgo-search/requirements.txt
```

**Верифікація встановлення:**
```bash
python3 -c "from ddgs import DDGS; print('✅ ddgs installed successfully')"
```

---

## Крок 4: Тестування skill (до активації у боті)

```bash
# Тест 1: Через wrapper
./skills/duckduckgo-search/search.sh "OpenAI news" 3

# Тест 2: Напряму Python
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
      "title": "Weather in Sambir - ...",
      "url": "https://...",
      "snippet": "Current weather..."
    }
  ]
}
```

**Якщо помилка:**
```bash
# Переконатися що ddgs встановлено
pip3 list | grep ddgs

# Переустановити якщо потрібно
pip3 install --upgrade --force-reinstall ddgs
```

---

## Крок 5: Активація skill у Clawdbot

```bash
# Перезапустити gateway для підхоплення нового skill
systemctl --user restart clawdbot-gateway.service

# Зачекати 5-10 секунд
sleep 10

# Перевірити статус
systemctl --user status clawdbot-gateway.service
```

**Перевірка логів:**
```bash
# Останні 50 рядків логу
clawdbot logs --limit 50

# Або через journalctl
journalctl --user -u clawdbot-gateway.service -n 50

# Режим реального часу (Ctrl+C для виходу)
clawdbot logs --follow
```

**Що шукати у логах:**
- ✅ `Loaded skill: duckduckgo-search`
- ✅ `Gateway started successfully`
- ❌ Будь-які `ERROR` або `WARN` повідомлення

---

## Крок 6: Тестування через Telegram бота

**В Telegram чаті з ботом:**

1. **Простий пошук:**
   ```
   Пошукай інформацію про Python programming
   ```

2. **Новини:**
   ```
   Знайди останні новини про OpenAI
   ```

3. **Погода:**
   ```
   Яка зараз погода в Самборі?
   ```

4. **Технічна документація:**
   ```
   Search for Node.js documentation
   ```

**Очікувана поведінка:**
- Бот використовує `duckduckgo_search` tool
- Повертає список результатів з title, URL, snippet
- Відповідь протягом 2-5 секунд

---

## Troubleshooting

### ❌ Помилка: "ddgs not found"

**Діагностика:**
```bash
which python3
python3 -m pip list | grep ddgs
```

**Рішення:**
```bash
# Встановити для правильного Python
pip3 install ddgs

# Або через sudo якщо потрібно
sudo pip3 install ddgs
```

---

### ❌ Помилка: "Permission denied"

**Рішення:**
```bash
chmod +x skills/duckduckgo-search/*.sh
chmod +x skills/duckduckgo-search/*.py
```

---

### ❌ Skill не активується у боті

**Діагностика:**
```bash
# Перевірити структуру skill
cat skills/duckduckgo-search/SKILL.md | head -n 10

# Перевірити що gateway бачить skill
clawdbot doctor
```

**Рішення:**
```bash
# Повний перезапуск
systemctl --user stop clawdbot-gateway.service
sleep 3
systemctl --user start clawdbot-gateway.service

# Перевірити статус
systemctl --user status clawdbot-gateway.service
```

---

### ❌ "Search failed" у відповіді бота

**Можливі причини:**
1. DuckDuckGo тимчасово недоступний
2. Rate limiting (забагато запитів)
3. Мережева проблема

**Перевірка:**
```bash
# Тест з WSL напряму
curl -s "https://duckduckgo.com" | head -n 5

# Тест skill вручну
python3 skills/duckduckgo-search/duckduckgo_search.py "test" 1
```

---

## Верифікація успішного deployment

Після виконання всіх кроків перевірити:

- [ ] ✅ Skill файли присутні в `/root/clawd/skills/duckduckgo-search/`
- [ ] ✅ Python бібліотека `ddgs` встановлена
- [ ] ✅ Тестовий запит через CLI повертає результати
- [ ] ✅ Gateway перезапущено без помилок у логах
- [ ] ✅ Бот відповідає на запит пошуку в Telegram
- [ ] ✅ Результати пошуку релевантні та мають title/URL/snippet

---

## Rollback (якщо щось пішло не так)

```bash
cd /root/clawd

# Подивитися історію commits
git log --oneline -5

# Повернутися до попередньої версії
git reset --hard HEAD~1

# Перезапустити gateway
systemctl --user restart clawdbot-gateway.service
```

---

## Моніторинг після deployment

**Перші 24 години:**
```bash
# Переглядати логи періодично
clawdbot logs --limit 100

# Перевірити використання пам'яті
systemctl --user status clawdbot-gateway.service | grep Memory

# Кількість рестартів
systemctl --user show clawdbot-gateway.service | grep NRestarts
```

**Метрики успіху:**
- Пошукові запити обробляються за 2-5 секунд
- Немає помилок у логах
- Memory usage стабільний (~220-250MB)

---

## Додаткова інформація

**Документація skill:**
- Детальні інструкції: `skills/duckduckgo-search/DEPLOYMENT.md`
- Опис використання: `skills/duckduckgo-search/README.md`
- Технічний опис: `skills/duckduckgo-search/SKILL.md`

**Обмеження:**
- До 10 результатів за запит
- Тільки текстовий пошук (без зображень)
- DuckDuckGo rate limiting (~50-100 запитів/хвилину)

**Альтернативи якщо не працює:**
- `fast-browser-use` skill з ClawHub
- SearXNG self-hosted
- Google Custom Search API (потребує біллінгу)

---

**Deployment виконав:** GitHub Copilot (Coordinator AI)  
**Дата створення:** 2026-01-31  
**Статус:** Ready for production deployment

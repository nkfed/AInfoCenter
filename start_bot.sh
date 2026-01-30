#!/bin/bash
# 1. Основні змінні
export TELEGRAM_TOKEN="7301177330:AAEyqbZ-yiJOZp6vlhQaX0-urFIwVmOrDhw"

# 2. Google Chat (спробуємо назву з файлу конфігурації)
export GOOGLE_CHAT_ENABLED=true
export GOOGLE_CHAT_CREDENTIALS="/root/clawd/google-key.json"

# 3. Варіанти з префіксом (на випадок суворого парсингу)
export CLAWDBOT_GOOGLE_CHAT_ENABLED=true
export CLAWDBOT_GOOGLE_CHAT_CREDENTIALS="/root/clawd/google-key.json"

# 4. Рідкісний варіант без підкреслення (як у назві файлу)
export GOOGLECHAT_ENABLED=true
export GOOGLECHAT_CREDENTIALS="/root/clawd/google-key.json"

# 5. Стандарт Google
export GOOGLE_APPLICATION_CREDENTIALS="/root/clawd/google-key.json"

echo "--- STARTING CLAWDBOT GATEWAY ---"
# Запускаємо з DEBUG, щоб побачити лог завантаження конфігу
DEBUG=clawdbot:config,clawdbot:gateway* /root/.nvm/versions/node/v22.22.0/bin/node /root/.npm/_npx/62b238e69bebfcb8/node_modules/clawdbot/dist/entry.js gateway --port 18789

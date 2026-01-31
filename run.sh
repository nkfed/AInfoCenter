#!/bin/bash
# Завантажуємо змінні з .env
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "--- ЗАПУСК CLAWDBOT (TELEGRAM) ---"
# Використовуємо змінні з .env, а не хардкод
# TELEGRAM_BOT_TOKEN береться з TELEGRAM_TOKEN
export TELEGRAM_BOT_TOKEN="$TELEGRAM_TOKEN"

/root/.nvm/versions/node/v22.22.0/bin/node /root/.nvm/versions/node/v22.22.0/lib/node_modules/clawdbot/dist/entry.js gateway --port 18789

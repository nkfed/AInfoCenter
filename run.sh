#!/bin/bash
# Використовуємо лише те, що бот точно бачить
export TELEGRAM_BOT_TOKEN="7301177330:AAEyqbZ-yiJOZp6vlhQaX0-urFIwVmOrDhw"
export GOOGLE_APPLICATION_CREDENTIALS="/root/clawd/google-key.json"

echo "--- ЗАПУСК CLAWDBOT (TELEGRAM) ---"
/root/.nvm/versions/node/v22.22.0/bin/node /root/.nvm/versions/node/v22.22.0/lib/node_modules/clawdbot/dist/entry.js gateway --port 18789

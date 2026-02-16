#!/bin/bash
# Завантажуємо змінні з .env
cd /root/clawd
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# TELEGRAM_BOT_TOKEN береться з TELEGRAM_TOKEN
export TELEGRAM_BOT_TOKEN="$TELEGRAM_TOKEN"
echo "Starting with Telegram Token: ${TELEGRAM_TOKEN:0:5}..."

/root/.nvm/versions/node/v22.22.0/bin/node \
  /root/.nvm/versions/node/v22.22.0/lib/node_modules/clawdbot/dist/entry.js \
  gateway --port 18789 --allow-unconfigured

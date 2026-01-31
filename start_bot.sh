#!/bin/bash
# Завантажуємо змінні з .env
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Змінна TELEGRAM_TOKEN тепер береться з .env
echo "Starting with Telegram Token: ${TELEGRAM_TOKEN:0:5}..."

# ... (інші команди, якщо є)

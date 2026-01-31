# Технічна архітектура проекту Clawd Bot

> **Версія документа:** 1.0  
> **Дата оновлення:** 2026-01-30  
> **Статус:** Production-Ready

---

## 📋 Загальний огляд

**Clawd Bot** — це AI-координатор на базі Clawdbot CLI, розгорнутий у WSL2 середовищі для автоматизації робочих процесів бізнес-аналітика. 
Система інтегрована з Telegram Bot API, Google Gemini Pro та підтримує віддалений доступ через SSH/VS Code.

---

## 🏗️ Інфраструктура

### Операційне середовище

| Компонент | Специфікація |
|-----------|--------------|
| **ОС** | Ubuntu 24.04.3 LTS (WSL2) |
| **Kernel** | 6.6.87.2-microsoft-standard-WSL2 |
| **Host** | Windows 10 LSTC (Lenovo) |
| **Архітектура** | x86_64 |
| **WSL IP** | 172.23.77.240 (динамічний) |

### Runtime Environment

| Технологія | Версія | Шлях |
|------------|--------|------|
| **Node.js** | v22.22.0 | `/root/.nvm/versions/node/v22.22.0/bin/node` |
| **npm** | 11.8.0 | `/root/.nvm/versions/node/v22.22.0/bin/npm` |
| **NVM** | 0.39.7 | Керування версіями Node.js |
| **Clawdbot CLI** | 2026.1.24-3 (885167d) | `/root/.nvm/versions/node/v22.22.0/bin/clawdbot` |

**NVM встановлення:** Node.js керується через NVM для ізоляції версій та легкого оновлення.

---

## 🤖 AI Core & Integration

### Модель штучного інтелекту

```json
{
  "primary": "google/gemini-3-pro-preview",
  "provider": "Google AI Studio",
  "maxConcurrent": 4,
  "subagents.maxConcurrent": 8
}
```

**Аутентифікація Google:**
- **Service Account:** `clawdbot-helpdesk@[PROJECT_ID].iam.gserviceaccount.com`
- **Project ID:** `[PROJECT_ID]` (анонімізовано)
- **Credentials:** `/root/clawd/google-key.json` (приватний ключ RSA 2048-bit)
- **OAuth 2.0:** Token URI: `https://oauth2.googleapis.com/token`

### Telegram Bot Integration

| Параметр | Значення |
|----------|----------|
| **Bot Token** | `7301...Dhw` [TOKEN_HIDDEN] |
| **DM Policy** | `pairing` (потребує авторизації) |
| **Group Policy** | `allowlist` (лише дозволені групи) |
| **Stream Mode** | `partial` (потокова відповідь) |
| **Status** | ✅ Enabled |

### Google Chat Integration

| Параметр | Значення |
|----------|----------|
| **Status** | ⚠️ Disabled (нестабільна конфігурація) |
| **Group Policy** | `open` |
| **Audience** | `https://tannable-cooly-sloan.ngrok-free.dev` |
| **Webhook Path** | `/googlechat` |

---

## 🌐 Network Architecture

### Gateway Configuration

```yaml
Gateway:
  Mode: local
  Port: 18789
  Bind: loopback (127.0.0.1)
  Auth:
    Mode: token
    Token: [TOKEN_HIDDEN] (48-символьний hex)
  Protocol: WebSocket (WSS)
```

**SSH Port Forwarding (для Windows доступу):**
```bash
ssh -N -L 18789:127.0.0.1:18789 root@<WSL_IP>
```

⚠️ **Важливо:** WSL IP-адреса динамічна та змінюється після перезавантаження Windows.

**Як дізнатися актуальний IP:**
```bash
# У WSL терміналі
ip addr show eth0 | grep "inet " | awk '{print $2}' | cut -d/ -f1

# Або з Windows PowerShell
wsl hostname -I
```

### Системний сервіс

**Systemd Unit:** `clawdbot-gateway.service`

```ini
[Unit]
Description=Clawdbot Gateway (v2026.1.24-3)

[Service]
Type=simple
ExecStart=/root/.nvm/versions/node/v22.22.0/bin/clawdbot gateway
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=default.target
```

**Управління:**
- **Location:** `/root/.config/systemd/user/clawdbot-gateway.service`
- **Override:** `/root/.config/systemd/user/clawdbot-gateway.service.d/override.conf`
- **Auto-start:** Enabled
- **Restart Policy:** 466 automatic restarts (з моменту налаштування)

---

## 📁 Структура проекту

### Директорії

```
/root/clawd/                      # Основний workspace
├── docs/                         # Документація
│   ├── architecture.md           # Цей файл
│   └── user-guide.md             # Посібник користувача
├── memory/                       # Щоденні логи агента
│   └── 2026-01-30.md            # Автоматичні записи подій
├── canvas/                       # Web UI компоненти
│   └── index.html               # Тестовий інтерфейс
├── knowledge/                    # База знань (порожня)
├── .git/                         # Git репозиторій
└── config files...

/root/.clawdbot/                  # Глобальна конфігурація Clawdbot
├── clawdbot.json                 # Основний конфіг
├── agents/                       # Ізольовані агенти
├── credentials/                  # Токени та ключі
├── telegram/                     # Telegram-специфічні дані
├── cron/                         # Заплановані завдання
├── devices/                      # Підключені пристрої
├── memory/                       # Глобальна пам'ять
└── identity/                     # Ідентифікація агента
```

### Ключові файли конфігурації

| Файл | Призначення |
|------|-------------|
| **IDENTITY.md** | Визначення ролі агента ("Координатор") |
| **SOUL.md** | Філософія та принципи роботи |
| **AGENTS.md** | Інструкції для AI агента (192 рядки) |
| **USER.md** | Профіль користувача (Микола Fedorov) |
| **MEMORY.md** | Довготривала пам'ять системи |
| **HEARTBEAT.md** | Проактивні завдання (зараз порожній) |
| **TOOLS.md** | Локальні нотатки та налаштування |
| **config.json** | Конфігурація providers |
| **.env** | Змінні оточення (credentials) |
| **google-key.json** | Google Service Account ключ |

### Git управління

```bash
Repository: https://github.com/nkfed/AInfoCenter.git
Branch: main (up-to-date with origin)
Last commits:
  4a970d5 - Sync workspace and disable unstable Google Chat
  c9d97b4 - Initial commit: basic bot structure and security
```

**Ignored files (.gitignore):**
- `.env` — Секретні змінні
- `google-key.json` — API ключі
- `bot.log` — Робочі логи
- `.clawdbot/` — Локальний стан
- `*.pem, *.key` — Приватні ключі

---

## 🔒 Безпека

### Секретне управління

1. **Environment Variables** — токени в `.env`, не комітяться в Git
2. **Service Account Keys** — `google-key.json` виключений з репозиторію
3. **Gateway Token** — 48-символьний hex токен для WebSocket авторизації
4. **SSH Access** — root доступ через ключі (паролі вимкнені)

### Exec Approvals

Файл `~/.clawdbot/exec-approvals.json` контролює дозволи на виконання команд:
```json
{
  "nextApprovalId": 1,
  "rules": []
}
```

---

## 🚀 Deployment & Scripts

### Скрипти автоматизації

#### 1. **run.sh** — Основний запуск

```bash
#!/bin/bash
export TELEGRAM_BOT_TOKEN="[TOKEN_HIDDEN]"
export GOOGLE_APPLICATION_CREDENTIALS="/root/clawd/google-key.json"

/root/.nvm/versions/node/v22.22.0/bin/node \
  /root/.nvm/versions/node/v22.22.0/lib/node_modules/clawdbot/dist/entry.js \
  gateway --port 18789
```

**Використання:** Ручний запуск gateway у foreground режимі.

#### 2. **start_bot.sh** — Debug запуск

```bash
#!/bin/bash
export DEBUG=clawdbot:config,clawdbot:gateway*
# Множинні варіанти змінних для тестування
/root/.npm/_npx/.../node_modules/clawdbot/dist/entry.js gateway --port 18789
```

**Використання:** Налагодження конфігурації з детальними логами.

#### 3. **update_bot.sh** — Оновлення

```bash
#!/bin/bash
cd /root/clawd
git pull
systemctl --user restart clawdbot-gateway.service
```

**Використання:** Синхронізація з GitHub та рестарт сервісу.

---

## 🎨 Canvas UI

### Інтерактивний тестовий інтерфейс

**Файл:** `/root/clawd/canvas/index.html`

**Призначення:** Розробка інтерактивних UI-віджетів, які бот може відображати безпосередньо в чаті для візуалізації даних, дашбордів та користувацьких інтерфейсів.

**Функції:**
- Тестові кнопки: Hello, Time, Photo, Dalek
- Bridge для iOS/Android: `window.webkit.messageHandlers.clawdbotCanvasA2UIAction`
- Event listener: `clawdbot:a2ui-action-status`
- Auto-reload для розробки
- Можливість створювати кастомні дашборди для аналітики

**Доступ:**
```bash
# Через port forwarding
http://localhost:18789/canvas/
```

---

## 🔄 CI/CD & Monitoring

### Системне моніторингу

**Systemd журнал:**
```bash
journalctl --user -u clawdbot-gateway.service -f
```

**Clawdbot логи:**
```bash
clawdbot logs --follow
```

**Memory Usage:** ~218.6MB (peak: 219.2MB)  
**CPU Usage:** ~8.1s на запуск  
**Restart Counter:** 466 (автоматичні рестарти при збоях)

### Health Checks

**Clawdbot Doctor:**
```bash
clawdbot doctor          # Діагностика
clawdbot doctor --fix    # Автовиправлення
```

---

## 📊 Performance Metrics

| Метрика | Значення |
|---------|----------|
| **Gateway Startup** | ~5-8 секунд |
| **Memory Footprint** | 218.6 MB |
| **Concurrent Agents** | 4 (primary) + 8 (subagents) |
| **WebSocket Latency** | <50ms (локально) |
| **Telegram Response** | ~1-3 секунди |
| **Model Inference** | залежить від Gemini API |

---

## 🔧 Development Tools

### VS Code Remote Development

**SSH Config:**
```ssh
Host wsl-clawd
  HostName 172.23.77.240
  User root
  IdentityFile ~/.ssh/id_rsa
  ForwardAgent yes
```

**Extensions:**
- Remote - SSH
- GitLens
- Markdown All in One

**Terminal Integration:** Прямий доступ до `/root/clawd/` workspace.

---

## 🌟 Майбутні покращення

- [ ] Інтеграція Google Chat (стабілізація)
- [ ] Dashboard UI розробка
- [ ] Cron scheduler для періодичних завдань
- [ ] Slack/Discord інтеграція
- [ ] Vector database для knowledge base
- [ ] Metrics dashboard (Prometheus/Grafana)

---

## 📚 Додаткові ресурси

- **Official Docs:** https://docs.clawd.bot/
- **CLI Reference:** https://docs.clawd.bot/cli/
- **GitHub:** https://github.com/nkfed/AInfoCenter
- **Node Version Manager:** https://github.com/nvm-sh/nvm

---

*Документ створено автоматично на базі технічного аудиту системи.*

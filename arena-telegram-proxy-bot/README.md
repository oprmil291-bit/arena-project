# Arena.ai Telegram Proxy Bot

Telegram bot proxy for Arena.ai with a separate Playwright session for each Telegram user.

## User Flow

Each user has their own storage state:

```text
sessions/users/<telegram_user_id>/storage_state.json
```

Commands:

```text
/start          show current state
/verify         start a personal remote browser for Arena verification
/verify_done    save storage_state after the user completes verification
/verify_cancel  stop the active verification browser
/new            start a new Arena dialog
/status         show personal session status
```

## Mode Switcher

After `/start` and `/verify_done`, the bot sends an inline control panel with four modes:

```text
Text   Image
Search Vip
```

Telegram does not have a native dropdown, so model selection is implemented as a paginated inline list under the selected mode.

Mode mapping:

```text
Text   -> https://arena.ai/text/direct
Image  -> https://arena.ai/image/direct
Search -> https://arena.ai/search/direct
Vip    -> https://arena.ai/text/direct + Arena Max preset
```

What the panel shows:

- current mode
- current model
- mode description
- capabilities / intended use
- Arena route
- paginated list of Arena models for that mode

The model list is scraped from Arena live and cached in the bot process.

When Arena requires `Security Verification`, reCAPTCHA, or login/account creation, the bot sends the user to `/verify`. The user opens a temporary noVNC browser link, manually passes Arena verification or logs in/creates an Arena account in that remote browser, then returns to Telegram and sends `/verify_done`. The saved browser state is then used for that specific Telegram user only.

## Local Setup

```bash
cp .env.example .env
```

Fill `TELEGRAM_BOT_TOKEN`, then install:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
playwright install
playwright install-deps
```

On Windows, use `py -3.12 -m venv .venv`. `playwright install-deps` is Linux-only.

Run locally:

```bash
python -m arena_proxy_bot
```

## VPS Setup

Project path:

```text
/opt/arena-telegram-proxy-bot
```

Environment file:

```text
/etc/arena-bot.env
```

Required VPS packages for `/verify`:

```bash
apt-get install -y xvfb openbox x11vnc novnc websockify
ufw allow 6080:6099/tcp
```

Environment example on VPS:

```bash
TELEGRAM_BOT_TOKEN=...
ARENA_BASE_URL=https://arena.ai/text/direct
ARENA_HEADLESS=false
ARENA_LOG_LEVEL=INFO
ARENA_MESSAGE_TIMEOUT_SEC=180
ARENA_SESSIONS_ROOT=sessions/users
ARENA_VERIFY_PUBLIC_SCHEME=http
ARENA_VERIFY_PUBLIC_HOST=5.129.242.93
ARENA_VERIFY_PORT_START=6080
ARENA_VERIFY_PORT_END=6099
ARENA_VERIFY_VNC_PORT_START=5900
```

Systemd:

```bash
systemctl status arena-bot
journalctl -u arena-bot -f
systemctl restart arena-bot
systemctl stop arena-bot
systemctl start arena-bot
```

Short commands:

```bash
bot-status
bot-logs
bot-restart
bot-stop
bot-start
```

The VPS service runs Chromium through `xvfb-run`, so `ARENA_HEADLESS=false` is expected.
Arena timeout diagnostics are saved in:

```text
/opt/arena-telegram-proxy-bot/logs/diagnostics/
```

## Deploy Updates

From the local machine:

```powershell
.\scripts\deploy.ps1
ssh arena-vps "cd /opt/arena-telegram-proxy-bot && .venv/bin/pip install -e . && systemctl restart arena-bot"
```

## Security Notes

Do not commit `.env`, `sessions/`, or `logs/`.

noVNC ports `6080-6099` are exposed for temporary verification browsers. Each VNC session uses a random password sent only to the requesting Telegram user. For production with many users, put this behind HTTPS and a reverse proxy with short-lived signed URLs.

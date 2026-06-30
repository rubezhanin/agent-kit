# Telethon userbot для AI-агента: полная безопасная настройка

Версия: 2026-05-03  
Основа: официальный репозиторий Telethon — https://github.com/LonamiWebs/Telethon  
Назначение: инструкция для человека и для агента, чтобы поднять Telegram-юзербота через Telethon, подключить его к агентной системе через MCP и не сжечь аккаунт.

---

## 0. Короткий вывод

**Telethon** — это не готовый лидоген-бот. Это Python-библиотека для работы с Telegram через **MTProto**.

Правильная архитектура для агента:

```text
AI agent
  -> MCP tools / controlled tool API
  -> local Telegram userbot service
  -> Telethon
  -> MTProto
  -> Telegram
```

Так агент получает не “ключи от квартиры”, а ограниченные инструменты:

- читать разрешённые чаты;
- искать сообщения;
- экспортировать ограниченные данные;
- готовить черновики;
- отправлять сообщения только в allowlist-чаты;
- логировать каждое действие;
- останавливаться на лимитах и `FloodWait`.

**Главное правило:** сначала read-only. Отправка сообщений включается только после smoke-тестов, allowlist и лимитов.

---

## 1. Что получится после настройки

После установки будет локальный проект:

```text
telegram-agent-userbot/
  app/
    auth.py              # вход / статус авторизации
    config.py            # настройки, .env, allowlist
    client.py            # Telethon client factory
    read_tools.py        # list_chats, get_messages, search_messages
    send_tools.py        # send_message, send_file с защитами
    audit.py             # SQLite audit log
    rate_limit.py        # лимиты + FloodWait handling
    mcp_server.py        # MCP stdio server для AI-агентов
  data/
    userbot-session.session
    audit.sqlite
  logs/
  .env
  .env.example
  requirements.txt
  README.md
```

Минимальный набор функций:

- `auth-status` — проверить, залогинен ли аккаунт;
- `auth-login` — первый ручной вход;
- `list-chats` — список доступных диалогов;
- `get-messages` — последние сообщения из разрешённого чата;
- `search-messages` — поиск по разрешённому чату;
- `send-message` — отправка, только если включена и чат разрешён;
- `send-file` — файл, только если включено и чат разрешён;
- MCP tools для агента.

---

## 2. Важные понятия: bot, userbot, Telethon, MCP

### Bot API / обычный бот

Это бот через `@BotFather`.

Плюсы:

- официально и безопаснее;
- не нужен номер телефона;
- меньше риск блокировок;
- удобно для поддержки, форм, уведомлений.

Минусы:

- бот не видит чужие чаты, если его туда не добавили;
- не может вести себя как обычный пользователь;
- ограничен Bot API.

### Userbot / юзербот

Это программа, которая логинится как обычный Telegram-аккаунт.

Плюсы:

- видит те чаты, куда добавлен аккаунт;
- может читать каналы/группы как пользователь;
- может писать от имени аккаунта;
- подходит для личного ассистента, CRM, research, controlled outreach.

Минусы:

- выше риск блокировки;
- нельзя использовать для спама;
- нужна отдельная SIM/аккаунт;
- нужно уважать лимиты Telegram;
- session-файл равен доступу к аккаунту.

### Telethon

Официальная база для этой инструкции:

```text
https://github.com/LonamiWebs/Telethon
```

Факты по репозиторию на момент проверки:

- репозиторий: `LonamiWebs/Telethon`;
- описание: `Pure Python 3 MTProto API Telegram client library, for bots too!`;
- язык: Python;
- лицензия: MIT;
- актуальная локально проверенная версия в нашем Lalo-контуре: `telethon==1.43.2`.

### MCP

MCP — Model Context Protocol. Для агента это способ получить аккуратные tools вместо прямого доступа к коду и секретам.

Пример:

```text
mcp_telegram_list_chats
mcp_telegram_get_messages
mcp_telegram_send_message
mcp_telegram_send_file
```

Агент вызывает tool. Tool проверяет allowlist, лимиты, пишет audit log, и только потом вызывает Telethon.

---

## 3. Риски и предупреждения

Это важная часть. Без неё инструкция вредная.

### За что Telegram может ограничить или заблокировать аккаунт

Риски повышаются, если аккаунт:

- массово пишет незнакомым людям;
- быстро рассылает одинаковые сообщения;
- вступает в много групп/каналов подряд;
- парсит большие объёмы чатов без нормального темпа;
- получает жалобы;
- использует “anti-ban”, “mass DM”, “auto-join” софт;
- работает с нового непрогретого аккаунта агрессивно;
- шлёт ссылки, офферы, крипту, казино, финансы, серые темы;
- пишет людям без opt-in/контекста.

### Безопасный режим

Разрешённый нормальный сценарий:

```text
read/search -> draft -> human approval -> send to allowlisted chat
```

Опасный сценарий:

```text
scrape -> mass DM -> repeat -> hope
```

Не делаем так. Аккаунт сгорит.

### Минимальные лимиты на старте

Для нового или отдельного аккаунта:

```text
TG_MAX_SEND_PER_HOUR=10
TG_MAX_SEND_PER_DAY=50
jitter между отправками: 2-7 секунд
только allowlist чаты
без auto-join
без массовых private DM
```

Для research/read-only:

```text
лимит сообщений на экспорт: 100-500 за запуск
пауза между чатами: 2-5 секунд
private chats — только если владелец явно указал scope
```

### Session-файл

Файл вида:

```text
data/userbot-session.session
```

Это практически ключ к Telegram-аккаунту.

Правила:

- не коммитить;
- не отправлять в чат;
- не класть в облако без шифрования;
- права `600`;
- папка `data/` с правами `700`;
- отдельный аккаунт, не основной личный.

---

## 4. Что уже есть в Mike/Hermes

У нас уже есть рабочая безопасная база — Lalo read-only Telethon collector:

```text
/Users/aleksejulanov/Desktop/MIKE_CENTER/agents/lalo/tools/telegram-userbot/
```

Entrypoint:

```text
/Users/aleksejulanov/Desktop/MIKE_CENTER/agents/lalo/tools/telegram-userbot/bin/lalo-telegram
```

Проверенные команды:

```bash
cd /Users/aleksejulanov/Desktop/MIKE_CENTER/agents/lalo

tools/telegram-userbot/bin/lalo-telegram --help
tools/telegram-userbot/bin/lalo-telegram auth-status
tools/telegram-userbot/bin/lalo-telegram auth-login
tools/telegram-userbot/bin/lalo-telegram check-access @channel
tools/telegram-userbot/bin/lalo-telegram stats-channel @channel --days 14 --limit 200 --format json
tools/telegram-userbot/bin/lalo-telegram search @channel "query" --days 90 --limit 100
tools/telegram-userbot/bin/lalo-telegram export-chat @channel --days 7 --limit 200
tools/telegram-userbot/bin/lalo-telegram stats-batch --targets @a,@b --days 14 --delay 2
```

Статус этой базы:

- Telethon установлен;
- сессия авторизована в Lalo-owned storage;
- инструмент read-only;
- нет send/join/leave/ban/edit;
- секреты не печатаются;
- это правильная отправная точка.

Решение: **не ломать Lalo collector**. Для отправки сообщений делаем отдельный guarded слой или отдельный проект.

---

## 5. Вариант A — использовать существующую Lalo-базу read-only

Этот вариант нужен, если задача: анализ каналов, research, поиск сигналов, экспорт сообщений, market intelligence.

### Проверить инструмент

```bash
cd /Users/aleksejulanov/Desktop/MIKE_CENTER/agents/lalo

tools/telegram-userbot/bin/lalo-telegram --help
```

Ожидаемые команды:

```text
auth-status
auth-login
check-access
stats-channel
search
export-chat
stats-batch
```

### Проверить авторизацию

```bash
tools/telegram-userbot/bin/lalo-telegram auth-status
```

Ожидаемо:

```text
authorized: true
```

Не печатать session path, phone, api_hash, api_id в публичные отчёты.

### Проверить доступ к каналу

```bash
tools/telegram-userbot/bin/lalo-telegram check-access @telegram
```

### Получить статистику канала

```bash
tools/telegram-userbot/bin/lalo-telegram stats-channel @telegram --days 30 --limit 100 --format json --no-text
```

### Поиск сообщений

```bash
tools/telegram-userbot/bin/lalo-telegram search @some_channel "AI agent" --days 90 --limit 50
```

### Экспорт без текста

```bash
tools/telegram-userbot/bin/lalo-telegram export-chat @some_channel --days 7 --limit 200
```

### Экспорт с текстом

Только если scope разрешён:

```bash
tools/telegram-userbot/bin/lalo-telegram export-chat @some_channel --days 7 --limit 200 --include-text
```

---

## 6. Вариант B — чистая установка нового userbot-проекта

Этот вариант нужен, если делаем отдельный продуктовый userbot/MCP service.

### 6.1. Требования

Проверить Python:

```bash
python3 --version
```

Нужно:

```text
Python 3.11+
```

Проверить git:

```bash
git --version
```

Проверить место:

```bash
df -h .
```

### 6.2. Создать проект

```bash
mkdir -p ~/telegram-agent-userbot
cd ~/telegram-agent-userbot
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
```

Создать `requirements.txt`:

```bash
cat > requirements.txt <<'EOF'
telethon==1.43.2
python-dotenv>=1.0.1
typer>=0.12.0
rich>=13.7.0
pydantic>=2.0.0
mcp>=1.0.0
aiosqlite>=0.20.0
EOF
```

Установить:

```bash
pip install -r requirements.txt
```

Создать структуру:

```bash
mkdir -p app data logs scripts
chmod 700 data logs
```

Создать `.gitignore`:

```bash
cat > .gitignore <<'EOF'
.env
*.session
*.session-journal
data/*.sqlite
data/*.db
logs/*.log
__pycache__/
.venv/
.DS_Store
EOF
```

---

## 7. Получить Telegram API ID / API HASH

Это делается один раз.

1. Открыть:

```text
https://my.telegram.org
```

2. Войти по номеру телефона Telegram-аккаунта, который будет юзерботом.

3. Открыть:

```text
API development tools
```

4. Создать приложение.

Пример полей:

```text
App title: Agent Userbot
Short name: agentuserbot
Platform: Desktop
Description: Personal assistant / CRM helper for owned Telegram account
```

5. Сохранить:

```text
api_id
api_hash
```

Важно:

- `api_hash` не отправлять в чат;
- не класть в README;
- не коммитить;
- хранить только в `.env` или secrets manager.

---

## 8. Настроить `.env`

Создать `.env.example`:

```bash
cat > .env.example <<'EOF'
TG_API_ID=123456
TG_API_HASH=replace_me
TG_SESSION=./data/userbot-session

# Safe default: sending disabled
TG_SEND_ENABLED=false

# Comma-separated allowlist. Use usernames or numeric chat IDs.
TG_ALLOWED_CHATS=@your_test_chat,123456789

# Conservative limits
TG_MAX_SEND_PER_HOUR=10
TG_MAX_SEND_PER_DAY=50
TG_READ_LIMIT_PER_RUN=500

# Optional operator identity for audit logs
TG_OPERATOR=local-agent
EOF
```

Создать настоящий `.env`:

```bash
cp .env.example .env
chmod 600 .env
```

Открыть и заполнить:

```bash
nano .env
```

Пример:

```text
TG_API_ID=12345678
TG_API_HASH=abcdef1234567890abcdef1234567890
TG_SESSION=./data/userbot-session
TG_SEND_ENABLED=false
TG_ALLOWED_CHATS=@my_test_group
TG_MAX_SEND_PER_HOUR=10
TG_MAX_SEND_PER_DAY=50
TG_READ_LIMIT_PER_RUN=500
TG_OPERATOR=alexey-agent
```

---

## 9. Минимальный код проекта

Ниже рабочий скелет. Его можно разнести по файлам.

### 9.1. `app/config.py`

```python
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    api_id: int
    api_hash: str
    session: Path
    send_enabled: bool
    allowed_chats: set[str]
    max_send_per_hour: int
    max_send_per_day: int
    read_limit_per_run: int
    operator: str


def load_settings() -> Settings:
    env_file = os.getenv("TG_ENV_FILE", ".env")
    load_dotenv(env_file)

    api_id_raw = os.getenv("TG_API_ID", "").strip()
    api_hash = os.getenv("TG_API_HASH", "").strip()
    if not api_id_raw or not api_hash:
        raise RuntimeError("Missing TG_API_ID/TG_API_HASH in .env")

    allowed = {
        x.strip() for x in os.getenv("TG_ALLOWED_CHATS", "").split(",") if x.strip()
    }

    return Settings(
        api_id=int(api_id_raw),
        api_hash=api_hash,
        session=Path(os.getenv("TG_SESSION", "./data/userbot-session")).expanduser(),
        send_enabled=os.getenv("TG_SEND_ENABLED", "false").lower() == "true",
        allowed_chats=allowed,
        max_send_per_hour=int(os.getenv("TG_MAX_SEND_PER_HOUR", "10")),
        max_send_per_day=int(os.getenv("TG_MAX_SEND_PER_DAY", "50")),
        read_limit_per_run=int(os.getenv("TG_READ_LIMIT_PER_RUN", "500")),
        operator=os.getenv("TG_OPERATOR", "local-agent"),
    )
```

### 9.2. `app/client.py`

```python
from __future__ import annotations

from telethon import TelegramClient
from .config import load_settings


def make_client() -> TelegramClient:
    s = load_settings()
    s.session.parent.mkdir(parents=True, exist_ok=True)
    return TelegramClient(str(s.session), s.api_id, s.api_hash)
```

### 9.3. `app/auth.py`

```python
from __future__ import annotations

import asyncio
import typer
from rich import print
from .client import make_client
from .config import load_settings

app = typer.Typer(no_args_is_help=True)


@app.command("login")
def login():
    """Interactive one-time login. Writes local .session file."""
    async def run():
        settings = load_settings()
        async with make_client() as client:
            ok = await client.is_user_authorized()
            print({"authorized": ok, "session": str(settings.session)})
        # Telethon asks phone/code/password automatically when needed via start().
    asyncio.run(run())


@app.command("start-login")
def start_login():
    """Login using Telethon start() prompt."""
    async def run():
        settings = load_settings()
        client = make_client()
        await client.start()
        ok = await client.is_user_authorized()
        print({"authorized": ok, "session": str(settings.session)})
        await client.disconnect()
    asyncio.run(run())


@app.command("status")
def status():
    async def run():
        async with make_client() as client:
            me = await client.get_me()
            print({
                "authorized": bool(me),
                "user_id": getattr(me, "id", None),
                "username": getattr(me, "username", None),
            })
    asyncio.run(run())


if __name__ == "__main__":
    app()
```

Первый вход:

```bash
python -m app.auth start-login
```

Telethon попросит:

- phone;
- login code from Telegram;
- 2FA password, если включён.

После входа:

```bash
chmod 600 data/*.session* 2>/dev/null || true
python -m app.auth status
```

### 9.4. `app/audit.py`

```python
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB = Path("./data/audit.sqlite")


def init_db():
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    con.execute(
        """
        create table if not exists audit_log (
            id integer primary key autoincrement,
            ts text not null,
            action text not null,
            target text,
            status text not null,
            detail text
        )
        """
    )
    con.commit()
    con.close()


def log_action(action: str, target: str, status: str, detail: str = ""):
    init_db()
    con = sqlite3.connect(DB)
    con.execute(
        "insert into audit_log(ts, action, target, status, detail) values (?, ?, ?, ?, ?)",
        (datetime.now(timezone.utc).isoformat(), action, target, status, detail[:1000]),
    )
    con.commit()
    con.close()
```

### 9.5. `app/read_tools.py`

```python
from __future__ import annotations

import asyncio
import json
import typer
from telethon.errors import FloodWaitError, RPCError
from .client import make_client
from .config import load_settings
from .audit import log_action

app = typer.Typer(no_args_is_help=True)


def compact_message(m):
    return {
        "id": m.id,
        "date": m.date.isoformat() if m.date else None,
        "sender_id": getattr(m, "sender_id", None),
        "text": (m.message or "")[:1000],
        "views": getattr(m, "views", None),
        "forwards": getattr(m, "forwards", None),
    }


@app.command("list-chats")
def list_chats(limit: int = 30):
    async def run():
        result = []
        async with make_client() as client:
            async for d in client.iter_dialogs(limit=limit):
                result.append({
                    "id": d.id,
                    "name": d.name,
                    "is_user": d.is_user,
                    "is_group": d.is_group,
                    "is_channel": d.is_channel,
                })
        log_action("list_chats", "", "ok", f"count={len(result)}")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    asyncio.run(run())


@app.command("get-messages")
def get_messages(target: str, limit: int = 20):
    async def run():
        settings = load_settings()
        limit2 = min(limit, settings.read_limit_per_run)
        result = []
        try:
            async with make_client() as client:
                async for m in client.iter_messages(target, limit=limit2):
                    result.append(compact_message(m))
            log_action("get_messages", target, "ok", f"count={len(result)}")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except FloodWaitError as e:
            log_action("get_messages", target, "flood_wait", str(e.seconds))
            raise typer.BadParameter(f"Telegram FloodWait: wait {e.seconds}s")
        except RPCError as e:
            log_action("get_messages", target, "rpc_error", str(e))
            raise typer.BadParameter(f"Telegram RPC error: {e}")
    asyncio.run(run())


@app.command("search-messages")
def search_messages(target: str, query: str, limit: int = 50):
    async def run():
        settings = load_settings()
        limit2 = min(limit, settings.read_limit_per_run)
        result = []
        async with make_client() as client:
            async for m in client.iter_messages(target, search=query, limit=limit2):
                result.append(compact_message(m))
        log_action("search_messages", target, "ok", f"query={query} count={len(result)}")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    asyncio.run(run())


if __name__ == "__main__":
    app()
```

### 9.6. `app/rate_limit.py`

```python
from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from .config import load_settings

DB = Path("./data/audit.sqlite")


def count_sends_since(since: datetime) -> int:
    if not DB.exists():
        return 0
    con = sqlite3.connect(DB)
    row = con.execute(
        "select count(*) from audit_log where action in ('send_message','send_file') and status='ok' and ts >= ?",
        (since.isoformat(),),
    ).fetchone()
    con.close()
    return int(row[0] or 0)


def check_send_limits():
    s = load_settings()
    now = datetime.now(timezone.utc)
    hour = count_sends_since(now - timedelta(hours=1))
    day = count_sends_since(now - timedelta(days=1))
    if hour >= s.max_send_per_hour:
        raise RuntimeError(f"Hourly send limit reached: {hour}/{s.max_send_per_hour}")
    if day >= s.max_send_per_day:
        raise RuntimeError(f"Daily send limit reached: {day}/{s.max_send_per_day}")
```

### 9.7. `app/send_tools.py`

```python
from __future__ import annotations

import asyncio
import random
import time
import typer
from pathlib import Path
from telethon.errors import FloodWaitError, RPCError
from .client import make_client
from .config import load_settings
from .audit import log_action
from .rate_limit import check_send_limits

app = typer.Typer(no_args_is_help=True)


def guard_target(target: str):
    s = load_settings()
    if not s.send_enabled:
        raise RuntimeError("Sending disabled. Set TG_SEND_ENABLED=true only after tests.")
    if target not in s.allowed_chats:
        raise RuntimeError(f"Target not allowed: {target}")
    check_send_limits()


@app.command("send-message")
def send_message(target: str, text: str):
    async def run():
        guard_target(target)
        time.sleep(random.uniform(2.0, 7.0))
        try:
            async with make_client() as client:
                msg = await client.send_message(target, text)
            log_action("send_message", target, "ok", f"message_id={msg.id}")
            print({"ok": True, "message_id": msg.id})
        except FloodWaitError as e:
            log_action("send_message", target, "flood_wait", str(e.seconds))
            raise typer.BadParameter(f"Telegram FloodWait: wait {e.seconds}s")
        except RPCError as e:
            log_action("send_message", target, "rpc_error", str(e))
            raise typer.BadParameter(f"Telegram RPC error: {e}")
    asyncio.run(run())


@app.command("send-file")
def send_file(target: str, file_path: str, caption: str = ""):
    async def run():
        guard_target(target)
        p = Path(file_path)
        if not p.exists() or not p.is_file():
            raise RuntimeError(f"File not found: {file_path}")
        time.sleep(random.uniform(2.0, 7.0))
        async with make_client() as client:
            msg = await client.send_file(target, str(p), caption=caption or None)
        log_action("send_file", target, "ok", f"message_id={msg.id} file={p.name}")
        print({"ok": True, "message_id": msg.id})
    asyncio.run(run())


if __name__ == "__main__":
    app()
```

---

## 10. Проверка установки без агента

### 10.1. Auth

```bash
cd ~/telegram-agent-userbot
. .venv/bin/activate
python -m app.auth start-login
python -m app.auth status
```

Ожидаемо:

```text
authorized: true
```

### 10.2. Read-only

```bash
python -m app.read_tools list-chats --limit 10
python -m app.read_tools get-messages @telegram --limit 5
python -m app.read_tools search-messages @telegram Telegram --limit 5
```

### 10.3. Send disabled test

```bash
python -m app.send_tools send-message @your_test_chat "test"
```

Ожидаемо:

```text
Sending disabled
```

Это хороший результат. Защита работает.

### 10.4. Send enabled only to test chat

В `.env`:

```text
TG_SEND_ENABLED=true
TG_ALLOWED_CHATS=@your_test_chat
```

Потом:

```bash
python -m app.send_tools send-message @your_test_chat "smoke test from Telethon userbot"
```

Если сообщение ушло — проверить audit:

```bash
sqlite3 data/audit.sqlite "select ts, action, target, status, detail from audit_log order by id desc limit 5;"
```

Вернуть безопасный режим:

```text
TG_SEND_ENABLED=false
```

---

## 11. MCP-сервер для агента

Задача MCP — дать агенту не полный Python, а безопасные команды.

### 11.1. Принцип

MCP server должен экспортировать tools:

```text
telegram_list_chats
telegram_get_messages
telegram_search_messages
telegram_send_message
telegram_send_file
```

Read tools можно включить сразу.

Send tools:

- видны агенту только если нужны;
- внутри всё равно проверяют `TG_SEND_ENABLED`;
- внутри всё равно проверяют `TG_ALLOWED_CHATS`;
- каждый вызов логируется;
- массовых циклов отправки нет.

### 11.2. Hermes native MCP config

Для Hermes профильный config:

```yaml
mcp_servers:
  telegram_userbot:
    command: "/Users/aleksejulanov/telegram-agent-userbot/.venv/bin/python"
    args: ["/Users/aleksejulanov/telegram-agent-userbot/app/mcp_server.py"]
    env:
      TG_ENV_FILE: "/Users/aleksejulanov/telegram-agent-userbot/.env"
    timeout: 120
    connect_timeout: 60
    sampling:
      enabled: false
```

Команды Hermes:

```bash
hermes --profile mike config edit
hermes --profile mike mcp list
hermes --profile mike mcp test telegram_userbot
```

После изменения MCP config нужен restart процесса агента/gateway, потому что MCP tools обнаруживаются на старте.

```bash
hermes --profile mike gateway restart
```

Если это другой профиль:

```bash
hermes --profile mike-lalo gateway restart
```

### 11.3. Почему `sampling.enabled: false`

Для Telegram userbot MCP server не нужен server-initiated LLM sampling.

Безопаснее так:

```yaml
sampling:
  enabled: false
```

Меньше неожиданных LLM-вызовов, меньше поверхностей риска.

---

## 12. Правила для AI-агента

Системное правило для агента, которому дали Telegram tools:

```text
Ты можешь читать только явно разрешённые чаты.
Ты не отправляешь сообщения без явного указания пользователя или заранее утверждённого сценария.
Ты не делаешь массовые рассылки.
Ты не обходишь лимиты Telegram.
Ты не вступаешь в чаты и не инвайтишь людей.
Перед отправкой в новый чат просишь approval.
Все черновики сначала показываешь человеку.
Если tool возвращает FloodWait или rate-limit — останавливаешься.
```

Для лидогенерации безопасный workflow:

```text
1. Найти публичные сигналы боли.
2. Составить список кандидатов/чатов.
3. Подготовить черновик сообщения.
4. Показать человеку.
5. Отправить только в allowlist и только после approval.
6. Записать факт отправки.
7. Остановиться на лимите.
```

---

## 13. LaunchAgent на macOS

Автозапуск нужен только после ручных тестов.

Для MCP stdio server отдельный daemon часто не нужен: Hermes сам запускает MCP process по `command/args`.

Но если делаем HTTP API service, тогда launchd.

Пример `~/Library/LaunchAgents/com.alexey.telegram-userbot-api.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
 "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.alexey.telegram-userbot-api</string>

  <key>ProgramArguments</key>
  <array>
    <string>/Users/aleksejulanov/telegram-agent-userbot/.venv/bin/python</string>
    <string>-m</string>
    <string>uvicorn</string>
    <string>app.http_api:app</string>
    <string>--host</string>
    <string>127.0.0.1</string>
    <string>--port</string>
    <string>8788</string>
  </array>

  <key>WorkingDirectory</key>
  <string>/Users/aleksejulanov/telegram-agent-userbot</string>

  <key>EnvironmentVariables</key>
  <dict>
    <key>TG_ENV_FILE</key>
    <string>/Users/aleksejulanov/telegram-agent-userbot/.env</string>
  </dict>

  <key>RunAtLoad</key>
  <true/>

  <key>KeepAlive</key>
  <true/>

  <key>StandardOutPath</key>
  <string>/Users/aleksejulanov/telegram-agent-userbot/logs/launchd.out.log</string>

  <key>StandardErrorPath</key>
  <string>/Users/aleksejulanov/telegram-agent-userbot/logs/launchd.err.log</string>
</dict>
</plist>
```

Загрузить:

```bash
launchctl load ~/Library/LaunchAgents/com.alexey.telegram-userbot-api.plist
launchctl list | grep telegram-userbot
```

Остановить:

```bash
launchctl unload ~/Library/LaunchAgents/com.alexey.telegram-userbot-api.plist
```

---

## 14. Systemd на Linux

Если сервер Linux:

```ini
[Unit]
Description=Telegram Userbot API
After=network-online.target

[Service]
Type=simple
WorkingDirectory=/home/agent/telegram-agent-userbot
Environment=TG_ENV_FILE=/home/agent/telegram-agent-userbot/.env
ExecStart=/home/agent/telegram-agent-userbot/.venv/bin/python -m uvicorn app.http_api:app --host 127.0.0.1 --port 8788
Restart=on-failure
RestartSec=5
User=agent
Group=agent

[Install]
WantedBy=multi-user.target
```

Команды:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now telegram-userbot-api
sudo systemctl status telegram-userbot-api
journalctl -u telegram-userbot-api -f
```

---

## 15. Troubleshooting

### `Missing TG_API_ID/TG_API_HASH`

Проверить:

```bash
pwd
ls -la .env
```

Если MCP запускает из другого cwd, укажи абсолютный env:

```yaml
env:
  TG_ENV_FILE: "/absolute/path/to/.env"
```

### `PhoneCodeInvalidError`

Код Telegram введён неверно или устарел. Запустить login заново.

### Запрашивает 2FA password

Это пароль облачной двухфакторной защиты Telegram. Его вводит человек руками при первом login. В `.env` не хранить.

### `FloodWaitError`

Telegram просит подождать. Не обходить.

Правильно:

```text
остановиться -> записать seconds -> повторить позже
```

Неправильно:

```text
создать новый аккаунт -> продолжить спам
```

### `ChatWriteForbiddenError`

Аккаунт не может писать в этот чат. Значит не может. Не обходить.

### `UsernameInvalidError` / `ValueError: Cannot find any entity`

Неверный username или аккаунт не имеет доступа.

Проверить:

```bash
python -m app.read_tools list-chats --limit 100
```

### Агент не видит MCP tools

Проверить:

```bash
hermes --profile mike mcp list
hermes --profile mike mcp test telegram_userbot
```

Потом restart gateway/profile.

### Сообщения не отправляются

Проверить `.env`:

```text
TG_SEND_ENABLED=true
TG_ALLOWED_CHATS=@your_test_chat
```

Проверить audit:

```bash
sqlite3 data/audit.sqlite "select * from audit_log order by id desc limit 10;"
```

---

## 16. Security checklist перед production

Перед тем как давать агенту Telegram tools:

- [ ] Используется отдельный Telegram-аккаунт, не основной личный.
- [ ] `.env` имеет права `600`.
- [ ] `data/` имеет права `700`.
- [ ] `*.session` не в git.
- [ ] `TG_SEND_ENABLED=false` по умолчанию.
- [ ] `TG_ALLOWED_CHATS` заполнен только тестовыми/разрешёнными чатами.
- [ ] Есть `audit.sqlite`.
- [ ] Есть лимиты per hour/per day.
- [ ] Нет mass-DM инструмента.
- [ ] Нет auto-join инструмента.
- [ ] Нет anti-ban логики.
- [ ] Агент обязан показывать черновик перед отправкой.
- [ ] FloodWait не обходится.
- [ ] Private chats читаются только по явному scope.

---

## 17. Сценарии использования

### Сценарий 1: market intelligence

Без отправки сообщений.

```text
list_chats -> search_messages -> export snippets -> summary -> Lalo packaging
```

Подходит для Lalo/Tuco.

### Сценарий 2: личный Telegram CRM

```text
get_messages from allowlisted chats -> classify -> draft reply -> human approval -> send
```

Подходит для Saul/Kaizen/Mike.

### Сценарий 3: поддержка клиентов

Лучше начать с Bot API, если клиенты сами пишут в бота.

Userbot нужен только если задача завязана на существующий пользовательский аккаунт и чаты.

### Сценарий 4: лидогенерация

Безопасная версия:

```text
public/allowed sources -> identify relevant public pain -> draft human message -> manual approval -> limited sends
```

Небезопасная версия:

```text
scrape private groups -> mass DM unknown people -> шаблонные офферы
```

Так не делать.

---

## 18. Что не ставить

Не использовать случайные GitHub-репозитории, если они обещают:

- `mass dm`;
- `auto join`;
- `anti ban`;
- `session string generator`;
- `scrape all members`;
- `invite all users`;
- `bypass limits`;
- cloud-hosted session без доверия.

Нормальная база:

- официальный Telethon: https://github.com/LonamiWebs/Telethon;
- собственный маленький controlled service;
- наш Lalo read-only collector как практический reference.

---

## 19. Рекомендуемый порядок внедрения у нас

1. Оставить Lalo collector read-only.
2. Создать отдельный `telegram-agent-userbot` repo/project.
3. Перенести туда чистую архитектуру: auth/read/send/audit/rate-limit/MCP.
4. Запустить с новым отдельным Telegram-аккаунтом.
5. Проверить read-only.
6. Проверить send disabled.
7. Добавить один тестовый allowlist-чат.
8. Отправить один smoke message.
9. Подключить MCP к нужному Hermes profile.
10. Добавить системное правило агенту: draft first, approval before send.
11. Только после этого — рабочие сценарии.

---

## 20. Быстрый “готово / не готово” тест

Система готова, если проходят команды:

```bash
cd ~/telegram-agent-userbot
. .venv/bin/activate
python -m app.auth status
python -m app.read_tools list-chats --limit 5
python -m app.read_tools get-messages @telegram --limit 3
python -m app.send_tools send-message @not_allowed_chat "test"
```

Последняя команда должна упасть с:

```text
Target not allowed
```

Потом тест в разрешённый чат:

```bash
python -m app.send_tools send-message @your_test_chat "controlled smoke test"
```

И audit:

```bash
sqlite3 data/audit.sqlite "select ts, action, target, status from audit_log order by id desc limit 5;"
```

Если всё это работает — база нормальная.

---

## 21. Финальная рекомендация

Для серьёзной работы не надо ставить “готовый лидоген-юзербот”. Надо собрать маленький контролируемый сервис на Telethon.

Лучший production path:

```text
Telethon official repo
  -> our controlled userbot service
  -> read-only first
  -> audit + limits
  -> guarded send tools
  -> MCP for agents
  -> human approval before outbound
```

Это дольше на один вечер, зато потом не будет пожара с аккаунтами, секретами и непонятными репами.

No half measures.

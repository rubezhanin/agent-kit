# AGENT.md - установка и настройка Telegram userbot-оператора

Этот файл можно дать AI-боту или техническому помощнику. Его задача - провести человека через установку и настройку Telegram userbot-оператора безопасно, без утечки секретов и без спама.

## Главная задача агента

Помоги пользователю установить и настроить Telegram userbot-оператора.

Результат в конце:

- проект создан в выбранной папке;
- Python-окружение работает;
- Telethon установлен;
- Telegram-аккаунт подключён через `api_id`, `api_hash` и код входа;
- секреты лежат только в локальном `.env` или `secrets.env`;
- есть список разрешённых людей и чатов;
- в личных сообщениях оператор отвечает только разрешённым людям;
- в группах оператор сначала делает черновик владельцу;
- ответ в группу уходит только после ручного подтверждения;
- есть логи и простая проверка, что всё живо.

## Жёсткие правила безопасности

1. Не проси пользователя присылать тебе `api_hash`, код входа, пароль 2FA, session-файл или содержимое `.env` в чат.
2. Если нужно проверить секреты - проси показать только факт наличия, не значение.
3. Не делай массовые рассылки.
4. Не включай автоматические ответы во всех группах.
5. Не включай cold DM - сообщения незнакомым людям.
6. Не делай auto-join в группы и каналы.
7. Не давай userbot-оператору права удалять, редактировать, форвардить или банить людей.
8. Для боевых групп используй режим: черновик -> личка владельцу -> ручное подтверждение -> отправка.
9. Перед изменением существующего проекта сделай backup файла, который меняешь.
10. В конце обязательно проверь работу через smoke-test.

## Как говорить с пользователем

Говори просто.

Не так:

> Инициализируем MTProto-клиент и валидируем конфигурационный слой.

А так:

> Сейчас подключим Telegram-аккаунт. Секреты в чат не отправляй. Вставляй их только в локальный файл на своём компьютере.

## Шаг 0. Сначала выясни окружение

Попроси пользователя ответить коротко:

1. Какая система: macOS, Linux, Windows или VPS?
2. Где создавать проект?
3. Есть ли Python 3.10+?
4. Есть ли отдельный Telegram-аккаунт под userbot?
5. Получены ли `api_id` и `api_hash` на странице `https://my.telegram.org/apps`?
6. Нужно работать только в личке, в группах или и там и там?
7. Кто владелец, которому отправлять черновики?

Если пользователь не знает - помоги проверить командами ниже.

## Шаг 1. Проверка Python

### macOS / Linux

```bash
python3 --version
which python3
```

Ожидаемо:

```text
Python 3.10.x или новее
```

Если Python старый или не найден - сначала помоги установить Python 3.10+.

### Windows PowerShell

```powershell
python --version
where python
```

## Шаг 2. Создание проекта

Попроси пользователя выбрать папку. Пример:

```bash
mkdir -p telegram-ai-operator
cd telegram-ai-operator
```

Создай структуру:

```bash
mkdir -p data logs
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
```

Для Windows PowerShell:

```powershell
mkdir telegram-ai-operator
cd telegram-ai-operator
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

## Шаг 3. Установка зависимостей

```bash
python -m pip install "telethon>=1.36,<2" python-dotenv
python -m pip freeze > requirements.txt
```

Проверка:

```bash
python - <<'PY'
import telethon
print('Telethon OK:', telethon.__version__)
PY
```

## Шаг 4. Файл секретов

Создай файл `data/secrets.env`.

Важно: значения ниже - placeholders. Пользователь должен вставить свои значения локально. В чат их не отправлять.

```env
TELEGRAM_API_ID=<your_api_id>
TELEGRAM_API_HASH=<your_api_hash>
TELEGRAM_PHONE=<your_phone_number>
OWNER_TELEGRAM_ID=<your_owner_user_id>
```

Права на файл на macOS/Linux:

```bash
chmod 600 data/secrets.env
```

Добавь `.gitignore`:

```gitignore
.venv/
data/*.env
data/*.session
data/*.session-journal
logs/*.log
```

## Шаг 5. Первый вход в Telegram

Создай файл `login_check.py`:

```python
import os
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv('data/secrets.env')

api_id = int(os.environ['TELEGRAM_API_ID'])
api_hash = os.environ['TELEGRAM_API_HASH']
phone = os.environ['TELEGRAM_PHONE']

client = TelegramClient('data/operator', api_id, api_hash)

async def main():
    await client.start(phone=phone)
    me = await client.get_me()
    print('Login OK')
    print('User ID:', me.id)
    print('Username:', me.username)

with client:
    client.loop.run_until_complete(main())
```

Запуск:

```bash
python login_check.py
```

Что сказать пользователю:

- Telegram пришлёт код входа.
- Код вводить только в локальном терминале.
- Если включена 2FA, Telethon спросит пароль. Вводить только в локальном терминале.
- Не присылать код и пароль в чат.

## Шаг 6. Настройка списка разрешённых

Создай `data/policy.json`:

```json
{
  "owner_id": 123456789,
  "allowed_private_users": [123456789],
  "allowed_groups": [],
  "group_mode": "draft_then_confirm",
  "test_group_auto_reply": false,
  "cold_dm_enabled": false,
  "mass_dm_enabled": false,
  "auto_join_enabled": false,
  "forward_enabled": false,
  "edit_delete_enabled": false,
  "admin_actions_enabled": false,
  "max_replies_per_hour": 10
}
```

Поясни пользователю:

- `owner_id` - Telegram ID владельца;
- `allowed_private_users` - кому можно отвечать в личке;
- `allowed_groups` - ID групп, где можно слушать сообщения;
- `group_mode: draft_then_confirm` - в группах сначала черновик владельцу;
- все опасные функции выключены.

Если пользователь не знает свой Telegram ID, помоги получить его через тестовый запуск или через системного бота вроде `@userinfobot`. Не проси присылать приватные данные сверх ID.

## Шаг 7. Минимальный listener

Создай `operator.py`:

```python
import asyncio
import hashlib
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from telethon import TelegramClient, events

BASE = Path(__file__).resolve().parent
DATA = BASE / 'data'
LOGS = BASE / 'logs'
LOGS.mkdir(exist_ok=True)

load_dotenv(DATA / 'secrets.env')

api_id = int(os.environ['TELEGRAM_API_ID'])
api_hash = os.environ['TELEGRAM_API_HASH']
owner_id = int(os.environ['OWNER_TELEGRAM_ID'])

policy = json.loads((DATA / 'policy.json').read_text(encoding='utf-8'))
client = TelegramClient(str(DATA / 'operator'), api_id, api_hash)

pending_file = DATA / 'pending_drafts.jsonl'
audit_file = DATA / 'audit.jsonl'


def log_event(event_type, payload):
    row = {
        'ts': int(time.time()),
        'event': event_type,
        **payload,
    }
    with audit_file.open('a', encoding='utf-8') as f:
        f.write(json.dumps(row, ensure_ascii=False) + '\n')


def short_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:12]


def make_draft(text):
    # Здесь позже можно подключить LLM/AI-агента.
    # Пока безопасная заглушка.
    return 'Черновик ответа: понял сообщение. Нужно ответить по делу и коротко.'


@client.on(events.NewMessage)
async def handler(event):
    sender = await event.get_sender()
    chat = await event.get_chat()

    sender_id = getattr(sender, 'id', None)
    chat_id = getattr(chat, 'id', None)
    text = event.raw_text or ''

    if not text.strip():
        return

    is_private = event.is_private
    is_group = event.is_group

    log_event('message_seen', {
        'chat_id': chat_id,
        'sender_id': sender_id,
        'is_private': is_private,
        'is_group': is_group,
        'text_hash': short_hash(text),
        'text_len': len(text),
    })

    if is_private:
        if sender_id not in policy.get('allowed_private_users', []):
            log_event('private_ignored_not_allowed', {'sender_id': sender_id})
            return

        reply = make_draft(text)
        await event.reply(reply)
        log_event('private_replied', {'sender_id': sender_id})
        return

    if is_group:
        if chat_id not in policy.get('allowed_groups', []):
            log_event('group_ignored_not_allowed', {'chat_id': chat_id})
            return

        draft_id = short_hash(str(time.time()) + text)
        draft = make_draft(text)
        row = {
            'draft_id': draft_id,
            'chat_id': chat_id,
            'reply_to_msg_id': event.id,
            'draft': draft,
            'created_at': int(time.time()),
        }
        with pending_file.open('a', encoding='utf-8') as f:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')

        await client.send_message(
            owner_id,
            f'Черновик для группы\nID: {draft_id}\n\n{draft}\n\nЧтобы отправить: ок {draft_id}'
        )
        log_event('group_draft_sent_to_owner', {'chat_id': chat_id, 'draft_id': draft_id})


@client.on(events.NewMessage(from_users=lambda u: getattr(u, 'id', None) == owner_id))
async def owner_commands(event):
    text = (event.raw_text or '').strip()
    if not text.startswith('ок '):
        return

    draft_id = text.split(maxsplit=1)[1].strip()

    if not pending_file.exists():
        await event.reply('Нет черновиков.')
        return

    rows = [json.loads(line) for line in pending_file.read_text(encoding='utf-8').splitlines() if line.strip()]
    match = next((r for r in rows if r.get('draft_id') == draft_id), None)

    if not match:
        await event.reply('Черновик не найден.')
        return

    await client.send_message(
        match['chat_id'],
        match['draft'],
        reply_to=match.get('reply_to_msg_id')
    )
    await event.reply(f'Отправлено: {draft_id}')
    log_event('draft_approved_and_sent', {'draft_id': draft_id, 'chat_id': match['chat_id']})


async def main():
    await client.start()
    print('Operator is running')
    await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
```

## Шаг 8. Первый запуск

```bash
python operator.py
```

Проверка:

1. Напиши userbot-аккаунту в личку с разрешённого аккаунта.
2. Ожидаемый результат: он отвечает короткой заглушкой.
3. Напиши с неразрешённого аккаунта.
4. Ожидаемый результат: он молчит.
5. Проверь лог:

```bash
tail -n 20 data/audit.jsonl
```

Если в группах ещё нет разрешённых ID - это нормально. Сначала проверь личку.

## Шаг 9. Добавление группы

Перед добавлением группы объясни риск:

- группа шумнее лички;
- автоответы в группе опаснее;
- безопасный режим - только черновики владельцу.

Как получить ID группы:

1. Добавь userbot-аккаунт в нужную группу вручную.
2. Напиши тестовое сообщение в группе.
3. Посмотри `data/audit.jsonl`.
4. Найди `chat_id`.
5. Добавь его в `allowed_groups` в `data/policy.json`.

Пример:

```json
"allowed_groups": [-1001234567890]
```

Перезапусти оператор.

Проверка:

1. Напиши сообщение в разрешённой группе.
2. Ожидаемый результат: в личку владельцу приходит черновик.
3. Владелец пишет userbot-аккаунту:

```text
ок <draft_id>
```

4. Ожидаемый результат: ответ уходит в группу.

## Шаг 10. Подключение AI-агента

Сначала добейся, чтобы работала безопасная заглушка.

Только потом меняй функцию `make_draft(text)`.

Правило:

- AI может готовить текст;
- AI не должен сам решать, кому писать;
- AI не должен обходить список разрешённых;
- AI не должен отправлять в группы без подтверждения.

Пример безопасной задачи для AI:

```text
Ты помогаешь написать короткий ответ в Telegram.
Ответь по делу, без продаж, без ссылок, без обещаний.
Если данных мало - предложи уточнить.
Исходное сообщение:
<message>
```

## Шаг 11. Постоянный запуск

Выбирай по системе.

### macOS

Самый простой вариант для новичка - сначала запускать вручную:

```bash
cd telegram-ai-operator
. .venv/bin/activate
python operator.py
```

Постоянный запуск через `launchd` делай только после успешного ручного теста.

Перед `launchd` проверь:

- абсолютный путь к Python внутри `.venv`;
- абсолютный путь к `operator.py`;
- права доступа к папке проекта;
- нет ли запрета macOS на доступ к папке Desktop/Documents/Downloads.

### Linux / VPS

После ручного теста можно сделать `systemd` service.

Не делай service, пока ручной запуск не прошёл.

## Частые ошибки

### Ошибка: код входа не приходит

Проверь:

- правильный номер телефона;
- Telegram не ограничил вход;
- нет частых повторных попыток.

Не проси код входа в чат.

### Ошибка: `api_id` или `api_hash` не работают

Проверь, что они взяты с `https://my.telegram.org/apps`.

Не проси показать `api_hash` полностью.

### Ошибка: аккаунт молчит в личке

Проверь:

- отправитель есть в `allowed_private_users`;
- `operator.py` запущен;
- нет исключений в терминале;
- `data/audit.jsonl` пополняется.

### Ошибка: в группе нет черновика

Проверь:

- группа есть в `allowed_groups`;
- userbot-аккаунт состоит в группе;
- сообщение не пустое;
- `chat_id` указан правильно;
- оператор перезапущен после изменения `policy.json`.

### Ошибка: страшно запускать в боевой группе

Правильно страшно.

Сначала:

1. тестовая группа;
2. один разрешённый чат;
3. только черновики;
4. низкий лимит ответов;
5. ручное подтверждение;
6. логирование.

## Минимальный smoke-test в конце

Сделай и покажи пользователю результат:

```bash
python -m py_compile operator.py login_check.py
python - <<'PY'
import json
from pathlib import Path
p = Path('data/policy.json')
json.loads(p.read_text(encoding='utf-8'))
print('policy.json OK')
PY
```

Потом проверь руками:

- разрешённая личка отвечает;
- неразрешённая личка игнорируется;
- группа создаёт черновик владельцу;
- `ок <draft_id>` отправляет ответ;
- `data/audit.jsonl` пишет события;
- секреты не попали в Git и чат.

## Что агент должен выдать в финале

В конце не пиши просто "готово".

Выдай короткий отчёт:

```text
Готово.

Что сделано:
- создан проект: <path>
- создано окружение Python
- установлен Telethon
- выполнен вход в Telegram
- настроен список разрешённых
- проверена личка
- проверены черновики для группы

Что не показывалось и не сохранялось в чат:
- api_hash
- код входа
- пароль 2FA
- session-файл
- secrets.env

Проверки:
- py_compile OK
- policy.json OK
- private allow OK
- private deny OK
- group draft OK
- manual confirmation OK

Осталось вручную:
- добавить нужные группы в allowed_groups
- подключить реальный AI вместо заглушки make_draft
- настроить постоянный запуск после стабильного ручного теста
```

## Запреты для агента

Не делай этого:

- не проси пользователя вставить секреты прямо в чат;
- не печатай содержимое `secrets.env`;
- не отправляй тестовые сообщения незнакомым людям;
- не включай автоответы во всех группах;
- не запускай массовые проверки по чатам;
- не коммить session-файлы;
- не заливай проект на GitHub вместе с `data/`;
- не обещай, что риска блокировки Telegram нет.

Правильная формулировка про риск:

> Риск не нулевой. Но если не спамить, не писать незнакомым, не делать массовые рассылки и держать группы через ручное подтверждение, риск заметно ниже.

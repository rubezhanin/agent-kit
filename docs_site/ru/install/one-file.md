# One-file installer

> Зеркало `docs/ONE_FILE_HERMES_KIT_INSTALLER.ru.md`. English — [here](../../en/install/one-file.md).

Дайте этот файл чистому Hermes-агенту. Агент проведёт владельца через установку в диалоговом режиме.

## Роль установщика

Агент — `setup-operator`. Алгоритм:

1. Discovery — сначала вопросы, не правки.
2. Dry-run plan — показать все изменения до применения.
3. Approval — получить явное согласие на пакет изменений.
4. Install — только после approval.
5. Smoke tests — прогнать `agent-center/templates/smoke-tests.md`.
6. Receipt — записать в `agent-center/reports/task-receipts/`.

## Что запрещено во время установки

- запрашивать токены, пароли, session-файлы или API-ключи в чате;
- писать в чужие директории;
- менять существующий конфиг Hermes без backup / diff / approval;
- включать Telegram / userbot / Telethon / TDLib без отдельного approval;
- обещать, что Telegram-аккаунт не забанят;
- считать, что Kanban / Curator уже доступны.

## Поток в одной схеме

```text
владелец
  │  "хочу установить kit"
  ▼
installer-agent
  │  discovery checklist
  ▼
dry-run plan
  │  approval владельца (approve minimal / full / discovery-only / change plan)
  ▼
install (one of: minimal / full / discovery-only / with-watcher)
  │  smoke tests
  ▼
финальный receipt (в reports/task-receipts/)
```

Полный диалоговый скрипт — в [`docs/ONE_FILE_HERMES_KIT_INSTALLER.ru.md`](https://github.com/your-org/hermes-agent-architecture-kit/blob/main/docs/ONE_FILE_HERMES_KIT_INSTALLER.ru.md) в репозитории.
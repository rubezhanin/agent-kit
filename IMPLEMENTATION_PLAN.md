# Implementation Plan

## Цель

Развернуть Hermes Agent систему с нуля как управляемый операционный контур:

- один главный оператор;
- ограниченный набор специалистов;
- wiki/source-of-truth;
- read-only retrieval;
- Kanban для длинных задач;
- safety/approval gates;
- receipts, audits и health checks.

## Phase 0. Discovery

Статус: planned.

Действия:

1. Проверить версию Hermes и доступные команды.
2. Проверить, есть ли Kanban, Curator, cron, skills и profile list.
3. Определить реальный `HERMES_HOME`.
4. Определить, как текущая версия Hermes подключает project skills.

Нельзя:

- включать Kanban по предположению;
- копировать YAML blueprint вслепую в runtime config;
- переносить секреты в Markdown.

## Phase 1. Minimal Main Profile

Статус: planned.

Действия:

1. Создать профиль `main-operator`.
2. Указать workspace на `kit/agent-center`.
3. Подключить `agent-center/AGENTS.md`.
4. Заполнить `owner-context/` минимальными правилами владельца.
5. Прогнать smoke test `Main Operator Triage`.

Критерий готовности:

- main operator корректно отличает простую задачу от задачи на делегацию;
- рискованные действия переводит в `NEEDS_APPROVAL`;
- не грузит все source-pack'и в контекст.

## Phase 2. Skills Layer

Статус: planned.

Действия:

1. Установить/подключить skills из `agent-center/skills/operations`.
2. Подключить активные specialist skills.
3. Оставить `psychological-support` disabled.
4. Проверить, что каждый skill открывает свой source-pack только при срабатывании.

Критерий готовности:

- `agent-creator`, `wiki-memory`, `kanban-operator`, `gateway-ux`, `token-drain`, `skill-hygiene` доступны;
- specialist routing работает через task brief.

## Phase 3. Knowledge Layer

Статус: planned.

Действия:

1. Создать/заполнить wiki: architecture, memory policy, roster, operating contract.
2. Добавить source cards для ключевых источников.
3. Настроить local memory index как read-only search, если нужен.
4. Запретить индексацию secrets, sessions, raw private logs.

Критерий готовности:

- агент ищет знания в wiki/references;
- retrieval не считается canonical truth;
- durable memory остаётся короткой.

## Phase 4. Kanban And Maintenance

Статус: planned.

Действия:

1. Проверить live `hermes kanban --help`.
2. Если доступно - включить board и dispatcher по `kanban/board-contract.md`.
3. Настроить read-only cron jobs из `config/cron-jobs.yaml`.
4. Включить weekly skill hygiene и token-drain diagnostics.

Критерий готовности:

- длинная задача создаётся как card;
- specialist возвращает receipt;
- cron пишет отчёты, но не меняет систему без approval.

## Phase 5. Gateway UX

Статус: planned.

Действия:

1. Проверить текущую схему Telegram/direct gateway.
2. Настроить ingress batching, если поддерживается.
3. Включить early ACK, partial streaming и final closure.
4. Запретить raw internal approval/tool blocks в user-facing ответах.

Критерий готовности:

- несколько быстрых сообщений и файл попадают в один turn;
- агент не молчит при длинной работе;
- каждая задача закрывается финальным ответом.

## Phase 6. Optional Integrations

Статус: hold.

Включать отдельно:

- Telethon/userbot;
- psychological-support profile;
- отдельный Codex CLI helper;
- browser/computer-use tools;
- внешние аккаунты.
- Telegram channel watcher.

Условие включения:

- отдельный risk review;
- least-privilege access;
- draft-only default;
- negative smoke tests;
- rollback/disable plan.

## Phase 7. Telegram Channel Intelligence

Статус: optional / hold.

Действия:

1. Researcher собирает кандидатов в `templates/telegram-channel-candidates.md`.
2. Владелец выбирает точные каналы.
3. Technical engineer проверяет watcher policy.
4. Для production выбрать TDLib; для прототипа можно Telethon.
5. Создать dedicated watcher account, не основной личный аккаунт.
6. Включить только read-only мониторинг.
7. Писать summaries в `integrations/telegram-channel-intelligence/reports/`.

Нельзя:

- массово подписываться;
- писать/комментировать/реагировать;
- собирать участников;
- обходить rate limits;
- хранить session files в repo/wiki;
- обещать, что бан невозможен.

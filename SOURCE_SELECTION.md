# Source Selection

## Перенесено в `kit/source`

| Группа | Файлы | Почему |
| --- | --- | --- |
| Core | `MAIN-AGENT-ARCHITECTURE-KIT.md`, `hermes-agent-setup-guide.md`, `ALL-IN-ONE-AGENT-STABILITY-KIT.md`, `context-management-guide.md`, `adaptive-agent-creator-kit.md` | Задают главный Hermes-контур: роль, workspace, memory, skills, delegation, context, создание новых агентов. |
| Memory/knowledge | `02-llm-wiki-hermes-obsidian-agent-setup.md`, `agent-user-local-embedding-brief-20260430 (2).md` | Нужны для wiki/source-of-truth и read-only retrieval слоя. |
| Operations | Kanban/Curator, token-drain, ingress batching, ACK/final closure, security, skill hygiene | Это эксплуатационный слой: задачи, UX, диагностика, безопасность, контроль skills. |
| Specialists | methodologist, designer, marketer, business analyst, researcher, technical engineer, Codex CLI, legal ops, economist, psychological support | Это agent/skill packs для профильных ролей. Часть включена как active, часть как optional. |
| Optional integrations | Telethon userbot setup и install-agent | Релевантно только если нужен Telegram userbot/MCP, но не включается по умолчанию из-за риска. |

## Оставлено в `files`

| Тип | Причина |
| --- | --- |
| PDF/аудио-курсы по context engineering, RAG, memory, workflow, security | Это обучающие и справочные материалы, не deploy-конфиги. |
| n8n JSON workflows (`TRENER`, `SOVETNIK`, `MARKETOLOG`, etc.) | Это n8n/OpenAI/Supabase/OpenClaw-like воркфлоу, не Hermes profile config. Несут риск смешать архитектуры. |
| OpenClaw/Claude setup и разборы | Полезны как идеи, но не должны становиться основой Hermes-сборки. |
| `MEMORY-UPGRADE new.md`, `БАЗОВЫЙ-ПАКЕТ-АГЕНТА.md` | Завязаны на OpenClaw-пути и небезопасные паттерны вроде запроса API ключа в чат. |
| ZIP/thumbnail/media | Не нужны для Hermes deploy kit. |

## Критерий отбора

Файл переносился, если он помогает:

- создать Hermes-профиль, skill, agent role или workspace;
- настроить память, wiki, retrieval, Kanban, cron/audit или gateway UX;
- задать безопасную роль специалиста;
- улучшить эксплуатацию и диагностику Hermes Agent.

Файл не переносился, если он:

- только обучает, но не конфигурирует;
- относится к другой платформе;
- содержит рискованные установки без Hermes-адаптации;
- дублирует уже выбранный MD-файл в PDF.


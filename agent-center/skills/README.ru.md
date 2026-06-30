# Индекс навыков (Russian)

> Русская локализация. Канонический английский — [`agent-center/skills/README.md`](agent-center/skills/README.md).

## Operations

| Skill | Path | Назначение |
| --- | --- | --- |
| `agent-creator` | `operations/agent-creator/SKILL.md` | Создание новых агентов / профилей / skills через audit, dry-run, approval. |
| `profile-factory` | `operations/profile-factory/SKILL.md` | Создание profile manifest и skill skeleton по описанию владельца. |
| `origin-return-protocol` | `operations/origin-return-protocol/SKILL.md` | Держит пять якорей (`origin` / `owner` / `artifact` / `status` / `return_path`) в каждой задаче; не ставит `DONE`, пока результат не вернулся в `return_path`. Первый слой агентской операционки. |
| `wiki-memory` | `operations/wiki-memory/SKILL.md` | Wiki, Obsidian-compatible knowledge base, memory index. |
| `kanban-operator` | `operations/kanban-operator/SKILL.md` | Kanban discovery, setup, routing, Curator. |
| `gateway-ux` | `operations/gateway-ux/SKILL.md` | Ingress batching, ACK, final closure, anti-leak UX. |
| `skill-hygiene-audit` | `operations/skill-hygiene-audit/SKILL.md` | Read-only аудит библиотеки skills. |
| `hermes-token-drain-diagnostic` | `operations/hermes-token-drain-diagnostic/SKILL.md` | Диагностика расхода токенов. |
| `telegram-channel-intelligence` | `operations/telegram-channel-intelligence/SKILL.md` | Подбор, approval, read-only мониторинг и анализ Telegram-каналов. |
| `carousel-creator` | `operations/carousel-creator/SKILL.md` | Опциональный brand carousel workflow поверх upstream `chatgpt-carousel-agent-kit`. |

## Specialists

| Skill | Path | Назначение |
| --- | --- | --- |
| `researcher` | `specialists/researcher/SKILL.md` | Public-source research, source ledger, фактчекинг. |
| `technical-engineer` | `specialists/technical-engineer/SKILL.md` | Setup, диагностика, ограниченные локальные правки. |
| `business-analyst` | `specialists/business-analyst/SKILL.md` | Process map, аудит автоматизации, дизайн пилота. |
| `methodologist` | `specialists/methodologist/SKILL.md` | Гайды, инструкции, обучающие материалы. |
| `marketer` | `specialists/marketer/SKILL.md` | Аудитория, оффер, proof bank, маркетинг. |
| `designer` | `specialists/designer/SKILL.md` | Visual brief, prompt pack, visual QA. |
| `legal-ops` | `specialists/legal-ops/SKILL.md` | Legal / risk / privacy review. |
| `economist` | `specialists/economist/SKILL.md` | ROI, pricing, подписки, paid pilot economics. |

## Optional

| Skill | Path | Назначение |
| --- | --- | --- |
| `psychological-support` | `optional/psychological-support/SKILL.md` | Disabled by default. Поддерживающая неклиническая беседа. |
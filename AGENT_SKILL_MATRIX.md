# Agent Skill Matrix

Здесь видно, какие агенты/профили какими навыками обладают в созданном kit.

Основные источники:

- `agent-center/config/profiles.yaml` - карта профилей и их назначение.
- `agent-center/wiki/team-roster.md` - человекочитаемый список ролей.
- `agent-center/skills/**/SKILL.md` - реальные skill-обёртки.

## Матрица

| Агент / профиль | Статус | Навыки / skills | Для чего |
| --- | --- | --- | --- |
| `main-operator` | active | `agent-creator`, `profile-factory`, `wiki-memory`, `kanban-operator`, `gateway-ux`, `skill-hygiene-audit`, `hermes-token-drain-diagnostic`, `telegram-channel-intelligence` | Приём задач, routing, установка, память, Kanban, диагностика, Telegram intelligence как управляемый контур. |
| `profile-factory` | active operations | `profile-factory`, `agent-creator` | Создание новых профилей и skills по описанию через intake, dry-run, approval и smoke tests. |
| `researcher` | active | `researcher`, `telegram-channel-intelligence` | Поиск источников, анализ публичных сигналов, подбор каналов, подготовка списка кандидатов для подписки/мониторинга. |
| `technical-engineer` | active | `technical-engineer`, `wiki-memory`, `hermes-token-drain-diagnostic` | Установка, диагностика, локальные изменения, smoke tests, receipts. |
| `business-analyst` | active | `business-analyst`, `researcher` as support | Process map, automation audit, pilot design, handoff в реализацию. |
| `methodologist` | active | `methodologist`, `wiki-memory` | Инструкции, гайды, курсы, agent-ready документы. |
| `marketer` | active | `marketer`, `researcher`, `legal-ops` as review | Аудитория, офферы, proof bank, безопасные маркетинговые эксперименты. |
| `designer` | active | `designer`, `marketer` as input | Visual brief, style pack, prompt pack, visual OTK. |
| `legal-ops` | active risk-review | `legal-ops` | Claims, privacy/data, vendor terms, договорные и AI-risk флаги. |
| `economist` | active risk-review | `economist` | ROI, pricing, подписки, paid pilot economics, бюджетные решения. |
| `agent-creator` | on-demand | `agent-creator` | Проектирование новых профилей, helper-agents и skills через dry-run/change packet. |
| `psychological-support` | disabled by default | `psychological-support` | Только отдельный безопасный support-профиль после явного включения. |
| `userbot/watcher` | disabled by default | `telegram-channel-intelligence` | Read-only Telegram channel watcher через TDLib/Telethon после отдельного approval. |

## Где смотреть в файловой структуре

```text
kit/
  AGENT_SKILL_MATRIX.md
  agent-center/
    profiles/
    config/
      profiles.yaml
    wiki/
      team-roster.md
    skills/
      operations/
      specialists/
      optional/
```

## Правило добавления нового skill

1. Создать `agent-center/skills/<group>/<skill-name>/SKILL.md`.
2. Добавить skill в `agent-center/config/profiles.yaml`.
3. Добавить строку в `agent-center/wiki/team-roster.md`, если skill меняет роль агента.
4. Обновить эту матрицу.
5. Прогнать smoke/negative smoke test.

Профили для автоматического подхвата установщиком лежат здесь:

```text
agent-center/profiles/*.profile.json
```

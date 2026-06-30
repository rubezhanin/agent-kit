---
hide:
  - navigation
---

# Hermes Agent Architecture Kit

> Русская локализация. English — [here](../en/index.md).

Манифестно-управляемый, консервативный стартовый комплект для развёртывания рабочего пространства Hermes Agent: профили, навыки, wiki, память, опциональный Kanban и слой read-only Telegram-разведки.

> [!IMPORTANT]
> Этот комплект **не** содержит сам runtime Hermes Agent. Установите Hermes отдельно (или передайте `--hermes-install-command`), затем укажите этому комплекту на рабочее пространство.

<div class="grid cards" markdown>

- :material-rocket-launch: __Быстрый старт__
    Склонировать, прогнать установщик, получить рабочий профиль `main-operator` за пять минут.
    [:octicons-arrow-right-24: Установка](install/index.md)

- :material-shield-lock: __Безопасность__
    Read-only по умолчанию, секреты только в `.env`, Telegram watcher выключен из коробки.
    [:octicons-arrow-right-24: Безопасность](architecture/index.md#безопасность-по-умолчанию)

- :material-source-branch: __Манифестно-управляемый__
    Добавить профиль — «положить JSON-файл», без правки кода.
    [:octicons-arrow-right-24: Архитектура](architecture/index.md)

</div>

## Что вы получаете

Установщик разворачивает Hermes-aware workspace с:

- профилем `main-operator` (intake, routing, финальный ответ, quality gate);
- командой специалистов (`researcher`, `technical-engineer`, `business-analyst`, `methodologist`, `marketer`, `designer`, `legal-ops`, `economist`);
- workspace `agent-center/` с `wiki/`, `references/`, `reports/`, `templates/`, `kanban/`, `prompts/`, `skills/`, `integrations/`;
- консервативными опциональными интеграциями (Telegram channel intelligence, brand carousel), выключенными до явного opt-in;
- install receipts в `reports/task-receipts/`.

## С чего начать

| Задача | Документ |
| --- | --- |
| Установить из свежего clone | [Установка](install/index.md) |
| Дать чистому Hermes-агенту диалоговый скрипт | [One-file installer](install/one-file.md) |
| Добавить новый профиль | [Добавление профилей](install/adding-profiles.md) |
| Понять архитектуру | [Архитектура](architecture/index.md) |
| Обзор «почему так» | [Обзор архитектуры](architecture/architecture-review.md) |
| Telegram channel watcher | [Telegram channel intelligence](integrations/telegram-channel-intelligence.md) |
| Brand carousel workflow | [Carousel creator](integrations/carousel-creator.md) |
| Кто каким навыком владеет | [Матрица агент × навык](reference/skill-matrix.md) |
| Что откуда перенесено | [Source selection](reference/source-selection.md) |
| Что нового в версиях | [Changelog](reference/changelog.md) |
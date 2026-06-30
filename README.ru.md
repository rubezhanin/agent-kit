# Hermes Agent Architecture Kit

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.4.0-blue.svg)](CHANGELOG.md)
[![CI](https://github.com/rubezhanin/agent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/rubezhanin/agent-kit/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-mkdocs--material-success)](https://rubezhanin.github.io/hermes-agent/)

[English version →](README.md)

Манифестно-управляемый, консервативный стартовый комплект для развёртывания рабочего пространства [Hermes Agent](https://github.com): профили, навыки, wiki, память, опциональный Kanban и слой read-only Telegram-разведки.

В комплект входит осторожный установщик, который **обнаруживает** профили из `agent-center/profiles/*.profile.json`, **никогда** не запрашивает секреты в чате и **никогда** не правит существующую конфигурацию Hermes без явного approval.

> [!IMPORTANT]
> Этот комплект **не** содержит сам runtime Hermes Agent. Установите Hermes отдельно (или передайте `--hermes-install-command`), затем укажите этому комплекту на рабочее пространство.

---

## Содержание

- [Зачем этот kit](#зачем-этот-kit)
- [Быстрый старт](#быстрый-старт)
- [Структура репозитория](#структура-репозитория)
- [Что устанавливается](#что-устанавливается)
- [Профили и навыки](#профили-и-навыки)
- [Опционально: Telegram channel intelligence](#опционально-telegram-channel-intelligence)
- [Конфигурация](#конфигурация)
- [Локализация](#локализация)
- [Безопасность по умолчанию](#безопасность-по-умолчанию)
- [Добавление новых профилей](#добавление-новых-профилей)
- [Документация](#документация)
- [Участие в проекте](#участие-в-проекте)
- [Лицензия](#лицензия)

---

## Зачем этот kit?

Большинство Hermes-сетапов стартуют с нуля в чате: вы собираете промпт, пишете пару навыков, склеиваете их с Kanban и надеетесь, что ничего не сломается. Этот kit даёт **скучный, консервативный дефолт**:

- Готовая команда агентов (`main-operator`, `researcher`, `technical-engineer`, `business-analyst`, `methodologist`, `marketer`, `designer`, `legal-ops`, `economist`).
- Чёткое разделение между *источником истины* (`wiki/`, `references/`, `owner-context/`) и *транзитным состоянием* (`reports/`, Kanban).
- Манифест, который установщик читает в рантайме — добавление профиля это «положил файл», а не «правлю код».
- Жёсткие safety-рельсы: режим записи — read-only по умолчанию, секреты не идут в чат, интеграции вроде Telegram watcher остаются выключенными, пока вы их сами не включите.

## Быстрый старт

### Linux / macOS

```bash
git clone https://github.com/rubezhanin/agent-kit hermes-agent
cd hermes-agent
sh ./install.sh
```

### Windows (PowerShell)

```powershell
git clone https://github.com/rubezhanin/agent-kit hermes-agent
cd hermes-agent
.\install.ps1
```

### Кросс-платформенный Python-вход (рекомендуется)

```bash
python scripts/setup_kit.py --dry-run   # посмотреть план
python scripts/setup_kit.py             # выполнить
```

Полезные флаги:

| Флаг | Описание |
| --- | --- |
| `--dry-run` | Печатает все действия, ничего не пишет. |
| `--yes` | Авто-подтверждение безопасных дефолтов (внешние эффекты всё равно спрашиваются). |
| `--workspace PATH` | Установить в указанную директорию. |
| `--hermes-home PATH` | Путь к Hermes (например, `~/.hermes`). |
| `--main-profile NAME` | Переопределить главный профиль (по умолчанию `main-operator`). |
| `--install-hermes` | Разрешить запуск команды установки Hermes. |
| `--hermes-install-command "..."` | Команда установки, если Hermes не найден. |
| `--include-disabled` | Показать также профили, выключенные по умолчанию. |

См. [`docs/GITHUB_INSTALL.ru.md`](docs/GITHUB_INSTALL.ru.md) для полного справочника и [`docs/ONE_FILE_HERMES_KIT_INSTALLER.ru.md`](docs/ONE_FILE_HERMES_KIT_INSTALLER.ru.md) для пошагового диалога установки.

## Структура репозитория

```
hermes-agent/
├── README.md                        # English (основной)
├── README.ru.md                     # этот файл
├── LICENSE                          # MIT
├── CHANGELOG.md
├── CONTRIBUTING.md
├── .env.example                     # шаблон локальной конфигурации
├── .gitignore
├── GITHUB_INSTALL.md                # EN-справочник установщика
├── docs/                            # локализованная длинная документация
│   ├── GITHUB_INSTALL.ru.md
│   ├── ONE_FILE_HERMES_KIT_INSTALLER.en.md
│   ├── ONE_FILE_HERMES_KIT_INSTALLER.ru.md
│   ├── ADDING_PROFILES.en.md
│   ├── ADDING_PROFILES.ru.md
│   ├── AGENT_SKILL_MATRIX.en.md
│   ├── AGENT_SKILL_MATRIX.ru.md
│   ├── ARCHITECTURE_REVIEW.en.md
│   ├── ARCHITECTURE_REVIEW.ru.md
│   ├── IMPLEMENTATION_PLAN.en.md
│   ├── IMPLEMENTATION_PLAN.ru.md
│   ├── SOURCE_SELECTION.en.md
│   └── SOURCE_SELECTION.ru.md
├── kit-manifest.json                # машиночитаемый манифест
├── install.ps1                      # Windows entry point
├── install.sh                       # POSIX entry point
├── scripts/
│   ├── setup_kit.py                 # канонический установщик
│   └── create_profile_skeleton.py   # помощник для новых профилей
├── agent-center/                    # рабочее пространство, которое ставится
│   ├── AGENTS.md                    # контракт главного оператора (EN)
│   ├── AGENTS.ru.md                 # русская локализация
│   ├── config/                      # blueprints профилей и команды
│   ├── profiles/                    # по JSON на профиль
│   ├── skills/                      # operations / specialists / optional
│   ├── wiki/                        # канонический source of truth
│   ├── prompts/                     # системные промпты
│   ├── templates/                   # формы receipt / task / smoke-test
│   ├── kanban/                      # контракт Kanban
│   ├── owner-context/               # приватные заметки владельца
│   ├── references/                  # длинные источники
│   ├── reports/                     # receipts / audits / health
│   └── integrations/
│       └── telegram-channel-intelligence/
└── source/                          # исходные MD-pack'и (только для справки)
```

## Что устанавливается

Установщик:

1. Читает `kit-manifest.json`.
2. Автоматически обнаруживает профили из `agent-center/profiles/*.profile.json` — добавить новый профиль можно просто положив файл, без правки кода установщика.
3. По желанию готовит workspace `agent-center` в указанной директории.
4. Сохраняет выбранные профили в `.hermes-kit/selected-profiles.json`.
5. Пишет таймстемпленный install-receipt в `reports/task-receipts/`.
6. Оставляет все опциональные интеграции выключенными, пока вы их сами не включите.

Установщик **не**:

- запрашивает секреты, токены или session-файлы в чате;
- бездумно правит существующий production-конфиг Hermes;
- включает Telegram watcher без отдельного approval;
- считает, что Kanban / Curator уже доступны — сначала проверка.

## Профили и навыки

Активны по умолчанию:

- `main-operator` — triage, routing, Kanban, quality gate, финальный ответ пользователю.
- `researcher` — публичные источники, source ledger, поиск Telegram-каналов.
- `technical-engineer` — setup, диагностика, ограниченные локальные правки.
- `business-analyst` — process map, аудит автоматизации, пилот.
- `methodologist` — гайды, курсы, упаковка знаний.
- `marketer` — аудитория, оффер, контент, безопасные эксперименты.
- `designer` — visual brief, prompt pack, visual QA.
- `legal-ops` — контракты, претензии, приватность, риск-обзор AI-вендоров.
- `economist` — ROI, ценообразование, бюджет, подписки.

Выключены по умолчанию (включаются явно):

- `psychological-support` — поддерживающая, неклиническая беседа.
- `telegram-channel-watcher` — read-only watcher одобренных каналов.
- `carousel-creator` — опциональная обёртка `chatgpt-carousel-agent-kit` для брендовых каруселей и GPT image prompts. См. `agent-center/integrations/carousel-creator/README.md`.

## Первый слой — Origin Return Protocol

Каждый активный профиль подгружает навык [`origin-return-protocol`](agent-center/skills/operations/origin-return-protocol/SKILL.md), чтобы контур держал пять якорей (`origin` / `owner` / `artifact` / `status` / `return_path`) и не ставил `DONE`, пока результат не вернулся в `return_path`. Полный текст протокола хранится в `agent-center/operations/origin-return-protocol/PROTOCOL.ru.md` (русский оригинал) и `PROTOCOL.en.md`. На сайте документации — `Архитектура → Origin Return Protocol`.

См. [`docs/AGENT_SKILL_MATRIX.ru.md`](docs/AGENT_SKILL_MATRIX.ru.md) и `agent-center/skills/README.md` для полной матрицы навыков.

## Опционально: Telegram channel intelligence

Выключено по умолчанию. Чтобы включить:

1. Определитесь, что хотите: researcher ищет кандидатов → владелец утверждает точные handles → выделенный watcher-аккаунт читает их в read-only.
2. Заполните секцию Telegram в `.env` (`HERMES_TELEGRAM_*`).
3. Запустите установщик с `--include-disabled` и явно включите профиль `telegram-channel-watcher`.
4. Утвердите точные handles **до** того, как watcher что-либо присоединит.

См. `agent-center/integrations/telegram-channel-intelligence/README.md` и `agent-center/config/watcher-policy.yaml`.

Kit не обещает «бан не прилетит». Автоматизация Telegram несёт встроенный риск — относитесь к ней как к выделенному консервативному watcher'у.

## Конфигурация

Все настройки лежат в `.env`. Начните с `.env.example`:

```bash
cp .env.example .env
$EDITOR .env
```

Установщик читает и `.env` (если есть), и явные CLI-флаги. CLI-флаги имеют приоритет. Полный список переменных — в `.env.example`.

## Локализация

- `README.md` — английский (основной, канонический).
- `README.ru.md` — этот файл.
- Длинные документы — в `docs/` с суффиксами `.en.md` / `.ru.md`.
- Source-of-truth (`agent-center/AGENTS.md`, `wiki/`, `prompts/`) — английский, с `.ru.md` рядом там, где это полезно.

Если заметили проблему перевода — откройте PR. Английская версия каноническая, русская — для удобства.

## Безопасность по умолчанию

- Режим по умолчанию — **read-only**. Запись, внешние вызовы, действия с аккаунтами, оплата и удаление требуют явного approval.
- Секреты не запрашиваются в чате. Они уходят в `.env` или во внешний secret manager.
- Telegram watcher никогда не использует основной аккаунт владельца.
- Установщик отказывается писать вне выбранного workspace, если `HERMES_KIT_LOCK_OUTSIDE_WORKSPACE=true`.
- `.gitignore` исключает `.env`, session-файлы, raw-кэши Telegram и весь вывод receipts / audits.

## Добавление новых профилей

Положите два файла в kit:

```text
agent-center/profiles/<profile-name>.profile.json
agent-center/skills/<group>/<profile-name>/SKILL.md
```

Установщик подхватит их при следующем запуске. См. [`docs/ADDING_PROFILES.ru.md`](docs/ADDING_PROFILES.ru.md).

## Документация

| Тема | English | Русский |
| --- | --- | --- |
| End-to-end архитектура | [`docs/ARCHITECTURE.en.md`](docs/ARCHITECTURE.en.md) | [`docs/ARCHITECTURE.ru.md`](docs/ARCHITECTURE.ru.md) |
| Справочник установщика | [`GITHUB_INSTALL.md`](GITHUB_INSTALL.md) | [`docs/GITHUB_INSTALL.ru.md`](docs/GITHUB_INSTALL.ru.md) |
| Диалог установки в один файл | [`docs/ONE_FILE_HERMES_KIT_INSTALLER.en.md`](docs/ONE_FILE_HERMES_KIT_INSTALLER.en.md) | [`docs/ONE_FILE_HERMES_KIT_INSTALLER.ru.md`](docs/ONE_FILE_HERMES_KIT_INSTALLER.ru.md) |
| Добавление профилей | [`docs/ADDING_PROFILES.en.md`](docs/ADDING_PROFILES.en.md) | [`docs/ADDING_PROFILES.ru.md`](docs/ADDING_PROFILES.ru.md) |
| Матрица агент × навык | [`docs/AGENT_SKILL_MATRIX.en.md`](docs/AGENT_SKILL_MATRIX.en.md) | [`docs/AGENT_SKILL_MATRIX.ru.md`](docs/AGENT_SKILL_MATRIX.ru.md) |
| Обзор архитектуры | [`docs/ARCHITECTURE_REVIEW.en.md`](docs/ARCHITECTURE_REVIEW.en.md) | [`docs/ARCHITECTURE_REVIEW.ru.md`](docs/ARCHITECTURE_REVIEW.ru.md) |
| План реализации | [`docs/IMPLEMENTATION_PLAN.en.md`](docs/IMPLEMENTATION_PLAN.en.md) | [`docs/IMPLEMENTATION_PLAN.ru.md`](docs/IMPLEMENTATION_PLAN.ru.md) |
| Лог выбора источников | [`docs/SOURCE_SELECTION.en.md`](docs/SOURCE_SELECTION.en.md) | [`docs/SOURCE_SELECTION.ru.md`](docs/SOURCE_SELECTION.ru.md) |

## Участие в проекте

См. [`CONTRIBUTING.md`](CONTRIBUTING.md). Держите PR маленькими — один профиль / навык / документ на PR, прогоняйте `python scripts/setup_kit.py --dry-run` перед отправкой.

## Лицензия

[MIT](LICENSE). Полный текст — в файле `LICENSE`.
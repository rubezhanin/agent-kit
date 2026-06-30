---
title: "Грамотная настройка Hermes-агента: слой поверх стандартной установки"
author: "Mike/Hermes contour"
date: "2026-04-29"
lang: ru-RU
---

# Грамотная настройка Hermes-агента

Коротко: стандартная установка Hermes даёт движок. Рабочий агент появляется только после настройки контура: границ, памяти, процедур, проверок, маршрутизации и отчётности.

Этот документ описывает практический слой, который стоит добавить поверх базового Hermes, если человек хочет не просто чат-бота, а надёжного персонального оператора.

## 1. Что уже даёт стандартный Hermes

Базовый Hermes полезен сам по себе:

- CLI-агент с tool calling.
- Подключение разных LLM providers.
- Gateway в мессенджеры: Telegram, Discord, Slack и другие.
- Profiles: отдельные агенты с разными конфигами.
- Skills: повторяемые процедуры.
- Persistent memory.
- Cron jobs.
- Webhooks и MCP.
- File, terminal, browser, web, vision и другие toolsets.

Но это ещё не рабочий контур. Это набор возможностей.

## 2. Что нужно добавить, чтобы агент стал надёжным

Минимальный взрослый слой:

1. **Ясная роль агента** — кто он, что решает, что не трогает.
2. **Рабочий корень** — отдельная директория, где живут wiki, reports, references, scripts и data.
3. **Границы доступа** — запрет на чужие проекты, старые контуры и приватные зоны без явного разрешения.
4. **Source-of-truth layering** — разные типы знания лежат в разных слоях, а не в одной куче.
5. **Гигиена памяти** — durable memory не должна быть task log.
6. **Skills как procedural memory** — сложные проверенные workflows сохраняются как процедуры.
7. **Readiness/health checks** — агент должен уметь проверять себя, а не только отвечать.
8. **Scheduled maintenance** — cron-задачи для health, audit, worklog, daily drafts.
9. **Privacy model** — какие данные можно отдавать команде, какие остаются у владельца или профильного агента.
10. **Quality gate** — перед финальным ответом проверять факты, формат, риски и побочные эффекты.
11. **Отчётный след** — важные действия оставляют файл: report, decision log, audit или runbook.
12. **Rollback/quarantine** — спорные данные не удаляются вслепую, а изолируются с возможностью отката.

## 3. Что интересного есть в нашем контуре помимо wiki и команды

### 3.1. Чистое разделение контура

У агента должен быть свой рабочий центр, например:

```text
~/AgentCenter/
  wiki/
  references/
  owner-context/
  reports/
  scripts/
  data/
  memory-index/
```

Правило: агент не считает чужие директории своей памятью. Старые проекты, миграционные источники и архивы могут использоваться только как reference по явному запросу.

Зачем это нужно: иначе агент начинает смешивать историю, чужие роли, старые инструкции и текущую реальность.

### 3.2. Слои источников правды

Нельзя всё складывать в memory. Нормальная схема:

| Слой | Для чего |
|---|---|
| `wiki/` | стабильная структурированная база знаний |
| `references/` | длинные документы и источники |
| `owner-context/` | приватный контекст владельца |
| `skills/` | проверенные процедуры и workflows |
| durable memory | короткие устойчивые факты и предпочтения |
| session search | поиск по прошлым разговорам |
| reports | след выполненных проверок и аудитов |

Главный принцип: memory короткая, wiki структурная, skills процедурные, reports доказательные.

### 3.3. Локальный memory index

Поверх wiki/references/owner-context можно держать локальный read-only retrieval index:

- SQLite;
- FTS5;
- embeddings;
- atomic rebuild;
- guard против индексации чужих roots;
- secret scan;
- benchmark queries.

Это даёт агенту быстрый поиск по своей базе без превращения durable memory в мусорную свалку.

### 3.4. Memory hygiene

Durable memory должна хранить только то, что пригодится через месяц:

- устойчивые предпочтения пользователя;
- стабильные environment pointers;
- коррекции, которые предотвращают повторные ошибки;
- короткие факты о важных компонентах.

Не хранить:

- task progress;
- временные todo;
- большие отчёты;
- сырые логи;
- факты, которые легко найти в файлах.

### 3.5. Readiness guard

У агента должен быть минимальный self-check:

- рабочий центр существует;
- wiki/references/owner-context доступны;
- profile cwd указывает в правильный root;
- memory index проходит verify;
- forbidden roots не используются;
- gateway жив;
- cron jobs активны;
- health report создаётся.

Без этого агент может красиво отвечать и быть сломанным внутри.

### 3.6. Cron-контур

Полезные scheduled jobs:

- ежедневный health check;
- вечерний расширенный check;
- weekly skills audit;
- rolling daily worklog;
- staged daily-note drafts;
- watchdog для внешних runtime-интеграций.

Цель: не ждать, пока пользователь заметит поломку.

### 3.7. Skills как инженерная память

Skill — это не заметка. Это инструкция, которую агент обязан загрузить перед похожей задачей.

Хороший skill содержит:

- когда использовать;
- точные команды;
- ограничения;
- pitfalls;
- verification steps;
- rollback;
- примеры успешного результата.

Это превращает разовые победы в повторяемую способность.

### 3.8. Профили и роли

Один агент может быть диспетчером. Другие профили — specialist lanes:

- finance;
- research;
- technical reliability;
- legal/document review;
- psychological support;
- marketing intelligence;
- knowledge management.

Важно: каждый профиль должен иметь свой cwd, роль, privacy rules и список skills. Иначе это не команда, а набор масок.

### 3.9. Privacy levels

Нужна простая схема приватности:

| Уровень | Значение |
|---|---|
| `public-team` | можно передавать всем профильным агентам |
| `private-meta` | только краткий статус без сырого личного контекста |
| `private-owner-only` | только владелец и главный агент |
| `finance-private` | финансы только владельцу и finance-агенту |
| `support-private` | личные психологические темы не уходят в общий контур |

Без этого multi-agent контур быстро превращается в утечку контекста.

### 3.10. Specialist tools

Поверх Hermes можно добавлять локальные инструменты под роли:

- read-only Telegram/Telethon userbot для market intelligence;
- finance scanners для подписок и расходов;
- repo/watchlist scanners для research;
- health scripts для runtime;
- publishing pipeline для MD/PDF/Slides;
- local OCR/document extraction;
- browser automation для проверок.

Правило: секреты отдельно, session files отдельно, права `600`, no hardcoded credentials, no active dependency на legacy roots.

### 3.11. Quality gate

Перед финальным ответом агент проверяет:

1. это правда;
2. это опирается на живые проверки или явно указанные источники;
3. нет секретов и приватных данных;
4. ответ подходит формату пользователя;
5. если были изменения — есть проверка результата;
6. если был риск — он назван;
7. если нужен файл — файл реально создан.

### 3.12. Отчёты, а не только ответы

Хороший агент оставляет след:

```text
reports/
  health/
  extended-health/
  skills-audit/
  team-audit/
  public/
  incidents/
```

Чат — это поверхность. Reports — это память операции.

## 4. Что можно дать людям как шаблон

Для публичного распространения стоит давать не приватный контур, а шаблон:

```text
AgentCenter/
  AGENTS.md
  wiki/
    index.md
    SCHEMA.md
    team/
      current-roster.md
      operating-contract.md
  references/
  owner-context/
    README.md
  reports/
    health/
    audits/
  scripts/
    health_check.py
  memory-index/
  skills/
    quality-check/
    memory-hygiene/
    publishing-stack/
```

Плюс короткий setup checklist.

## 5. Setup checklist для человека

### Шаг 1. Поставить Hermes

```bash
hermes setup
hermes doctor
```

Настроить model provider, terminal backend, gateway и нужные toolsets.

### Шаг 2. Создать рабочий центр

```bash
mkdir -p ~/AgentCenter/{wiki,references,owner-context,reports,scripts,data,memory-index}
```

### Шаг 3. Зафиксировать роль агента

Создать `AGENTS.md`:

```text
Ты — [роль].
Твой рабочий root: ~/AgentCenter.
Не читать и не менять внешние проекты без явной просьбы.
Секреты не печатать.
Перед опасными действиями назвать риск и обратимость.
Финальные ответы короткие: вывод, факты, следующий шаг.
```

### Шаг 4. Разделить знания по слоям

- durable memory — только короткие устойчивые факты;
- wiki — стабильные знания;
- references — длинные источники;
- skills — процедуры;
- reports — доказательства выполненной работы.

### Шаг 5. Настроить skills

Минимальный набор:

- memory hygiene;
- quality check;
- health check;
- publishing stack;
- debugging workflow;
- boundary/separation rules;
- role-specific procedures.

### Шаг 6. Настроить health check

Минимальная проверка:

- нужные директории существуют;
- config cwd правильный;
- forbidden roots не используются;
- secrets не лежат в wiki/reports;
- gateway запущен;
- cron jobs активны;
- последний report PASS.

### Шаг 7. Настроить cron

```bash
hermes cron create '0 9 * * *'
hermes cron create '50 23 * * *'
```

Один job — лёгкий утренний health. Второй — вечерний расширенный audit.

### Шаг 8. Настроить публичный след

Каждый важный фикс или аудит должен оставлять файл:

```text
reports/<type>/<date>-<topic>.md
```

Внутри:

- цель;
- что проверено;
- что изменено;
- чем подтверждено;
- риски;
- следующий шаг.

## 6. Чем наш контур отличается от обычной установки

Коротко:

| Обычный Hermes | Настроенный операторский контур |
|---|---|
| агент с tools | агент с границами и ответственностью |
| memory есть | memory очищена и не используется как лог |
| skills есть | skills поддерживаются как процедурная база |
| profiles есть | profiles имеют роли, cwd, privacy и handoff rules |
| cron есть | cron используется для self-maintenance |
| gateway есть | gateway вписан в правила ответа и доставки |
| wiki можно сделать | wiki является source-of-truth, не свалкой |
| можно запускать команды | есть readiness guard, audit и rollback discipline |
| можно отвечать в чат | есть reports, decision logs и проверяемый след |

## 7. Самая короткая формула

Чтобы грамотно настроить себе такого агента, человеку нужны не только модель и Telegram-бот.

Ему нужны:

1. роль;
2. границы;
3. рабочий root;
4. wiki schema;
5. memory hygiene;
6. skills;
7. local retrieval;
8. health checks;
9. cron maintenance;
10. privacy rules;
11. reports;
12. quality gate;
13. rollback/quarantine policy;
14. specialist integrations под реальные задачи.

Тогда Hermes становится не игрушкой, а рабочим внешним оператором.

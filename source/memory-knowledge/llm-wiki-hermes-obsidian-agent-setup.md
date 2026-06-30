# Инструкция для Hermes-агента: настрой LLM Wiki + Obsidian

Эту инструкцию можно дать Hermes-агенту пользователя. Цель — создать переносимую Markdown-wiki, которую человек читает в Obsidian, а агент поддерживает как долговременную базу знаний.

Основа идеи: Andrej Karpathy, **LLM Wiki**  
https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f


---

## 0. Важное уточнение: это не дефолт Hermes

Эта система не включена в Hermes автоматически.

Hermes обычно умеет работать с файлами, Markdown, tools, memory и skills. Но LLM Wiki с Obsidian — это отдельная архитектура, которую нужно создать:

- папки;
- `SCHEMA.md`;
- `index.md`;
- `log.md`;
- правила обновления;
- запрет на секреты;
- decision log;
- optional semantic/retrieval index;
- Obsidian vault для человека.

Твоя задача как агента — развернуть эту надстройку безопасно и понятно.

---

## 1. Твоя роль

Ты Hermes-агент, который помогает пользователю построить личную или проектную **LLM Wiki**.

Ты не просто отвечаешь в чате. Ты поддерживаешь долговременный слой знаний:

- читаешь исходники;
- выделяешь устойчивые факты;
- обновляешь Markdown-страницы;
- поддерживаешь индекс;
- ведёшь лог изменений;
- проверяешь качество wiki;
- не сохраняешь секреты и случайный мусор.

Главный принцип: **wiki — источник правды; поиск, embeddings и semantic memory — производные слои.**

---

## 2. Что нужно создать

Создай рабочую папку, например:

```text
~/HermesWiki/
  README.md
  sources/
    inbox/
    processed/
  wiki/
    index.md
    SCHEMA.md
    log.md
    entities/
    concepts/
    projects/
    decisions/
    procedures/
  references/
  owner-context/
  reports/
  artifacts/
```

Назначение папок:

| Папка | Назначение |
|---|---|
| `sources/` | сырые материалы: заметки, расшифровки, документы, ссылки |
| `wiki/` | чистая долговременная база знаний |
| `references/` | справочные материалы и внешние документы |
| `owner-context/` | устойчивый контекст пользователя: цели, принципы, предпочтения |
| `reports/` | отчёты агента о проделанной работе |
| `artifacts/` | итоговые файлы: PDF, таблицы, схемы, выгрузки |

Не смешивай эти слои.

---

## 3. Создай `README.md`

Файл: `~/HermesWiki/README.md`

```md
# HermesWiki

Локальная LLM Wiki пользователя.

## Слои

- `sources/` — сырые входные материалы.
- `wiki/` — долговременная Markdown-база знаний.
- `references/` — справочные материалы.
- `owner-context/` — устойчивый контекст пользователя.
- `reports/` — отчёты агента.
- `artifacts/` — итоговые документы и выгрузки.

## Правило

Wiki редактируется агентом аккуратно: через схему, индекс, лог и проверку качества.
Секреты, ключи доступа, пароли и приватные одноразовые данные в wiki не сохраняются.
```

---

## 4. Создай `wiki/SCHEMA.md`

Файл: `~/HermesWiki/wiki/SCHEMA.md`

```md
---
title: Wiki Schema
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: schema
tags: [wiki, schema]
sources: []
confidence: high
---

# Wiki Schema

## Domain

Эта wiki хранит долговременное знание пользователя и его проектов.

## Layers

1. Raw sources — неизменяемые входные материалы.
2. Wiki — очищенный долговременный слой знания.
3. Index — навигация по wiki.
4. Log — история изменений.
5. Reports — оперативные отчёты агента.
6. Semantic memory — производный retrieval-слой, если он настроен.
7. Skills — процедурная память: как выполнять повторяемые задачи.

## Page types

- `entity` — человек, организация, продукт, система.
- `concept` — идея, принцип, модель, термин.
- `project` — проект или направление.
- `decision` — принятое решение.
- `procedure` — повторяемый процесс.
- `index` — навигация.
- `log` — история изменений.
- `schema` — правила wiki.

## Required frontmatter

Каждая durable-страница в `wiki/` должна иметь YAML frontmatter:

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | project | decision | procedure | index | log | schema
tags: []
sources: []
confidence: high | medium | low
---
```

## Update policy

Перед изменением wiki агент должен:

1. определить источник факта;
2. понять, является ли факт долговременным;
3. найти подходящую страницу;
4. обновить страницу минимальным точным изменением;
5. обновить `index.md`, если появилась новая страница;
6. добавить запись в `log.md`;
7. сообщить пользователю краткий diff/summary.

## Privacy policy

В wiki нельзя сохранять:

- пароли;
- ключи доступа;
- приватные одноразовые коды;
- платёжные данные;
- случайные фрагменты переписки без явной ценности;
- медицинские, юридические и финансовые выводы без указания источника и уровня уверенности.
```

---

## 5. Создай `wiki/index.md`

Файл: `~/HermesWiki/wiki/index.md`

```md
---
title: Wiki Index
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: index
tags: [wiki, index]
sources: []
confidence: high
---

# Wiki Index

## Core

- [[SCHEMA]] — правила wiki.
- [[log]] — история изменений.

## Entities

Пока пусто.

## Concepts

Пока пусто.

## Projects

Пока пусто.

## Decisions

Пока пусто.

## Procedures

Пока пусто.
```

---

## 6. Создай `wiki/log.md`

Файл: `~/HermesWiki/wiki/log.md`

```md
---
title: Wiki Log
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: log
tags: [wiki, log]
sources: []
confidence: high
---

# Wiki Log

## YYYY-MM-DD create | Initial LLM Wiki setup

- Created base folder structure.
- Created `SCHEMA.md`.
- Created `index.md`.
- Created `log.md`.
- Raw sources are separated from durable wiki pages.
- Secret storage is forbidden.
```

---

## 7. Первый запуск: что спросить у пользователя

Перед наполнением wiki задай короткие вопросы:

1. Для чего wiki: личная память, бизнес, обучение, проекты, команда?
2. Какие 3–7 главных доменов знаний надо хранить?
3. Где лежат исходники: Obsidian vault, Google Docs, Telegram exports, локальные файлы, Notion, GitHub?
4. Что нельзя сохранять ни при каких условиях?
5. Какой режим подтверждения нужен: авто-draft, diff-before-write или только read-only?
6. Нужны ли ежедневные/еженедельные отчёты?

Если пользователь не отвечает подробно — начни с безопасного минимума: `sources/`, `wiki/`, `SCHEMA.md`, `index.md`, `log.md`.

---

## 8. Правила обработки источников

Когда пользователь даёт материал:

1. Сохрани исходник в `sources/inbox/` или укажи ссылку на него.
2. Не переписывай исходник.
3. Выдели только устойчивые факты, решения, понятия и процедуры.
4. Определи целевые страницы в `wiki/`.
5. Если страницы нет — создай её с frontmatter.
6. Если страница есть — обнови только нужный раздел.
7. Обнови `index.md`.
8. Добавь запись в `log.md`.
9. Напиши пользователю кратко:
   - что прочитал;
   - какие страницы создал/обновил;
   - что требует проверки;
   - какие следующие 3 шага полезны.

---

## 9. Шаблон durable-страницы

```md
---
title: Название страницы
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: concept
tags: [example]
sources:
  - sources/inbox/example.md
confidence: medium
---

# Название страницы

## Коротко

1–3 предложения: что это и зачем важно.

## Что известно

- Факт 1.
- Факт 2.
- Факт 3.

## Связи

- [[related-page]]

## Открытые вопросы

- Что нужно проверить позже?
```

---

## 10. Decision log

Решения нельзя прятать в длинных заметках. Для каждого важного решения создавай файл:

```text
wiki/decisions/YYYY-MM-DD-short-title.md
```

Шаблон:

```md
---
title: Короткое название решения
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: decision
tags: [decision]
sources: []
confidence: high
---

# Короткое название решения

## Решение

Что решили.

## Контекст

Почему вопрос возник.

## Варианты

- Вариант A.
- Вариант B.

## Причина выбора

Почему выбран этот вариант.

## Последствия

Что изменится.

## Когда пересмотреть

Дата или условие пересмотра.
```

---

## 11. Obsidian

Obsidian используется как удобный интерфейс к Markdown-файлам.

Настройка:

1. Открой Obsidian.
2. `Open folder as vault`.
3. Выбери `~/HermesWiki/wiki` или весь `~/HermesWiki`.
4. Включи backlinks и graph view.
5. Не ставь плагины, которые автоматически меняют файлы, пока структура не стабилизирована.

Правило: Obsidian — reader/IDE для человека. Hermes — maintainer/editor для порядка. Markdown — переносимый формат.

---

## 12. Semantic memory / embeddings

Если у пользователя есть LanceDB, SQLite FTS, vector DB или другой retrieval-слой:

- индексируй `wiki/`, `references/`, `owner-context/`;
- не делай embeddings источником правды;
- rebuild должен быть воспроизводимым из Markdown-файлов;
- если retrieval противоречит wiki — верь wiki, потом перестрой индекс;
- перед индексированием запускай secret scan.

Минимальная проверка retrieval:

```text
1. Сколько документов проиндексировано?
2. Какие source roots используются?
3. Нет ли старых/чужих папок?
4. Находит ли поиск ключевые страницы?
5. Можно ли полностью перестроить индекс из wiki?
```

---

## 13. Skills как процедурная память

Wiki хранит факты и знания. Skills хранят **как делать повторяемую работу**.

Создавай skill, если:

- задача повторяется;
- есть точные шаги;
- есть ошибки и обходные пути;
- важно не забыть порядок действий;
- процедура полезна через месяц.

Не сохраняй в skill временный прогресс конкретной задачи. Это идёт в reports или task status.

---

## 14. Dashboard и task status

Для оперативного слоя создай файл:

```text
reports/daily/YYYY-MM-DD.md
```

Шаблон:

```md
# Daily Agent Report — YYYY-MM-DD

## Active tasks

- [ ] Задача 1.
- [ ] Задача 2.

## Done

- Что сделано.

## Artifacts

- Путь к файлу.

## Blockers

- Что мешает.

## Handoff

- Что должен знать следующий агент/следующая сессия.
```

Этот слой не заменяет wiki. Он нужен для текущей работы и передачи состояния.

---

## 15. Health check wiki

После создания и после крупных обновлений проверь:

```text
Wiki health check:
- `SCHEMA.md` есть;
- `index.md` есть;
- `log.md` есть;
- все durable-страницы имеют YAML frontmatter;
- все durable-страницы есть в index;
- новые решения лежат в `decisions/`;
- raw sources не переписаны;
- секреты не сохранены;
- нет битых wikilinks;
- есть краткий отчёт пользователю.
```

---

## 16. Команда, которую можно выполнить сразу

Сначала покажи пользователю план. Потом создай структуру.

```text
Я создам локальную LLM Wiki в `~/HermesWiki`:
- raw sources отдельно;
- durable wiki отдельно;
- schema/index/log;
- decision log;
- reports/handoff;
- правила для Obsidian;
- запрет на секреты;
- health check.

После создания отдам список файлов и предложу первый ingest.
```

---

## 17. Финальный отчёт пользователю

После настройки ответь коротко:

```text
Готово.

Создано:
- ~/HermesWiki/wiki/SCHEMA.md
- ~/HermesWiki/wiki/index.md
- ~/HermesWiki/wiki/log.md
- базовые папки для sources/wiki/reports/artifacts

Правила:
- wiki = source of truth;
- sources не переписываются;
- semantic memory производная;
- решения идут в decisions;
- секреты запрещены.

Следующий шаг: дайте 3–5 исходных материалов для первого ingest.
```

---

## 18. Жёсткие запреты

Не делай этого:

- не складывай всё подряд в одну папку;
- не называй черновики source of truth;
- не индексируй приватные или чужие папки без разрешения;
- не сохраняй секреты;
- не переписывай сырые источники;
- не делай silent write в Obsidian vault без понятного diff;
- не создавай сложную архитектуру до первой полезной wiki-страницы.

Сначала простая рабочая система. Потом расширения.

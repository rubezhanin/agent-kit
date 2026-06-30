# Agent-user brief: локальный embedding и memory-index

Версия: 2026-04-30  
Назначение: дать AI-агенту или техническому пользователю понятную инструкцию, как использовать локальный embedding как retrieval-слой, без приватных данных владельца.

---

## 1. Главная идея

Локальный embedding нужен не как «магическая память», а как поиск по смыслу в проверенной базе знаний.

Агент не должен помнить всё. Агент должен:

1. получить задачу;
2. понять, какие знания нужны;
3. вызвать retrieval tool;
4. получить несколько релевантных фрагментов;
5. ответить по источникам;
6. явно сказать, если источников не хватает.

---

## 2. Рекомендуемый стек

Базовый стек:

```text
Python 3.10+
fastembed
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
SQLite
FTS5
Markdown/Text source documents
read-only search tool for agent
```

Параметры модели:

```text
model: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
dimensions: 384
runtime: fastembed
```

Почему эта модель:

- работает с русским и английским;
- лёгкая;
- запускается на CPU;
- подходит для Mac mini, MacBook, Linux-сервера и VPS;
- достаточно хороша для wiki, инструкций и процедур;
- проста в установке и обслуживании.

---

## 3. Где запускать

Допустимые варианты:

### Вариант A — всё локально

```text
agent runtime + memory-index + docs на одной машине
```

Подходит для личного агента и быстрого старта.

### Вариант B — индекс на Mac mini

```text
ноутбук/чат → агент → Mac mini retrieval → source docs/index
```

Подходит, если Mac mini постоянно включён и играет роль домашнего сервера.

### Вариант C — индекс на VPS/Linux-сервере

```text
несколько агентов → private network/VPN → retrieval server
```

Подходит для постоянного доступа и команды.

### Вариант D — read-only копии

```text
одна машина пересобирает индекс → другие машины получают read-only копию DB
```

Подходит, если агенты не должны менять базу.

---

## 4. Что индексировать

Разрешённые источники:

- `wiki/`
- `references/`
- `procedures/`
- `docs/`
- curated owner/team context
- README
- ADR / architecture notes
- инструкции запуска, деплоя, отладки
- правила работы агента

---

## 5. Что исключить

Исключать всегда, если нет отдельного решения:

```text
.env
*.env
secrets/
tokens/
credentials/
logs/
backups/
archive/
node_modules/
.venv/
venv/
dist/
build/
raw chat dumps
Telegram/Slack/Discord exports
private finance docs
binary/media files
```

Правило: агент не должен случайно найти то, что нельзя показать в ответе.

---

## 6. Установка на macOS

```bash
mkdir -p ~/agent-memory-index
cd ~/agent-memory-index
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install fastembed numpy pytest
```

Smoke test:

```bash
python - <<'PY'
from fastembed import TextEmbedding
model = TextEmbedding(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
vec = list(model.embed(["локальный embedding для AI-агента"]))[0]
print("dimensions", len(vec))
assert len(vec) == 384
PY
```

---

## 7. Установка на Linux/VPS

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip sqlite3
mkdir -p ~/agent-memory-index
cd ~/agent-memory-index
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install fastembed numpy pytest
```

Smoke test:

```bash
python - <<'PY'
from fastembed import TextEmbedding
model = TextEmbedding(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
vec = list(model.embed(["how to rebuild memory index"]))[0]
print("dimensions", len(vec))
assert len(vec) == 384
PY
```

---

## 8. Retrieval contract для агента

Агент должен иметь tool примерно такого вида:

Input:

```json
{
  "query": "как пересобрать индекс памяти",
  "top_k": 5,
  "source_type": "any"
}
```

Output:

```json
{
  "success": true,
  "results": [
    {
      "path": "docs/memory-index.md",
      "heading": "Rebuild",
      "score": 0.82,
      "snippet": "..."
    }
  ]
}
```

Правила ответа агента:

1. Используй найденные фрагменты как источник.
2. Не выдавай найденный snippet за абсолютную истину, если он старый или противоречивый.
3. Если результатов нет — скажи, что в базе знаний не найдено.
4. Если вопрос рискованный — запроси подтверждение перед изменениями.
5. Не записывай в source of truth автоматически.

---

## 9. Индексация: production pattern

Минимальный production-процесс:

```text
1. scan source roots
2. reject forbidden paths
3. split documents into chunks
4. embed title + heading + chunk body
5. write documents/chunks to temporary SQLite DB
6. create FTS5 index
7. run secret scan
8. run benchmark queries
9. atomically replace live DB
10. expose read-only search tool
```

---

## 10. Команды, которые стоит иметь

```bash
python memory_index.py rebuild-atomic
python memory_index.py verify
python memory_index.py secret-scan
python memory_index.py benchmark
python memory_index.py search "локальный embedding" --top-k 5
```

`rebuild-atomic` обязателен для безопасного обновления: новая база сначала собирается и проверяется отдельно, потом заменяет старую.

---

## 11. Benchmark

Нужен набор контрольных запросов.

Пример:

```text
query: "как обновить индекс памяти"
expected path contains: "memory-index"

query: "правила работы агента с секретами"
expected path contains: "security" or "secrets"

query: "как запустить проект локально"
expected path contains: "README" or "setup"
```

Без benchmark нельзя понять, улучшился поиск или деградировал.

---

## 12. Security gate

Перед подключением к агенту проверить:

- нет `.env` в indexed paths;
- нет токенов в chunk text;
- нет приватных дампов;
- нет backup/archive мусора;
- DB доступна агенту только на чтение;
- retrieval endpoint не открыт в публичный интернет;
- server закрыт VPN/firewall/SSH tunnel.

---

## 13. System prompt rule для агента

Можно добавить агенту такое правило:

```text
When a task depends on local project knowledge, procedures, architecture, roles, policies, or previous curated context, call the local memory_index_search tool first. Treat the index as a retrieval layer over source documents, not as canonical truth. Prefer cited source snippets over memory. If search returns nothing relevant, say so and ask for missing context instead of guessing.
```

Русская версия:

```text
Когда задача зависит от локальных знаний проекта, процедур, архитектуры, ролей, политик или curated context, сначала вызови memory_index_search. Считай индекс поисковым слоем поверх документов, а не источником истины. Предпочитай найденные фрагменты памяти и догадкам. Если поиск ничего полезного не вернул — скажи об этом и запроси недостающий контекст, не выдумывай.
```

---

## 14. Минимальный критерий готовности

Считать систему готовой только если:

- smoke test модели проходит;
- индекс содержит ожидаемые документы;
- forbidden paths не попали в DB;
- secret scan чистый;
- benchmark проходит;
- agent tool возвращает 3–5 релевантных результатов;
- агент в ответе использует найденные источники;
- есть понятная команда пересборки.

---

## 15. Короткая формула для пользователя

Локальный embedding — это не память агента. Это навигация по памяти.

Хороший агент не «помнит всё». Он умеет быстро найти правильный документ, поднять нужный кусок в контекст и честно ответить по источнику.

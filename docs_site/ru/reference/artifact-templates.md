# Шаблоны артефактов

> Зеркало `agent-center/templates/artifacts/README.md` для сайта документации.

Origin Return Protocol требует, чтобы каждая задача оставила **артефакт** — файл, который владелец может открыть. Эти шаблоны предзаполняют пять якорей, чтобы оператор не выдумывал их каждый раз.

## Шаблоны

| Шаблон | Когда |
| --- | --- |
| **Note** | Короткая заметка, одно наблюдение. |
| **Report** | Длинный аналитический артефакт с источниками. |
| **Brief** | Одностраничная сводка для стейкхолдера. |
| **Summary** | TL;DR для завершённой задачи. |
| **Hypothesis** | Рабочая гипотеза с планом фальсификации. |

Каждый шаблон лежит в `agent-center/templates/artifacts/<name>.md`. Скопировал, заполнил, сохранил, протащил путь обратно через `return_path`.

## Блок Origin Return (вверху каждого шаблона)

```yaml
origin:
owner:
artifact: ./<this-file>.md
status: DONE | BLOCKED | NEEDS_APPROVAL | STALE
return_path:
verification:
```

Шаблон без `status:` или `return_path:` — это черновик, не артефакт. CI-валидатор `scripts/check_orp.py` ловит это.

## Словарь статусов

На уровне оператора признаются только четыре:

| Статус | Когда |
| --- | --- |
| `DONE` | Готово, проверено, возвращено в `return_path`. |
| `BLOCKED` | Нет файла / доступа / решения / контекста. |
| `NEEDS_APPROVAL` | Требуется внешнее действие. |
| `STALE` | Задача зависла; нужна перепроверка. |

## Подробнее

| Документ | Зачем |
| --- | --- |
| [`agent-center/templates/artifacts/README.md`](https://github.com/rubezhanin/agent-kit/blob/main/agent-center/templates/artifacts/README.md) | Индекс шаблонов. |
| [`agent-center/operations/origin-return-protocol/PROTOCOL.ru.md`](https://github.com/rubezhanin/agent-kit/blob/main/agent-center/operations/origin-return-protocol/PROTOCOL.ru.md) | Полный текст протокола. |
| [`scripts/check_orp.py`](https://github.com/rubezhanin/agent-kit/blob/main/scripts/check_orp.py) | CI-валидатор. |
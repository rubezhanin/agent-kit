# Origin Return Protocol — интеграция в kit

> Зеркало `agent-center/wiki/origin-return-protocol.ru.md`. Канонический английский — `../../en/architecture/origin-return-protocol.md`.

Первое правило kit:

> Задача закрыта только когда результат вернулся туда, где его попросили.

Ответ, который сводится к «Готово», — это не закрытие, это невидимость. Протокол встроен в контракт, шаблоны и навыки.

## Пять якорей у каждой задачи

| Якорь | Вопрос |
| --- | --- |
| `origin` | Откуда пришёл запрос? |
| `owner` | Кто отвечает за итог? |
| `artifact` | Где лежит результат? |
| `status` | Какой сейчас статус? |
| `return_path` | Куда вернуть финальный ответ? |

## Четыре статуса — без зоопарка

| Статус | Когда |
| --- | --- |
| `DONE` | Результат готов, проверен и возвращён в `return_path`. |
| `BLOCKED` | Агент не может продолжить без файла, доступа, решения или контекста. |
| `NEEDS_APPROVAL` | Требуется внешнее действие (отправить, опубликовать, удалить, оплатить, изменить живую систему, использовать секрет). |
| `STALE` | Задача зависла или устарела; нужна перепроверка. |

## Формат финального ответа

```text
Status: DONE | BLOCKED | NEEDS_APPROVAL | STALE
Outcome: что сделано
Artifact: путь к результату
Verification: что проверено
Returned to: куда вернулся итог
Blocked: что осталось нерешённым
```

Ответ одним «Готово» — это не закрытие, это невидимость.

## Где kit это поддерживает

| Слой | Где лежит |
| --- | --- |
| Skill-обёртка | `agent-center/skills/operations/origin-return-protocol/SKILL.md` |
| Справка (EN/RU) | `agent-center/operations/origin-return-protocol/PROTOCOL.{en,ru}.md` |
| Профиль по умолчанию | `main-operator.profile.json` и все активные профили подгружают skill |
| Контракт оператора | `agent-center/AGENTS.md` — блок «Первое правило» |
| Системный промпт | `agent-center/prompts/main-agent-system.md` |
| Форма финального ответа | `agent-center/prompts/final-report.md` |
| Шаблоны | `agent-center/templates/task-card.md` + `agent-center/templates/receipt.md` |
| Wiki-страница | `agent-center/wiki/origin-return-protocol.md` |

## Self-test оператора

Прежде чем ответить владельцу, ответьте на четыре вопроса:

```text
Где результат?
Что проверено?
Куда вернулся итог?
Что осталось заблокировано?
```

Если хоть один ответ пустой — задача не закрыта.

## Подробнее

Полный оригинал протокола на русском — [`agent-center/operations/origin-return-protocol/PROTOCOL.ru.md`](https://github.com/rubezhanin/agent-kit/blob/main/agent-center/operations/origin-return-protocol/PROTOCOL.ru.md).
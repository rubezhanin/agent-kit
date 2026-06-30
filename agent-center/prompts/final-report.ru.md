# Формат финального отчёта (Origin Return Protocol)

> Русская локализация. Канонический английский — [`agent-center/prompts/final-report.md`](agent-center/prompts/final-report.md).

Использовать после каждой задачи. Формат обязателен по **Origin Return Protocol**: задача закрыта только когда результат дошёл до `return_path`.

```text
Status: DONE | BLOCKED | NEEDS_APPROVAL | STALE
Outcome: что сделано
Artifact: путь к результату
Verification: что проверено
Returned to: куда вернулся итог (чат / файл / канал)
Blocked: что осталось нерешённым, если есть
```

## Правила

- Не заявлять `DONE`, если результат не дошёл до `return_path`.
- Указать, если проверка не запускалась.
- Не показывать пользователю сырые approval / tool-блоки.
- Ответ одним «Готово» — это невидимость, а не закрытие.

## Напоминание про якоря

У каждой задачи пять якорей:

| Якорь | Источник |
| --- | --- |
| `origin` | Откуда пришёл запрос. |
| `owner` | Кто отвечает за итог. |
| `artifact` | Где лежит результат. |
| `status` | `DONE` / `BLOCKED` / `NEEDS_APPROVAL` / `STALE`. |
| `return_path` | Куда вернуть финальный ответ. |

См. [`../operations/origin-return-protocol/PROTOCOL.ru.md`](../operations/origin-return-protocol/PROTOCOL.ru.md).
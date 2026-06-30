# Origin Return Protocol (интеграция в kit)

> Русская локализация. Канонический английский — [`agent-center/wiki/origin-return-protocol.md`](../agent-center/wiki/origin-return-protocol.md).

Зеркало `agent-center/wiki/origin-return-protocol.md` для сайта документации.

## Что это за протокол

Первое правило агентской операционки:

> Задача закрыта только когда результат вернулся туда, где его попросили.

Ответ, который сводится к «Готово», — это не закрытие, это невидимость для владельца.

## Пять якорей

| Якорь | Вопрос |
| --- | --- |
| `origin` | Откуда пришёл запрос? |
| `owner` | Кто отвечает за итог? |
| `artifact` | Где лежит результат? |
| `status` | Какой сейчас статус? |
| `return_path` | Куда вернуть финальный ответ? |

## Четыре статуса

| Статус | Когда |
| --- | --- |
| `DONE` | Результат готов, проверен и возвращён в `return_path`. |
| `BLOCKED` | Нельзя продолжить без файла, доступа, решения или контекста. |
| `NEEDS_APPROVAL` | Требуется внешнее действие. |
| `STALE` | Задача зависла; нужна перепроверка. |

## Формат финального ответа

```text
Status: DONE | BLOCKED | NEEDS_APPROVAL | STALE
Outcome: что сделано
Artifact: путь к результату
Verification: что проверено
Returned to: куда вернулся итог
Blocked: что осталось нерешённым
```

## Где kit это поддерживает

- Навык: `agent-center/skills/operations/origin-return-protocol/SKILL.md`.
- Справка: `agent-center/operations/origin-return-protocol/PROTOCOL.ru.md` (оригинал) и `PROTOCOL.en.md`.
- Загружается: во все активные профили, включая `main-operator`.
- Контракт оператора: `agent-center/AGENTS.ru.md` — блок «Первое правило».
- Шаблоны: `agent-center/templates/task-card.md` и `agent-center/templates/receipt.md`.

## Быстрый self-test

Запросите у агента:

```text
Создай файл test-result.md с одной строкой: ORIGIN_RETURN_OK.
Используй Origin Return Protocol.
Верни статус, путь, проверку и финальное сообщение.
```

Правильный ответ содержит все пять якорей и формат финального ответа. Ответ «Сделал.» — это провал.

## Подробнее

| Документ | Зачем |
| --- | --- |
| [`agent-center/operations/origin-return-protocol/PROTOCOL.ru.md`](https://github.com/your-org/hermes-agent-architecture-kit/blob/main/agent-center/operations/origin-return-protocol/PROTOCOL.ru.md) | Оригинал протокола на русском. |
| [`agent-center/skills/operations/origin-return-protocol/SKILL.md`](https://github.com/your-org/hermes-agent-architecture-kit/blob/main/agent-center/skills/operations/origin-return-protocol/SKILL.md) | Skill-обёртка. |
| [`agent-center/templates/task-card.md`](https://github.com/your-org/hermes-agent-architecture-kit/blob/main/agent-center/templates/task-card.md) | Шаблон карточки задачи. |
| [`agent-center/templates/receipt.md`](https://github.com/your-org/hermes-agent-architecture-kit/blob/main/agent-center/templates/receipt.md) | Шаблон receipt. |
| [`agent-center/AGENTS.ru.md`](https://github.com/your-org/hermes-agent-architecture-kit/blob/main/agent-center/AGENTS.ru.md) | Контракт оператора. |
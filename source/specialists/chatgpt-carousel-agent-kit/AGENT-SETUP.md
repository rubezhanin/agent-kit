# AGENT-SETUP — как агенту развернуть Carousel Agent Kit пользователю

Этот файл нужен для ситуации: пользователь дал агенту ZIP-архив `chatgpt-carousel-agent-kit-v0.1.0.zip` и просит развернуть систему создания каруселей.

## Цель агента

Развернуть пользователю переносимую систему для создания Telegram/Instagram-каруселей:

```text
brand intake -> SMM/marketing brief -> carousel structure -> visual brief -> GPT Image prompt-pack -> OTK -> final delivery
```

## Жёсткие правила

Агент не должен:

- просить API keys, access tokens, cookies, session files;
- публиковать или отправлять что-либо без отдельного подтверждения пользователя;
- использовать чужие приватные стили, лица, референсы или брендбуки;
- обещать, что live image generation сработает у всех одинаково;
- начинать с генерации картинок до brand intake;
- игнорировать медицинские, финансовые, юридические или репутационные риски.

## Шаг 1 — распаковать архив

Архив содержит top-level папку:

```text
chatgpt-carousel-agent-kit/
```

Распакуй ZIP и зайди внутрь этой папки:

```bash
unzip chatgpt-carousel-agent-kit-v0.1.0.zip
cd chatgpt-carousel-agent-kit
```

После этого в текущей папке должны быть файлы:

```text
README.md
INSTALL.md
CHATGPT-PROJECT-INSTRUCTIONS.md
CUSTOM-GPT-INSTRUCTIONS.md
01-BRAND-INTAKE.md
02-SMM-MARKETER.md
03-CAROUSEL-WORKFLOW.md
04-VISUAL-DESIGNER.md
05-GPT-IMAGE-PROMPTS.md
06-OTK-CHECKLIST.md
07-TROUBLESHOOTING.md
templates/
examples/
smoke-tests/
optional-local-cli/
hermes-skill/
```

## Шаг 2 — проверить пакет

Если есть Python:

```bash
python3 scripts/verify_package.py
```

Ожидаемый результат:

```text
PASS: package structure, markdown sanity and leak scan are clean
```

Если Python недоступен, проверь вручную, что основные файлы из шага 1 существуют и не пустые.

## Шаг 3 — выбрать режим установки

Спроси пользователя одним вопросом:

```text
Куда разворачиваем Carousel Agent Kit?
1. ChatGPT Project
2. Custom GPT
3. Hermes Agent skill
4. Просто папка с инструкциями и шаблонами
5. Локальная генерация через gpt-image-2-agent-kit тоже нужна
```

Если пользователь не знает, выбери безопасный дефолт: `ChatGPT Project`.

## Шаг 4A — ChatGPT Project

Дай пользователю инструкции:

1. Создать новый ChatGPT Project.
2. Назвать его `Carousel Agent Kit`.
3. Загрузить все `.md` файлы из папки пакета как Knowledge.
4. Загрузить `templates/` и `examples/`, если интерфейс позволяет.
5. В Project Instructions вставить содержимое `CHATGPT-PROJECT-INSTRUCTIONS.md`.
6. Начать с команды:

```text
Проведи brand intake для моей карусели. Не создавай финальную карусель, пока не соберёшь brand-profile.
```

## Шаг 4B — Custom GPT

Дай пользователю инструкции:

1. Создать Custom GPT.
2. Name: `Carousel Agent Kit`.
3. Description: `Помогает собирать бренд-анкету, SMM brief, структуру карусели, prompts для GPT Image и OTK.`
4. Instructions: вставить `CUSTOM-GPT-INSTRUCTIONS.md`.
5. Knowledge: загрузить основные `.md` файлы и `templates/`.
6. Image generation включать только если пользователь понимает ограничения и будет проверять результат.

## Шаг 4C — Hermes Agent skill

Если у пользователя есть Hermes Agent:

1. Скопируй папку `hermes-skill/` как отдельную skill-директорию с именем `carousel-agent-kit` в каталог skills нужного профиля пользователя.
2. Итоговая структура должна быть такой:

```text
<profile-skills>/carousel-agent-kit/SKILL.md
<profile-skills>/carousel-agent-kit/references/...
```

3. Проверь, что skill виден в Hermes.
4. Запусти тестовую задачу:

```text
Создай карусель по теме: 5 ошибок в постановке задач дизайнеру. Сначала проведи brand intake.
```

Не угадывай путь Hermes-профиля. Он зависит от установки пользователя.

## Шаг 4D — просто папка

Если пользователь не хочет ничего устанавливать:

1. Оставь папку как справочник.
2. Объясни порядок работы:

```text
01-BRAND-INTAKE.md
02-SMM-MARKETER.md
03-CAROUSEL-WORKFLOW.md
04-VISUAL-DESIGNER.md
05-GPT-IMAGE-PROMPTS.md
06-OTK-CHECKLIST.md
```

3. Скажи, что ответы надо сохранять в шаблоны из `templates/`.

## Шаг 4E — optional local image generation

Если пользователь хочет локальный CLI-слой для генерации/receipts:

1. Открой `optional-local-cli/README.md`.
2. Установи публичный `gpt-image-2-agent-kit` по инструкции.
3. Сначала выполни dry-run:

```bash
gpt-image2-agent "Telegram carousel slide, no private data" --root . --preset russian-text --aspect square --dry-run --json
```

4. Live generation запускать только после явного подтверждения пользователя и только с его собственным совместимым доступом.

## Шаг 5 — smoke test

Используй тест из `smoke-tests/neutral-business-test.md`.

Ожидаемый результат:

- brand-profile;
- marketing brief;
- carousel brief;
- slide-plan;
- visual brief;
- prompt-pack;
- OTK report;
- никаких приватных ссылок/стилей/секретов;
- никаких гарантированных claims.

## Шаг 6 — финальный отчёт пользователю

Верни пользователю короткий отчёт:

```text
Готово.
Развёрнуто как: <ChatGPT Project / Custom GPT / Hermes skill / folder>
Пакет проверен: PASS / вручную проверен
Smoke test: PASS / not run + why
Live image generation: not configured / configured by user / not tested
Следующий шаг: провести brand intake для первой карусели
```

## Важное ограничение

Этот kit автоматизирует подготовку карусели и prompt-pack. Полностью автоматическая генерация готовых PNG зависит от выбранного инструмента, доступа пользователя, текущих лимитов, правил сервиса и качества prompts. Если live generation не настроена, kit всё равно полезен: он выдаёт структуру, тексты, визуальное ТЗ и prompts для ручной генерации в ChatGPT/GPT Image.

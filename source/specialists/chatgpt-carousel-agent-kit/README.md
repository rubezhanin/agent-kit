# ChatGPT Carousel Agent Kit

Переносимый набор Markdown-инструкций для создания Telegram/Instagram-каруселей через ChatGPT Project, Custom GPT, любого markdown-friendly агента или опционально через локальный CLI для GPT Image.

Пакет помогает пройти весь путь:

```text
brand intake -> SMM/marketing brief -> carousel structure -> visual brief -> GPT Image prompt-pack -> OTK -> final delivery
```

## Для кого

- эксперт, консультант, школа, малый бизнес, автор канала;
- SMM-специалист, который хочет быстрее собирать карусели;
- дизайнер, который генерирует изображения через GPT Image;
- агент/ассистент, которому нужен понятный процесс, а не один огромный prompt.

## Что внутри

- `AGENT-SETUP.md` — инструкция для любого агента, которому пользователь отдаёт ZIP и просит всё развернуть.
- `CHATGPT-PROJECT-INSTRUCTIONS.md` — готовые инструкции для ChatGPT Project.
- `CUSTOM-GPT-INSTRUCTIONS.md` — инструкции для Custom GPT.
- `01-BRAND-INTAKE.md` — анкета бренда/продукта/аудитории.
- `02-SMM-MARKETER.md` — маркетинговый смысл и структура.
- `03-CAROUSEL-WORKFLOW.md` — общий производственный процесс.
- `04-VISUAL-DESIGNER.md` — дизайн, композиция, визуальные правила.
- `05-GPT-IMAGE-PROMPTS.md` — как писать prompts для GPT Image.
- `06-OTK-CHECKLIST.md` — финальная проверка качества.
- `07-TROUBLESHOOTING.md` — типовые проблемы.
- `templates/` — пустые шаблоны рабочих файлов.
- `examples/` — нейтральный пример.
- `optional-local-cli/` — опциональная связка с публичным `gpt-image-2-agent-kit`.
- `hermes-skill/` — опциональная версия skill-пакета для Hermes Agent.

## Быстрый старт в ChatGPT Project

1. Создайте новый ChatGPT Project.
2. Назовите его `Carousel Agent Kit`.
3. Загрузите core-файлы как Knowledge:

```text
PACKAGE-CONTRACT.md
01-BRAND-INTAKE.md
02-SMM-MARKETER.md
03-CAROUSEL-WORKFLOW.md
04-VISUAL-DESIGNER.md
05-GPT-IMAGE-PROMPTS.md
06-OTK-CHECKLIST.md
07-TROUBLESHOOTING.md
templates/*.md
examples/**/*.md
```

`AGENT-SETUP.md`, `VERIFICATION-RECEIPT.md`, `RELEASE-NOTES.md` и `smoke-tests/` нужны для установки/проверки, но не обязательны как Knowledge.
4. В Project Instructions вставьте содержимое `CHATGPT-PROJECT-INSTRUCTIONS.md`.
5. Начните с сообщения:

```text
Проведи brand intake для моей карусели. Не создавай финальную карусель, пока не соберёшь brand-profile.
```

## Быстрый старт без установки

Можно просто открыть файлы по порядку и копировать блоки в ChatGPT:

```text
01-BRAND-INTAKE.md
02-SMM-MARKETER.md
03-CAROUSEL-WORKFLOW.md
04-VISUAL-DESIGNER.md
05-GPT-IMAGE-PROMPTS.md
06-OTK-CHECKLIST.md
```

## Что получится на выходе

```text
brand-profile.md
marketing-brief.md
carousel-brief.md
slide-plan.md
visual-brief.md
prompt-pack.md
otk-report.md
final-delivery-report.md
```

Если подключена генерация изображений:

```text
generated/slides/*.png
generated/contact-sheet.png
generated/final-carousel.zip
```

## Честные ограничения

- Это не автопубликующий сервис.
- Это не обход лимитов и не бесплатная генерация.
- Результат GPT Image зависит от аккаунта, региона, лимитов, интерфейса и текущих условий сервиса.
- Русский текст внутри изображений может ошибаться. Нужен OTK и иногда ручная правка.
- Для точного лица нужны собственные референсы и право их использовать.
- Медицинские, финансовые, юридические и репутационные утверждения требуют осторожности.

## Главное правило

Не начинайте с картинки. Сначала собирается бренд, аудитория, задача и смысл. Картинка - последний слой, а не начало работы.

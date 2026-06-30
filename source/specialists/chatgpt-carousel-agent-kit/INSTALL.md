# Установка и варианты использования

## Вариант A — ChatGPT Project

1. Создайте новый ChatGPT Project.
2. Загрузите в Knowledge все основные `.md` файлы из пакета.
3. Загрузите папки `templates/` и `examples/`, если интерфейс позволяет.
4. В Project Instructions вставьте текст из `CHATGPT-PROJECT-INSTRUCTIONS.md`.
5. Стартовая команда:

```text
Проведи brand intake. Не создавай карусель, пока не соберёшь brand-profile.
```

## Вариант B — Custom GPT

1. Создайте Custom GPT.
2. Name: `Carousel Agent Kit`.
3. Description: `Помогает собирать бренд-анкету, SMM brief, структуру карусели, prompts для GPT Image и OTK.`
4. Instructions: вставьте `CUSTOM-GPT-INSTRUCTIONS.md`.
5. Knowledge: загрузите основные `.md` и `templates/`.
6. Capabilities:
   - Image generation: optional, если доступно.
   - Code interpreter: optional, если нужно упаковывать файлы.
   - Web browsing: optional, если нужны внешние факты.

## Вариант C — ручной workflow

Откройте файлы по порядку:

```text
01-BRAND-INTAKE.md
02-SMM-MARKETER.md
03-CAROUSEL-WORKFLOW.md
04-VISUAL-DESIGNER.md
05-GPT-IMAGE-PROMPTS.md
06-OTK-CHECKLIST.md
```

Копируйте нужные блоки в ChatGPT и сохраняйте ответы в файлы из `templates/`.

## Вариант D — optional local CLI через публичный GPT Image 2 Agent Kit

Этот путь нужен, если вы хотите локально планировать prompts, refs, receipts и опционально запускать live-генерацию через свой совместимый доступ.

Публичный репозиторий:

```text
https://github.com/AlekseiUL/gpt-image-2-agent-kit
```

Установка:

```bash
mkdir -p ~/ai-tools
cd ~/ai-tools

git clone https://github.com/AlekseiUL/gpt-image-2-agent-kit.git
cd gpt-image-2-agent-kit

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .

gpt-image2-agent --help
```

Сначала используйте dry-run:

```bash
gpt-image2-agent "Telegram carousel cover, clean educational style, no private data" \
  --root . \
  --preset russian-text \
  --preset brand-style \
  --aspect square \
  --dry-run \
  --review-markdown
```

Live-генерация - только если вы понимаете, как настроен ваш доступ и что именно отправляется во внешний сервис.

## Вариант E — Hermes Agent skill

Если у вас есть Hermes Agent, можно скопировать `hermes-skill/` в папку skills своего профиля. Путь зависит от вашей установки и профиля.

Скопируйте папку `hermes-skill/` как отдельную skill-директорию с именем `carousel-agent-kit` в каталог skills нужного профиля вашей установки Hermes.

Итоговая структура должна быть такой:

```text
<profile-skills>/carousel-agent-kit/SKILL.md
<profile-skills>/carousel-agent-kit/references/...
```

Проверка зависит от вашей версии Hermes. Используйте команды просмотра skills из вашей установки. В публичном пакете путь не фиксируется: у разных пользователей он отличается.

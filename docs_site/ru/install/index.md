# Установка

> Зеркало `docs/GITHUB_INSTALL.ru.md`. English — [here](../../en/install/index.md).

## Быстрый старт

```bash
git clone https://github.com/rubezhanin/agent-kit hermes-agent
cd hermes-agent

# Linux / macOS:
sh ./install.sh

# Windows PowerShell:
.\install.ps1

# Кросс-платформенный (рекомендуется):
python scripts/setup_kit.py --dry-run
python scripts/setup_kit.py
```

## Если Hermes Agent не установлен

Установщик проверяет `hermes` и `hermes-agent` и запускает install-команду **только** после явного подтверждения.

```bash
export HERMES_KIT_HERMES_INSTALL_COMMAND="<OFFICIAL_INSTALL_COMMAND>"
python scripts/setup_kit.py --install-hermes
```

…или флагом:

```bash
python scripts/setup_kit.py --install-hermes --hermes-install-command "<OFFICIAL_INSTALL_COMMAND>"
```

## Конфигурация через `.env`

```bash
cp .env.example .env
$EDITOR .env
```

Полный список переменных — в файле `.env.example`.

## Что делает установщик

- читает `kit-manifest.json`;
- обнаруживает профили из `agent-center/profiles/*.profile.json`;
- готовит / использует workspace `agent-center`;
- сохраняет выбранные профили в `.hermes-kit/selected-profiles.json`;
- пишет install-receipt в `reports/task-receipts/`;
- оставляет опциональные интеграции выключенными.

## Что установщик НЕ делает по умолчанию

- не запрашивает секреты в чате;
- не правит production-конфиг вслепую;
- не включает Telegram watcher;
- не подписывается на Telegram-каналы;
- не считает, что Kanban / Curator уже доступны.

## Дальше

| Гайд | Зачем |
| --- | --- |
| [One-file installer](one-file.md) | Диалог для чистого Hermes-агента. |
| [Добавление профилей](adding-profiles.md) | Положить JSON — получить нового специалиста. |
| [Архитектура](../architecture/index.md) | End-to-end архитектура. |
| [Changelog](../reference/changelog.md) | Что менялось между версиями. |
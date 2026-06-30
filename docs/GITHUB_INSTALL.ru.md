# Справочник установщика (GitHub Install)

> Русская локализация. Канонический английский вариант — [`docs/GITHUB_INSTALL.en.md`](docs/GITHUB_INSTALL.en.md).

## Быстрый старт

```bash
git clone https://github.com/rubezhanin/agent-kit hermes-agent
cd hermes-agent
sh ./install.sh        # POSIX
python scripts/setup_kit.py   # кросс-платформенный
```

Windows PowerShell:

```powershell
git clone https://github.com/rubezhanin/agent-kit hermes-agent
cd hermes-agent
.\install.ps1
```

## Если Hermes Agent не установлен

Установщик проверяет:

```text
hermes
hermes-agent
```

Разные дистрибутивы Hermes ставятся по-разному, поэтому kit не вшивает фиктивную «универсальную» команду установки.

Используйте один из вариантов:

```bash
python scripts/setup_kit.py --install-hermes --hermes-install-command "<OFFICIAL_INSTALL_COMMAND>"
```

или:

```bash
export HERMES_KIT_HERMES_INSTALL_COMMAND="<OFFICIAL_INSTALL_COMMAND>"
python scripts/setup_kit.py --install-hermes
```

PowerShell:

```powershell
$env:HERMES_KIT_HERMES_INSTALL_COMMAND="<OFFICIAL_INSTALL_COMMAND>"
.\install.ps1 -Yes
```

Скрипт спрашивает подтверждение перед запуском команды, если не передан `--yes` / `-Yes`.

## Dry-run

```bash
python scripts/setup_kit.py --dry-run
```

PowerShell:

```powershell
.\install.ps1 -DryRun
```

## Установка в другой workspace

```bash
python scripts/setup_kit.py --workspace ~/AgentCenter
```

## Если известен HERMES_HOME

```bash
python scripts/setup_kit.py --hermes-home ~/.hermes --main-profile main-operator
```

Установщик пишет маленький указатель пакета `hermes-kit` сюда:

```text
<HERMES_HOME>/profiles/<main-profile>/hermes-kit/
```

Он **не** перетирает неизвестный ему runtime-конфиг Hermes.

## Конфигурация через `.env`

Все настройки, не выраженные флагами, можно задать в `.env` (шаблон — `.env.example`). CLI-флаги перекрывают значения из env.

```bash
cp .env.example .env
$EDITOR .env
```

Полезные переменные:

| Переменная | Назначение |
| --- | --- |
| `HERMES_KIT_WORKSPACE` | Путь к целевому workspace. |
| `HERMES_KIT_HERMES_HOME` | Домашняя директория Hermes. |
| `HERMES_KIT_MAIN_PROFILE` | Имя главного профиля (по умолчанию `main-operator`). |
| `HERMES_KIT_YES` | Авто-подтверждение безопасных дефолтов (`true` / `false`). |
| `HERMES_KIT_DRY_RUN` | Принудительный dry-run (`true` / `false`). |
| `HERMES_KIT_HERMES_INSTALL_COMMAND` | Команда установки Hermes, если его нет. |
| `HERMES_KIT_INSTALL_HERMES` | Разрешить запуск install-команды без интерактива. |
| `HERMES_KIT_DEFAULT_PROFILES` | CSV-переопределение дефолтных профилей. |
| `HERMES_KIT_INCLUDE_DISABLED` | Предлагать выключенные по умолчанию профили. |
| `HERMES_KIT_SAFETY_LEVEL` | `strict`, `balanced` или `permissive`. |
| `HERMES_KIT_LOCK_OUTSIDE_WORKSPACE` | Запретить писать вне выбранного workspace. |
| `HERMES_KIT_REFUSE_SHELL_FROM_ENV` | Защита: отказываться от shell-команд из env. |

## Что делает установщик

- читает `kit-manifest.json`;
- обнаруживает профили из `agent-center/profiles/*.profile.json`;
- готовит / использует workspace `agent-center`;
- сохраняет выбранные профили в `.hermes-kit/selected-profiles.json`;
- пишет install-receipt в `reports/task-receipts/`;
- оставляет опциональные интеграции выключенными, пока их не выбрали.

## Что установщик НЕ делает по умолчанию

- не запрашивает секреты в чате;
- не правит production-конфиг вслепую;
- не включает Telegram watcher;
- не подписывается на Telegram-каналы;
- не считает, что Kanban / Curator уже доступны.
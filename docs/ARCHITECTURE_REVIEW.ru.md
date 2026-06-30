# Architecture Review

## Итоговая архитектура

```text
Human / Owner
  -> Gateway / CLI / Direct chat
  -> Main Operator Hermes profile
  -> Intake + risk triage
  -> Direct answer OR Kanban task
  -> Specialist profile/skill
  -> Artifact / report / receipt
  -> Quality gate
  -> Final user-facing answer
  -> Audit / health / skill hygiene / token diagnostics
```

Главная идея: Hermes - это движок. Рабочая агентская система появляется только после добавления контура: workspace, источники правды, память, task board, routing, safety, receipts и maintenance.

## Найденные ошибки исходного набора

| Ошибка | Почему это плохо | Исправление в `kit` |
| --- | --- | --- |
| Нет единого главного operating contract. | Специалисты и инструкции могут спорить между собой. | `agent-center/AGENTS.md` делает main operator владельцем маршрутизации и финального ответа. |
| Слишком много agent-pack'ов как будто все должны быть активны. | Раздувает контекст, routing и стоимость; растёт риск ложной делегации. | `team-roster.md` делит роли на active, on-demand и disabled-by-default. |
| Смешаны Hermes, OpenClaw, n8n, Claude/Codex и учебные материалы. | Агент может применить чужие пути, команды и модель безопасности. | `SOURCE_SELECTION.md` отделяет Hermes deploy от справочных/чужих артефактов. |
| Memory, wiki, reports и vector search местами смешаны. | Durable memory превращается в мусорный лог, retrieval начинает казаться правдой. | `memory-policy.md` задаёт слои: wiki = truth, references = sources, reports = evidence, index = search only. |
| Kanban местами предполагается доступным по версии. | В некоторых сборках функции могут отсутствовать или быть изменены. | `kanban/board-contract.md` требует live discovery перед включением. |
| Нет строгого UX входа для Telegram/direct. | Агент может начать работу до получения файла или молчать без финала. | `config/gateway-telegram.yaml` и `gateway-ux` skill: ingress batching, ACK, final closure. |
| Нет обязательного receipt. | Сложно понять, что сделал агент и чем это проверено. | `templates/receipt.md` и `prompts/final-report.md`. |
| High-risk роли не изолированы. | Legal, economy, psychological support могут звучать как финальные экспертные решения. | Legal/economist активны только как risk-review; psychological support disabled-by-default. |
| Userbot/Telethon может быть воспринят как обычный бот. | Риск спама, блокировки аккаунта, утечки session/secrets. | Вынесен в optional integrations, не включён в базовый профиль. |
| Подписка на Telegram-каналы смешана с research-задачей. | Агент может начать вступать в каналы без выбора владельца и без лимитов. | Добавлен `telegram-channel-intelligence`: researcher только предлагает кандидатов, watcher читает только approved channels. |

## Сильные стороны

| Сильная сторона | Описание |
| --- | --- |
| Чёткий main/operator паттерн | Один агент отвечает за вход, routing, финальный ответ и quality gate. |
| Хорошая база для memory hygiene | Есть wiki, source-of-truth layering, local memory index и запрет хранить всё в durable memory. |
| Kanban как durable execution | Долгие задачи не живут в одном чате; есть статусы, assignee, dependencies, receipt. |
| Повторяемые procedures через skills | Сложные процессы вынесены в skill-обёртки, а не в один огромный prompt. |
| Операционная диагностика | Token drain, skill hygiene, health/audit и gateway UX закрывают реальные эксплуатационные боли. |
| Сильный набор специалистов | Research, technical, business, marketing, design, legal risk, economy и methodologist покрывают большинство задач малого AI-операционного контура. |

## Слабые стороны и ограничения

| Слабое место | Что делать |
| --- | --- |
| Нет live Hermes config/schema в проекте. | `config/*.yaml` сделаны как blueprint. Перед применением сверить с текущей версией Hermes. |
| Source-pack'и длинные. | Не грузить их все в prompt. Skills должны читать source-файл только при релевантной задаче. |
| Недостаточно реальных owner данных. | Первый запуск должен собрать owner-context, privacy, стиль, домены, allowed paths. |
| Specialist overlap | Marketer/Business Analyst/Methodologist иногда пересекаются; main operator должен выбирать одного владельца задачи. |
| High-stakes domains | Legal/economy/psychology должны давать triage и вопросы, а не финальные решения. |

## Агенты

| Агент | Статус | Задачи | Не делает | Взаимодействие |
| --- | --- | --- | --- | --- |
| main-operator | Active | Приём задач, triage, routing, Kanban, финальный ответ, quality gate. | Не делает вид, что всё знает; не обходит approval. | Входная точка для всех задач. |
| researcher | Active | Поиск источников, fact-check, weak signals, public-source intelligence. | Не пишет финальный persuasive copy без проверки. | Получает research brief, возвращает source ledger. |
| technical-engineer | Active | Setup, диагностика, scripts, smoke tests, bounded local changes. | Не меняет production/secrets без approval. | Получает task brief с allowed paths и verification. |
| business-analyst | Active | Process map, automation audit, pilot design, handoff в реализацию. | Не обещает выручку и не внедряет production automation. | Часто стартует перед marketer/technical. |
| methodologist | Active | Гайды, уроки, инструкции, упаковка знаний, agent-ready docs. | Не выдумывает факты и методологию из воздуха. | Использует wiki/references и output requirements. |
| marketer | Active | Audience, offer, proof bank, content/experiment strategy. | Не публикует, не тратит бюджет, не делает claims без proof/approval. | Часто требует researcher и legal-ops review. |
| designer | Active | Visual brief, style pack, prompt pack, visual QA. | Не отправляет приватные материалы наружу без approval. | Получает смысл от marketer/methodologist. |
| legal-ops | Active risk-review | Contract/claim/privacy/vendor risk triage, lawyer packet. | Не заменяет юриста и не даёт final legal advice. | Проверяет marketer/business/technical outputs перед внешними действиями. |
| economist | Active risk-review | ROI, subscriptions, paid pilot economics, pricing floor, runway. | Не двигает деньги и не даёт regulated advice. | Проверяет денежные решения и pilot economics. |
| agent-creator | On-demand | Проектирование новых profiles/skills/helper-agents. | Не создаёт live agent без dry-run, approval, rollback и smoke. | Вызывается только main operator. |
| psychological-support | Disabled by default | Поддерживающий разговор в безопасных границах. | Не диагностирует, не лечит, не заменяет специалиста. | Включать только как отдельный профиль с crisis policy. |
| userbot-operator | Disabled by default | Telegram userbot/MCP read tools, drafts, monitoring. | Не спамит, не отправляет без approval, не хранит session в wiki. | Отдельный интеграционный контур после security review. |
| telegram-channel-watcher | Disabled by default | Чтение approved Telegram channels, summaries, weak signals. | Не подписывается массово, не пишет, не собирает участников, не использует основной аккаунт. | Researcher готовит candidates, owner approves exact handles, technical-engineer настраивает watcher. |

## Оптимальный flow

| Ситуация | Маршрут |
| --- | --- |
| Простая просьба | main-operator отвечает сам. |
| Нужны факты | main-operator -> researcher -> source ledger -> final. |
| Нужны Telegram-каналы по теме | main-operator -> researcher -> candidate list -> owner approval -> watcher setup. |
| Нужно внедрение/файл/код | main-operator -> technical-engineer -> receipt -> review -> final. |
| Бизнес-процесс/автоматизация | business-analyst -> technical-engineer -> legal/economist if needed. |
| Маркетинг/контент | marketer -> researcher/proof -> legal-ops if claims -> designer if visual. |
| Длинная задача | main-operator создаёт Kanban task и dependencies. |
| Рискованное действие | Stop: NEEDS_APPROVAL with exact action, scope, rollback. |

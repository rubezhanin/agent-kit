# Agent Brief: как внедрить Hermes Kanban + Curator + audit-контур

Назначение файла: дать Hermes-агенту или техническому оператору copy-paste-ready инструкцию, как повторить архитектурный паттерн “AI-операционки”: durable задачи через Kanban, weekly Curator, daily skills audit, hourly health auditor, безопасный gatekeeper-процесс.

Документ универсальный. Не предполагает конкретную частную команду, имена агентов или локальные пути.

---

## 0. Роль агента, который читает этот brief

Ты — агент-оператор Hermes-контура.

Твоя задача:

1. Проверить, какие функции доступны в текущей установке Hermes.
2. Внедрить или предложить внедрение Kanban как слоя исполнения.
3. Включить Curator как слой гигиены skill-библиотеки.
4. Добавить read-only проверки skills и health состояния.
5. Не раскрывать secrets.
6. Не переписывать критичные skills/config без diff и approval.
7. Оставить проверяемый след: команды, отчёты, artifacts, rollback notes.

Работай осторожно. Skills и config — это поведение агентной системы. Не ломай их автоматически.

---

## 1. Главная архитектурная идея

Не строить “один длинный чат с агентом”.

Строить операционный контур:

```text
User / Owner
  → Operator / Gatekeeper
  → Kanban Board
  → Specialist Agent Profiles
  → Artifacts / Reports
  → Quality Gate
  → User-facing Output
  → Curator / Audit / Health Checks
```

Слои:

- `Kanban` — execution layer: задачи, статусы, assignee, dependencies, logs, runs, workspaces.
- `Curator` — hygiene layer: уборка skills, поиск дублей, consolidation, stale/archive.
- `Daily skills audit` — read-only контроль качества skill-библиотеки.
- `Health auditor` — проверка gateway/cron/jobs/profiles.
- `Gatekeeper` — человек или главный агент, который подтверждает рискованные изменения.
- `Knowledge base` — source of truth: wiki/docs/references.
- `Memory` — короткие устойчивые факты, не dump всего подряд.
- `Skills` — повторяемые процедуры.

---

## 2. Сначала проверь версию и функции

Выполни:

```bash
hermes --version
hermes kanban --help
hermes curator status
hermes cron list --all
hermes profile list
```

Интерпретация:

- Если `hermes kanban --help` работает — можно внедрять durable Kanban pattern.
- Если Kanban отсутствует — не имитируй его промптом. Предложи обновление Hermes или временный task-log fallback.
- Если `hermes curator status` работает — Curator доступен.
- Если curator disabled — предложи включение с weekly cadence.
- Если cron недоступен — сначала почини/настрой scheduler/gateway.

Важный нюанс про версии:

- Официальный Hermes v0.12.0 — Curator release.
- В некоторых v0.12 notes Kanban мог быть reverted/under redesign.
- В post-v0.12 main/build Kanban может быть доступен.
- Всегда проверяй live командой, а не обещай по памяти.

---

## 3. Минимальная ролевая модель

Создай или опиши роли. Они могут быть отдельными Hermes profiles или устойчивыми режимами одного агента.

Рекомендуемый минимум:

1. `operator` — принимает задачи, режет на части, ставит в Kanban, делает quality gate.
2. `research` — ищет факты, источники, weak signals.
3. `technical` — проверяет runtime, код, интеграции, воспроизводимость.
4. `content` — пишет user-facing тексты, посты, документы.
5. `risk/legal` — проверяет claims, обещания, договорные и репутационные риски.
6. `finance/business` — считает ROI, renewals, money risk, если нужно.

Не плодить роли без функции. Каждая роль должна иметь:

- назначение;
- границы;
- типовые входы;
- типовые outputs;
- критерий done.

---

## 4. Kanban как обязательный слой для длинных задач

Правило:

- Простая задача до 10 минут может идти в чате.
- Длинная, многошаговая, multi-agent или risky задача должна идти через Kanban.

### 4.1. Шаблон Kanban task

Используй такой task body:

```text
Goal:
[Что должно быть готово]

Context:
[Краткий контекст, ссылки на source-of-truth, ограничения]

Assignee:
[profile/role]

Done when:
[Проверяемый критерий завершения]

Artifacts:
[Куда положить результат: report path, doc path, PR, dashboard, etc.]

Risks:
[Что нельзя сломать / раскрыть / переписать]

Verification:
[Как проверить результат]
```

### 4.2. Типовые команды

```bash
hermes kanban create
hermes kanban list
hermes kanban show <task_id>
hermes kanban assign <task_id> <profile>
hermes kanban link <parent_id> <child_id>
hermes kanban comment <task_id> "progress: ..."
hermes kanban block <task_id> "blocked: need user input"
hermes kanban unblock <task_id>
hermes kanban complete <task_id>
hermes kanban runs <task_id>
hermes kanban stats
```

### 4.3. Handoff между агентами

Когда один агент передаёт задачу другому, он обязан дать:

- task ID;
- что уже сделано;
- какие источники проверены;
- какие artifacts созданы;
- что осталось;
- blockers;
- risks;
- verification checklist.

Не передавать “разберись” без контекста.

---

## 5. Curator как weekly hygiene layer

Curator нужен для skill-библиотеки.

Рекомендуемая базовая конфигурация:

```yaml
curator:
  enabled: true
  interval_hours: 168
  stale_after_days: 30
  archive_after_days: 90
```

Проверка:

```bash
hermes curator status
```

Что Curator может делать:

- находить stale skills;
- показывать least-used / most-used;
- предлагать consolidation;
- архивировать dead agent-created skills;
- создавать umbrella skills;
- писать reports.

Что Curator НЕ должен делать без контроля:

- переписывать критичные operating rules;
- менять approval/security policy;
- менять legal/publishing workflow;
- удалять source-of-truth;
- редактировать pinned/bundled/hub skills в обход защиты;
- автоматически “улучшать” всё подряд.

Правильный процесс для critical skills:

```text
curator/audit finding
  → proposal
  → diff
  → human/operator approval
  → patch
  → verification
  → report
```

---

## 6. Daily read-only skills audit

Curator weekly. Audit daily.

Daily audit должен быть read-only. Его задача — сигналить, а не лечить.

Проверять:

- duplicate skill names;
- missing frontmatter;
- oversized skills;
- long descriptions;
- similar/overlapping skills;
- broken linked files;
- stale archive noise;
- skills without clear trigger/use case.

Минимальный fallback, если нет кастомного audit script:

```bash
hermes skills list
hermes skills check
hermes curator status
```

Если есть custom script, запускай через cron и складывай report в локальную папку reports.

Рекомендуемая частота:

```text
daily 10:30 local timezone
```

Принцип доставки:

- local report каждый день;
- user alert только при actionable failure.

---

## 7. Hourly team/gateway/cron auditor

Цель: ловить тихую деградацию.

Проверять:

- gateway status;
- profiles with enabled jobs;
- cron jobs active/failed;
- next run times;
- stale running sessions;
- missing reports;
- broken health endpoints;
- critical watchdog status.

Рекомендуемая частота:

```text
hourly, например minute 17: 17 * * * *
```

Принцип ответа:

```text
if no actionable failures:
  output: [SILENT]
else:
  alert with exact failed component, evidence, recommended next action
```

Не спамить “всё хорошо”. Это убивает доверие к alerts.

---

## 8. Knowledge / memory / skills boundary

Объясни системе и агентам разницу:

```text
Knowledge base = документы, wiki, references, source-of-truth.
Memory = короткие устойчивые факты и предпочтения.
Skills = повторяемые процедуры.
Session history = прошлые разговоры, не source-of-truth.
Kanban = текущее исполнение задач.
Curator = уборка skills.
```

Нельзя автоматически сохранять в memory/skills:

- raw chat dumps;
- API keys;
- tokens;
- passwords;
- private financial dumps;
- случайные временные TODO;
- logs без очистки;
- персональные данные без необходимости.

Если встретил secret — не печатай его. Используй `[REDACTED]`.

---

## 9. Gatekeeper policy

Для безопасной агентной организации нужен gatekeeper.

Gatekeeper может быть главным агентом или человеком.

Он утверждает:

- изменения critical skills;
- изменения config/gateway;
- изменения approval policy;
- публикации наружу;
- legal/financial claims;
- удаление/архивирование важных процедур;
- публичное раскрытие архитектуры.

Правило:

```text
Read-only checks can run automatically.
Mutating critical behavior requires approval.
```

---

## 10. Рекомендуемый порядок внедрения

### Phase 1 — Audit only

1. Проверить version/features.
2. Составить список profiles/roles.
3. Проверить current skills.
4. Включить curator status наблюдение.
5. Создать daily read-only skills audit.
6. Создать hourly gateway/cron health auditor.

Ничего критичного не переписывать.

### Phase 2 — Kanban pilot

1. Выбрать одну реальную multi-step задачу.
2. Создать parent task.
3. Разбить на 2–4 child tasks.
4. Назначить роли.
5. Потребовать artifacts.
6. Завершить через quality gate.
7. Сравнить с обычным chat workflow.

### Phase 3 — Curator governance

1. Включить weekly Curator.
2. Проверить first report.
3. Разобрать proposed consolidations.
4. Pin или защитить critical skills.
5. Разрешить Curator активно работать только с low-risk agent-created skills.
6. Для critical skills использовать proposal/diff/approval.

### Phase 4 — Operating rhythm

Ежедневно:

- skills audit;
- health reports;
- Kanban review.

Еженедельно:

- Curator report;
- skill hygiene review;
- stale tasks cleanup;
- architecture drift check.

После каждой сложной задачи:

- artifact saved;
- Kanban completed;
- lesson goes to skill only if reusable;
- memory updated only if durable fact/preference;
- no raw task noise in memory.

---

## 11. Definition of Done для внедрения

Система считается внедрённой, если:

- [ ] `hermes --version` зафиксирован.
- [ ] `hermes kanban --help` проверен или зафиксирован fallback.
- [ ] `hermes curator status` проверен.
- [ ] Роли/профили описаны.
- [ ] Есть правило: длинные задачи → Kanban.
- [ ] Есть task template.
- [ ] Curator включён weekly или есть решение почему нет.
- [ ] Daily skills audit работает read-only.
- [ ] Hourly gateway/cron auditor работает или запланирован.
- [ ] Alerts silent by default, only actionable failures.
- [ ] Critical skills/config changes require approval.
- [ ] Secrets не печатаются и не сохраняются.
- [ ] Есть report/artifact после pilot-задачи.

---

## 12. Шаблон инструкции для operator profile

Добавь в operator/system skill, если нужно:

```text
Ты оператор Hermes-based agent system.

Для простых задач отвечай прямо.
Для длинных, многошаговых, рискованных или multi-agent задач используй Kanban/task board.

Перед созданием задачи уточни:
- goal;
- context/source-of-truth;
- assignee/role;
- done criteria;
- artifacts;
- risks;
- verification.

Не сохраняй task noise в durable memory.
Reusable procedures сохраняй в skills.
Durable user/system facts сохраняй в memory.
Source-of-truth держи в wiki/docs/references.

Curator is hygiene, not dictator.
Daily audits are read-only.
Critical skills/config changes require diff and approval.
```

---

## 13. Шаблон еженедельного Curator review

```text
Weekly Curator Review

1. Run/check:
   hermes curator status

2. Review:
   - most-used skills;
   - least-used skills;
   - stale candidates;
   - archived/consolidated items;
   - proposed umbrella skills.

3. Decide:
   - safe auto-archive low-risk dead skills;
   - proposal needed for overlaps;
   - pin/protect critical skills;
   - no action.

4. For each accepted change:
   - create diff;
   - get approval if critical;
   - apply patch;
   - verify skill loads;
   - update report.
```

---

## 14. Шаблон Kanban task для multi-agent работы

```text
Title: [Task name]

Goal:
[What must be produced]

Why it matters:
[Operational value]

Context:
[Relevant docs, user request, constraints]

Assignee:
[Profile/role]

Dependencies:
- [parent/child links if any]

Artifacts:
- [expected file/report/output path]

Done when:
- [testable condition 1]
- [testable condition 2]

Risks:
- [privacy/security/reliability risk]

Verification:
- [commands/checks/manual QA]
```

---

## 15. Типовые ошибки

1. **Считать Kanban project management игрушкой.** Нет. Это execution state.
2. **Пускать Curator без governance.** Получите тихую порчу поведения.
3. **Путать audit и repair.** Audit смотрит. Repair меняет.
4. **Сохранять всё в memory.** Memory должна быть чистой и короткой.
5. **Плодить agents без boundaries.** Роли должны иметь ясные outputs.
6. **Спамить health OK.** Alerts работают только если молчат в норме.
7. **Публиковать raw dashboard.** Делайте sanitized view.
8. **Игнорировать version caveats.** Проверяйте live commands.

---

## 16. Финальная формула для агента

Если нужно объяснить владельцу системы, скажи так:

```text
Мы внедряем не “ещё одну фичу Hermes”, а операционный слой.

Kanban отвечает за то, чтобы работа не терялась.
Curator отвечает за то, чтобы procedural memory не гнила.
Daily audit отвечает за ранние сигналы.
Health auditor отвечает за gateway/cron деградацию.
Gatekeeper отвечает за безопасность критичных изменений.

Вместе это превращает набор агентов из длинного чата в управляемую AI-операционку.
```

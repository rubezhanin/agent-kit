# Implementation Plan (English)

> Canonical English version. Russian localization: [`docs/IMPLEMENTATION_PLAN.ru.md`](https://github.com/your-org/hermes-agent-architecture-kit/blob/main/docs/IMPLEMENTATION_PLAN.ru.md).

## Goal

Bring up a Hermes Agent system from scratch as a managed operational loop:

- one main operator;
- a bounded set of specialists;
- wiki / source-of-truth;
- read-only retrieval;
- Kanban for long tasks;
- safety / approval gates;
- receipts, audits and health checks.

## Phase 0. Discovery

Status: planned.

Actions:

1. Check Hermes version and available commands.
2. Check whether Kanban, Curator, cron, skills and profile list are available.
3. Identify the real `HERMES_HOME`.
4. Identify how your Hermes version wires project skills.

Must not:

- enable Kanban on assumption;
- paste a YAML blueprint blindly into runtime config;
- move secrets into Markdown.

## Phase 1. Minimal main profile

Status: planned.

Actions:

1. Create the `main-operator` profile.
2. Point the workspace at `kit/agent-center`.
3. Wire up `agent-center/AGENTS.md`.
4. Fill `owner-context/` with minimal owner rules.
5. Run the `Main Operator Triage` smoke test.

Done criteria:

- main operator correctly distinguishes a simple task from a delegation task;
- risky actions are converted to `NEEDS_APPROVAL`;
- no full source-pack loaded into context.

## Phase 2. Skills layer

Status: planned.

Actions:

1. Install / wire skills from `agent-center/skills/operations`.
2. Wire active specialist skills.
3. Leave `psychological-support` disabled.
4. Verify each skill opens its source-pack only on trigger.

Done criteria:

- `agent-creator`, `wiki-memory`, `kanban-operator`, `gateway-ux`, `token-drain`, `skill-hygiene` are available;
- specialist routing works through task brief.

## Phase 3. Knowledge layer

Status: planned.

Actions:

1. Create / fill wiki: architecture, memory policy, roster, operating contract.
2. Add source cards for key sources.
3. Set up local memory index as read-only search, if needed.
4. Forbid indexing secrets, sessions and raw private logs.

Done criteria:

- the agent searches knowledge in wiki / references;
- retrieval is not canonical truth;
- durable memory stays short.

## Phase 4. Kanban and maintenance

Status: planned.

Actions:

1. Live-check `hermes kanban --help`.
2. If available, enable the board and dispatcher per `kanban/board-contract.md`.
3. Set up read-only cron jobs from `config/cron-jobs.yaml`.
4. Enable weekly skill hygiene and token-drain diagnostics.

Done criteria:

- a long task is created as a card;
- a specialist returns a receipt;
- cron writes reports but does not modify the system without approval.

## Phase 5. Gateway UX

Status: planned.

Actions:

1. Check the current Telegram / direct gateway schema.
2. Configure ingress batching if supported.
3. Enable early ACK, partial streaming and final closure.
4. Forbid raw internal approval / tool blocks in user-facing replies.

Done criteria:

- several quick messages and a file land in one turn;
- the agent does not stay silent on long work;
- every task ends with a final answer.

## Phase 6. Optional integrations

Status: hold.

Enable separately:

- Telethon / userbot;
- the `psychological-support` profile;
- a separate Codex CLI helper;
- browser / computer-use tools;
- external accounts;
- the Telegram channel watcher.

Enable criteria:

- separate risk review;
- least-privilege access;
- draft-only default;
- negative smoke tests;
- rollback / disable plan.

## Phase 7. Telegram channel intelligence

Status: optional / hold.

Actions:

1. Researcher collects candidates into `templates/telegram-channel-candidates.md`.
2. Owner selects exact channels.
3. Technical-engineer verifies the watcher policy.
4. Pick TDLib for production; Telethon is fine for a prototype.
5. Create a dedicated watcher account — not the owner's main personal account.
6. Enable read-only monitoring only.
7. Write summaries into `integrations/telegram-channel-intelligence/reports/`.

Must not:

- mass-subscribe;
- post / comment / react;
- scrape members;
- bypass rate limits;
- keep session files in repo / wiki;
- promise that a ban is impossible.
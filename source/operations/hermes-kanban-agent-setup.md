# Hermes Kanban setup and routing guide for a subscriber's Hermes agent

Purpose: this file is for a Hermes agent/operator that needs to check, enable, configure, and use Hermes Kanban for multi-agent task routing.

Audience: a local Hermes Agent installation with one or more profiles.

Core rule:

```text
Kanban = route, don't execute.
Decompose, route, summarize.
```

## 0. Safety first

Before changing anything:

1. Do read-only discovery first.
2. Do not expose dashboard publicly.
3. Do not paste secrets, tokens, chat IDs, `.env`, session files, API keys, passwords, or raw private logs into task bodies/comments.
4. Do not run destructive commands or modify profile configs without explicit approval from the human owner.
5. Do not start both gateway-embedded dispatcher and standalone `hermes kanban daemon` against the same board.

Danger zone:

```bash
hermes dashboard --host 0.0.0.0 --insecure
```

Only use that if the owner understands that Kanban plugin routes can expose and mutate task data from the network. Default should stay localhost:

```text
127.0.0.1:9119
```

## 1. Verify that this Hermes build has Kanban

Do not assume from version number alone. Some v0.12 release notes mention Kanban being reverted while design was reworked. Check live commands.

```bash
hermes --version
hermes kanban --help
hermes dashboard --help
```

Expected: `hermes kanban --help` lists actions like:

```text
init, create, list, show, assign, link, unlink, claim, comment,
complete, block, unblock, archive, tail, dispatch, watch, stats,
runs, heartbeat, assignees, context, gc
```

If `hermes kanban` does not exist:

- stop;
- tell the owner this build does not include Kanban;
- suggest upgrading Hermes Agent to a build where Kanban is present;
- do not invent your own Kanban layer.

## 2. Understand the architecture

Hermes Kanban is inside Hermes. The browser tab is only a visual interface.

```text
Human / CLI / Gateway / Dashboard
        ↓
Kanban engine / kanban_db
        ↓
SQLite board: ~/.hermes/kanban.db
        ↓
Dispatcher inside Hermes Gateway
        ↓
Hermes profile worker: researcher / analyst / writer / reviewer / ops
        ↓
Worker tools + normal agent tools
        ↓
summary + metadata + comments + events + runs back to board
```

Important distinction:

- `delegate_task` = short synchronous subagent call inside one agent turn.
- `kanban` = durable queue and state machine for work that can outlive the current turn.

Use Kanban when:

- multiple specialists are needed;
- work is long-running;
- dependencies matter;
- review/iteration is expected;
- a human may need to intervene;
- audit trail matters;
- the task should survive restart/crash.

Use `delegate_task` when:

- the current agent needs a quick answer before continuing;
- no durable board state is needed;
- no human-in-the-loop is expected.

## 3. Initialize the board

```bash
hermes kanban init
hermes kanban stats
hermes kanban list
```

The default board is SQLite:

```text
~/.hermes/kanban.db
```

In profile-aware installations, the effective Hermes home may differ. Use commands, not guesses.

## 4. Discover available agents/profiles

```bash
hermes profile list
hermes kanban assignees
hermes kanban assignees --json
```

Build a routing table from what actually exists.

Suggested generic role map:

```text
researcher -> profile that can search/read/source facts
analyst    -> profile that can synthesize and compare
writer     -> profile that can produce final prose/artifact
reviewer   -> profile that can check facts/risks/quality
ops        -> profile that can operate services/scripts
backend    -> profile that can write backend code
frontend   -> profile that can write frontend/UI code
pm         -> profile that can write specs/acceptance criteria
```

If a generic profile does not exist:

1. Do not assign tasks to it.
2. Map the role to the closest existing specialist.
3. If no fit exists, ask the owner to create/approve a new profile.

## 5. Install/check Kanban skills

Workers should know the Kanban lifecycle. Orchestrators should know route-don't-execute behavior.

```bash
hermes skills install devops/kanban-worker
hermes skills install devops/kanban-orchestrator
hermes skills list | grep kanban
```

Notes:

- In many builds these are bundled.
- The dispatcher auto-passes `--skills kanban-worker` when spawning workers.
- Extra task-specific skills can be attached per task with `--skill <name>`.

Example:

```bash
hermes kanban create "review auth PR" \
  --assignee reviewer \
  --skill github-code-review
```

## 6. Configure dispatcher

Default and recommended: dispatcher runs inside Hermes Gateway.

Config:

```yaml
kanban:
  dispatch_in_gateway: true
  dispatch_interval_seconds: 60
```

Start gateway:

```bash
hermes gateway start
```

One-shot dispatcher pass:

```bash
hermes kanban dispatch --dry-run --max 2
hermes kanban dispatch --max 2
```

Do not normally use:

```bash
hermes kanban daemon --force
```

That standalone daemon is deprecated. Never run it together with gateway dispatcher on the same DB.

## 7. Start the visual dashboard

```bash
hermes kanban init
hermes dashboard --port 9119 --host 127.0.0.1
```

Open:

```text
http://127.0.0.1:9119/kanban
```

If direct Kanban route fails, open root and click the Kanban tab:

```text
http://127.0.0.1:9119
```

Dashboard is a thin UI. It reads/writes the same board as CLI and gateway.

Optional dashboard defaults in config:

```yaml
dashboard:
  kanban:
    default_tenant: acme
    lane_by_profile: true
    include_archived_by_default: false
    render_markdown: true
```

## 8. Create a small smoke task

Choose a real profile from `hermes kanban assignees`.

```bash
hermes kanban create "smoke: Kanban worker readiness" \
  --assignee <existing-profile> \
  --body "Reply with one short readiness line. Do not perform external actions." \
  --json
```

Watch:

```bash
hermes kanban list
hermes kanban watch
hermes kanban dispatch --max 1
```

Inspect:

```bash
hermes kanban show <task_id>
hermes kanban runs <task_id>
hermes kanban log <task_id>
```

If successful, archive the smoke card if it pollutes the board:

```bash
hermes kanban archive <task_id>
```

## 9. Worker lifecycle

When spawned by dispatcher, a worker gets Kanban env and tools.

Environment:

```text
HERMES_KANBAN_TASK
HERMES_KANBAN_WORKSPACE
HERMES_KANBAN_DB_PATH
HERMES_TENANT  # if tenant was set
```

Tools available only in Kanban worker mode:

```text
kanban_show
kanban_complete
kanban_block
kanban_heartbeat
kanban_comment
kanban_create
kanban_link
```

Worker must:

1. Call `kanban_show()` first.
2. Read title, body, comments, parent handoffs, prior attempts.
3. Work in `$HERMES_KANBAN_WORKSPACE` unless task explicitly says otherwise.
4. Send meaningful heartbeat during long work.
5. Use `kanban_block(reason=...)` if human input is needed.
6. Use `kanban_complete(summary=..., metadata={...})` when done.
7. Do not complete unfinished work.
8. Do not create follow-up tasks assigned to itself when another specialist is the right owner.

Good completion shape:

```python
kanban_complete(
    summary="Reviewed 8 sources, selected 5 reliable ones, rejected 3 weak sources.",
    metadata={
        "sources_read": 8,
        "sources_used": 5,
        "rejected": 3,
        "risk": "low"
    }
)
```

Good block shape:

```python
kanban_comment(
    task_id=os.environ["HERMES_KANBAN_TASK"],
    body="Context: two possible publication tones are viable; factual content is ready."
)
kanban_block(reason="Choose publication tone: calm expert or aggressive sales?")
```

## 10. Orchestrator workflow

An orchestrator should not do specialist work. It should create and link tasks.

Standard pattern:

```text
T1 - researcher: collect facts
T2 - researcher: collect alternatives
T3 - analyst: synthesize T1 + T2
T4 - writer: format final result
T5 - reviewer: verify and return fixes
```

CLI example:

```bash
T1=$(hermes kanban create "research: collect facts" \
  --assignee researcher \
  --body "Collect reliable facts and links. Return summary + sources." \
  --json | jq -r .id)

T2=$(hermes kanban create "research: collect alternatives" \
  --assignee researcher \
  --body "Collect alternative approaches, pros/cons, and links." \
  --json | jq -r .id)

T3=$(hermes kanban create "analysis: synthesize facts and alternatives" \
  --assignee analyst \
  --parent "$T1" --parent "$T2" \
  --body "Read parent handoffs and produce clear recommendation." \
  --json | jq -r .id)

T4=$(hermes kanban create "writing: prepare final result" \
  --assignee writer \
  --parent "$T3" \
  --body "Turn analysis into the requested format." \
  --json | jq -r .id)

hermes kanban create "review: check final result" \
  --assignee reviewer \
  --parent "$T4" \
  --body "Check facts, links, risks, clarity. Block if fixes are required."
```

If exact profiles do not exist, substitute actual profile names from discovery.

## 11. Workspaces

Use the right workspace kind.

### scratch

```bash
--workspace scratch
```

Use for research, analysis, drafts, temporary artifacts.

### dir:absolute-path

```bash
--workspace dir:/absolute/path/to/project
```

Use for persistent project folders. Path must be absolute. Treat it as trusted local access.

### worktree

```bash
--workspace worktree
```

Use for coding tasks that should happen in isolated git worktrees.

## 12. Dependencies

Create parent/child dependencies with `--parent` or `link`.

```bash
hermes kanban create "write report" --assignee writer --parent <research_task_id>
hermes kanban link <parent_id> <child_id>
```

Rule:

```text
child stays todo until all parents are done, then auto-promotes to ready
```

Do not reverse link order:

```text
parent first, child second
```

## 13. Status operations

```bash
hermes kanban assign <id> <profile|none>
hermes kanban comment <id> "text"
hermes kanban block <id> "reason"
hermes kanban unblock <id>
hermes kanban complete <id> --summary "..." --metadata '{"key":"value"}'
hermes kanban archive <id>
```

Use `blocked` when a human decision is needed. Do not guess.

## 14. Observability

```bash
hermes kanban stats
hermes kanban list
hermes kanban show <id>
hermes kanban runs <id>
hermes kanban tail <id>
hermes kanban watch
hermes kanban log <id>
hermes kanban context <id>
```

Use `runs` to diagnose retries:

- `completed` - success;
- `blocked` - worker asked for input;
- `spawn_failed` - profile/config/start failure;
- `gave_up` - circuit breaker after repeated spawn failures;
- `crashed` - process died;
- `timed_out` - max runtime exceeded;
- `reclaimed` - task was reclaimed from a stale/changed run.

## 15. Gateway/slash commands

Gateway supports `/kanban ...` surface.

Examples:

```text
/kanban list
/kanban create ...
/kanban comment <id> "..."
/kanban unblock <id>
```

Gateway-created tasks can notify the originating chat on terminal events.

Do not expose real IDs in public docs. Use placeholders:

```text
<chat_id>
<thread_id>
<task_id>
```

## 16. Troubleshooting

### `hermes kanban` command missing

The build does not include Kanban. Upgrade/switch build. Stop.

### Task stuck in `ready`

Check dispatcher/gateway:

```bash
hermes gateway status || true
hermes kanban dispatch --dry-run --max 2
hermes kanban dispatch --max 1
```

### Task stuck in `todo`

Probably waiting on parents:

```bash
hermes kanban show <id>
```

Complete parent tasks or fix links.

### Task blocked

Read reason and comments:

```bash
hermes kanban show <id>
```

Add human answer:

```bash
hermes kanban comment <id> "Decision: ..."
hermes kanban unblock <id>
```

### Spawn failures

Check profile exists and has credentials/tooling:

```bash
hermes kanban runs <id>
hermes kanban log <id>
hermes profile list
```

If profile missing, reassign or create profile after owner approval.

### Dashboard not opening

Check process and local route:

```bash
hermes dashboard --status
hermes dashboard --port 9119 --host 127.0.0.1 --no-open
curl -s --max-time 5 http://127.0.0.1:9119/ | head
curl -s --max-time 5 http://127.0.0.1:9119/kanban | head
```

Dashboard failure does not necessarily mean Kanban engine failure. Check:

```bash
hermes kanban stats
hermes kanban list
```

### Worker says unknown task id

Possible profile-board mismatch in profile-aware setups. Operator should inspect the orchestrator/current board:

```bash
hermes kanban show <task_id>
hermes kanban log <task_id>
hermes kanban list
```

Do not create a duplicate task until board path/profile routing is verified.

## 17. Public docs and source links

- Kanban overview: https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban
- Kanban tutorial: https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-tutorial
- CLI commands reference: https://hermes-agent.nousresearch.com/docs/reference/cli-commands
- Kanban Worker skill: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/devops/devops-kanban-worker
- Kanban Orchestrator skill: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/devops/devops-kanban-orchestrator
- Dashboard extension docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/extending-the-dashboard
- Hermes Agent repo: https://github.com/NousResearch/hermes-agent
- Kanban design spec PDF: https://github.com/NousResearch/hermes-agent/blob/main/docs/hermes-kanban-v1-spec.pdf
- v0.12 release notes caveat: https://github.com/NousResearch/hermes-agent/blob/main/RELEASE_v0.12.0.md

## 18. Final behavior rule for the agent

When user asks for multi-agent work:

1. Decide if Kanban is warranted.
2. If yes, discover profiles.
3. Draft task graph.
4. Ask only if routing ambiguity matters.
5. Create Kanban tasks.
6. Link dependencies.
7. Report task IDs and how to watch.
8. Do not do specialist work inside orchestrator unless no specialist exists and user explicitly approves.

Remember:

```text
Small one-shot reasoning -> answer or delegate_task.
Durable multi-stage work -> Kanban.
```

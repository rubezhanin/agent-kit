# Architecture Review (English)

> Canonical English version. Russian localization: [`docs/ARCHITECTURE_REVIEW.ru.md`](https://github.com/your-org/hermes-agent-architecture-kit/blob/main/docs/ARCHITECTURE_REVIEW.ru.md).

## Target architecture

```text
Human / Owner
  -> Gateway / CLI / Direct chat
  -> Main Operator Hermes profile
  -> Intake + risk triage
  -> Direct answer OR Kanban task
  -> Specialist profile / skill
  -> Artifact / report / receipt
  -> Quality gate
  -> Final user-facing answer
  -> Audit / health / skill hygiene / token diagnostics
```

The core idea: Hermes is the engine. A working agent system only appears after the operational loop is layered on top — workspace, sources of truth, memory, task board, routing, safety, receipts and maintenance.

## Errors found in the original set

| Problem | Why it is bad | Fix in `kit` |
| --- | --- | --- |
| No single operating contract. | Specialists and instructions can disagree. | `agent-center/AGENTS.md` makes the main operator the owner of routing and the final answer. |
| Too many agent-packs as if all should be active. | Bloats context, routing and cost; increases false delegation risk. | `team-roster.md` separates roles into active, on-demand and disabled-by-default. |
| Hermes, OpenClaw, n8n, Claude / Codex and training material mixed together. | The agent may apply foreign paths, commands and safety models. | `SOURCE_SELECTION.md` separates the Hermes deploy from reference / foreign artifacts. |
| Memory, wiki, reports and vector search mixed in places. | Durable memory becomes a junk log; retrieval starts to look like truth. | `memory-policy.md` defines the layers: wiki = truth, references = sources, reports = evidence, index = search only. |
| Kanban assumed available by version in some places. | Different builds may lack or change those features. | `kanban/board-contract.md` requires live discovery before enabling. |
| No strict UX gate for Telegram / direct. | The agent may start work before getting a file, or stay silent without a finale. | `config/gateway-telegram.yaml` and the `gateway-ux` skill: ingress batching, ACK, final closure. |
| Receipt not mandatory. | Hard to tell what the agent actually did and how it was verified. | `templates/receipt.md` and `prompts/final-report.md`. |
| High-risk roles not isolated. | Legal, economy and psychological support may sound like final expert verdicts. | Legal / economist active only as risk-review; psychological support disabled-by-default. |
| Userbot / Telethon may be treated as a normal bot. | Risk of spam, account ban, session / secret leakage. | Moved to optional integrations, not part of the base profile. |
| Telegram-channel subscription conflated with research. | The agent may start joining channels without owner choice and without limits. | Added `telegram-channel-intelligence`: researcher only proposes candidates, watcher reads only approved channels. |

## Strengths

| Strength | Description |
| --- | --- |
| Clear main / operator pattern | One agent owns intake, routing, final answer and quality gate. |
| Good base for memory hygiene | Wiki, source-of-truth layering, local memory index and a rule against dumping everything into durable memory. |
| Kanban as durable execution | Long tasks do not live in a single chat; there are statuses, assignees, dependencies and receipts. |
| Repeatable procedures through skills | Complex processes live in skill wrappers, not in one giant prompt. |
| Operational diagnostics | Token drain, skill hygiene, health / audit and gateway UX address real day-two pain. |
| Strong specialist set | Research, technical, business, marketing, design, legal risk, economy and methodologist cover most small-team AI operations. |

## Weaknesses and limits

| Weakness | What to do |
| --- | --- |
| No live Hermes config / schema in the project. | `config/*.yaml` are blueprints. Verify against your Hermes version before applying. |
| Source-packs are long. | Do not load them all into the prompt. Skills should open a source file only on a relevant task. |
| Not enough real owner data. | The first run must collect owner-context, privacy, style, domains and allowed paths. |
| Specialist overlap | Marketer / business-analyst / methodologist overlap; main operator must pick one owner per task. |
| High-stakes domains | Legal / economy / psychology should provide triage and questions, not final verdicts. |

## Agents

| Agent | Status | Does | Does not | Interaction |
| --- | --- | --- | --- | --- |
| main-operator | active | Intake, triage, routing, Kanban, final answer, quality gate. | Does not pretend to know everything; does not bypass approval. | Entry point for all tasks. |
| researcher | active | Source finding, fact-check, weak signals, public-source intelligence. | Does not write final persuasive copy without verification. | Receives research brief, returns source ledger. |
| technical-engineer | active | Setup, diagnostics, scripts, smoke tests, bounded local changes. | Does not change production / secrets without approval. | Receives task brief with allowed paths and verification. |
| business-analyst | active | Process map, automation audit, pilot design, handoff to implementation. | Does not promise revenue and does not deploy production automation. | Often starts before marketer / technical. |
| methodologist | active | Guides, lessons, instructions, knowledge packaging, agent-ready docs. | Does not invent facts and methodology out of thin air. | Uses wiki / references and output requirements. |
| marketer | active | Audience, offer, proof bank, content / experiment strategy. | Does not publish, spend budget, or make claims without proof / approval. | Often needs researcher and legal-ops review. |
| designer | active | Visual brief, style pack, prompt pack, visual QA. | Does not send private material outside without approval. | Takes meaning from marketer / methodologist. |
| legal-ops | active risk-review | Contract / claim / privacy / vendor risk triage, lawyer packet. | Does not replace a lawyer and does not give final legal advice. | Reviews marketer / business / technical outputs before external actions. |
| economist | active risk-review | ROI, subscriptions, paid pilot economics, pricing floor, runway. | Does not move money and does not give regulated advice. | Reviews monetary decisions and pilot economics. |
| agent-creator | on-demand | Designs new profiles / skills / helper-agents. | Does not create a live agent without dry-run, approval, rollback and smoke. | Invoked only by main operator. |
| psychological-support | disabled by default | Supportive conversation within safe boundaries. | Does not diagnose, treat, or replace a specialist. | Enable only as a separate profile with a crisis policy. |
| userbot-operator | disabled by default | Telegram userbot / MCP read tools, drafts, monitoring. | Does not spam, send without approval, store sessions in wiki. | Separate integration loop after a security review. |
| telegram-channel-watcher | disabled by default | Reads approved Telegram channels, summaries, weak signals. | Does not mass-subscribe, post, scrape members, or use the owner's main account. | Researcher prepares candidates, owner approves exact handles, technical-engineer sets up watcher. |

## Optimal flow

| Situation | Route |
| --- | --- |
| Simple request | main-operator answers directly. |
| Facts needed | main-operator → researcher → source ledger → final. |
| Telegram channels on a topic | main-operator → researcher → candidate list → owner approval → watcher setup. |
| Implementation / file / code | main-operator → technical-engineer → receipt → review → final. |
| Business process / automation | business-analyst → technical-engineer → legal / economist if needed. |
| Marketing / content | marketer → researcher / proof → legal-ops if claims → designer if visual. |
| Long task | main-operator creates a Kanban task with dependencies. |
| Risky action | Stop: NEEDS_APPROVAL with exact action, scope, rollback.
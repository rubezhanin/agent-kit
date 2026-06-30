# Team Roster

| Agent | Status | Trigger | Output |
| --- | --- | --- | --- |
| main-operator | Active | Every user request | Final answer, routing, Kanban task, approval request. |
| researcher | Active | Facts, sources, market/public research | Source ledger, confidence, gaps. |
| technical-engineer | Active | Setup, files, code, scripts, diagnostics | Changes, verification, receipt. |
| business-analyst | Active | Process, automation, pilot, business diagnosis | Process map, feasibility gate, risk register. |
| methodologist | Active | Guides, courses, instructions, knowledge packaging | Structured artifact and quality checklist. |
| marketer | Active | Audience, offer, content, go-to-market | Market read, proof path, experiment. |
| designer | Active | Visual concept, style, prompt pack | Visual brief, prompt pack, OTK. |
| legal-ops | Active risk-review | Contracts, claims, privacy, vendor risk | Risk flags, safer wording, escalation packet. |
| economist | Active risk-review | Money, ROI, pricing, subscriptions | Money-risk review, assumptions, missing numbers. |
| agent-creator | On-demand | Need new profile/skill/helper | Dry-run, change packet, smoke test plan. |
| psychological-support | Disabled | Explicit enable only | Supportive non-clinical conversation. |
| userbot-operator | Disabled | Separate integration project | Telegram userbot setup plan and safety gates. |
| telegram-channel-watcher | Disabled | Owner approves exact Telegram channels for monitoring | Read-only channel summaries and source-referenced reports. |

## Routing Notes

- If a task spans multiple agents, main-operator creates Kanban tasks with dependencies.
- If two agents overlap, choose one owner and request reviews from others.
- Do not run high-risk specialists as autonomous decision makers.
- Researcher may find Telegram channel candidates, but only owner-approved channels can be joined/read by a watcher.

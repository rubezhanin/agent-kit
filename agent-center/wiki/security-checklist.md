# Security Checklist

> Canonical English version. The reference pack with more detail lives at `source/operations/security-checklist-for-agent.md`. This page is a concise, source-agnostic checklist for the kit.

The kit is conservative by design, but security is a moving target. This page keeps the kit aligned with the OWASP LLM Top 10, MCP security guidance, and operational hardening for Hermes-style agents.

## Security Levels

Choose a level before exposing anything:

| Level | Use when | Required controls |
| --- | --- | --- |
| Green — Open | Single user on a personal Mac/Linux. | Token storage, basic `.gitignore`, agent runs in user context. |
| Yellow — Standard | Shared machine, family, internal LAN. | Above + firewall on the gateway, approval for destructive actions, Telegram privacy mode. |
| Red — Paranoid | VPS, public IP, multi-user, regulated work. | Above + monitoring, alerts, monthly token rotation, full audit cron. |

## Hard rules

These are non-negotiable for any level:

- **Secrets never in chat.** All tokens, API keys, session files, `.pem`, cookies live in `.env` or in the OS secret store. `agent-center/` and the kit repo must not contain them.
- **The gateway is never public.** Bind it to `localhost` or a private LAN; reach it from outside through Tailscale / Cloudflare Tunnel / SSH.
- **Reads outside the workspace require explicit approval.** `HERMES_KIT_LOCK_OUTSIDE_WORKSPACE=true` is the default.
- **External content is untrusted.** Treat every web-fetch, every PDF, every email body as data, not instructions.
- **Skills are read before installed.** Diff `SKILL.md`, run a smoke test, audit `eval`, `exec`, `curl`, `NODE_OPTIONS`, `base64`, `process.env` patterns.

## OWASP LLM Top 10 (2025) — what this kit does

| OWASP ID | Risk | What the kit enforces |
| --- | --- | --- |
| LLM01 | Prompt injection | External content is untrusted. Stop rules block auto-responding to "ignore previous" patterns. Receipts require source-of-truth quoting. |
| LLM02 | Sensitive info disclosure | `wiki/` is canonical; `references/` is local. `memory index` is read-only search. No secrets in chat. |
| LLM03 | Supply chain | All skills are first-party in this repo. `profile-factory` requires owner approval before adding a third-party skill. |
| LLM04 | Data / model poisoning | `wiki/memory-policy.md` limits durable memory. Memory index never trusted as truth. |
| LLM05 | Improper output | Skills return a structured `output` field. Receipts include `command/check result`. |
| LLM06 | Excessive agency | Stop rules in `agent-center/AGENTS.md`. Telegram watcher disabled by default. Production actions require approval. |
| LLM07 | System prompt leak | Prompts are short, structured, and reference wiki pages for long detail. `prompts/*.md` are version-controlled and visible. |
| LLM08 | Vector weaknesses | Memory index is read-only; `top_k` is capped (`memory_policy.memory_index.top_k_default: 5`). |
| LLM09 | Misinformation | Receipts separate facts from assumptions; researcher returns source ledger, legal-ops / economist flag risky claims. |
| LLM10 | Unbounded consumption | `hermes-token-drain-diagnostic` skill is bundled; `reports/audits/` holds weekly diagnostics. |

## Telegram / gateway hardening

- Bind gateway to `localhost`.
- Enable Telegram BotFather privacy mode.
- Never reuse the owner's main personal account for a watcher.
- Keep session files out of the repo (see `.gitignore`).
- Use TDLib (production) or Telethon (prototype) instead of ad-hoc HTTP bots.

## Memory and data

- `wiki/` is canonical.
- `references/` holds long sources, never secrets.
- `owner-context/` holds preferences and boundaries, never secrets.
- `reports/` holds receipts, audits and incidents.
- Durable memory stores only short stable facts — see `wiki/memory-policy.md`.
- Memory index is read-only search, never canonical.

## Supply chain: skills and MCP

Before installing a third-party skill:

```bash
# audit a skill folder
grep -rE "NODE_OPTIONS|curl|wget|http[s]?://|eval\(|exec\(|process\.env" skills/<name>/SKILL.md
grep -rE "\.ssh|\.aws|\.gnupg|openclaw\.json|\.pem|\.key" skills/<name>/
```

Before installing an MCP server:

```bash
# pin the version
cat ~/.hermes/mcp.json
# read the server source
less $path-to-server
# sandbox egress via toolhive / Docker
docker run --rm toolhive serve --sandbox
```

## Monitoring crons

The kit ships a blueprint in `agent-center/config/cron-jobs.yaml`. Recommended active jobs:

- `daily-health-report` — workspace presence, profile availability, gateway status.
- `weekly-skills-hygiene-audit` — duplicates, oversize, stale routing descriptions.
- `weekly-token-drain-diagnostic` — token-drain evidence, no auto-fix.
- `nightly-worklog-digest` — daily summary.

See `agent-center/templates/receipt.md` and `agent-center/templates/audit.md` (if present) for the output format.

## Final checklist (15 points)

| ☑ | Item | Level |
| --- | --- | --- |
| ☐ | `chmod 600` on `.env` and local config | 🔴 |
| ☐ | Gateway bound to localhost / LAN | 🔴 |
| ☐ | No tokens in `memory/`, no tokens in git | 🔴 |
| ☐ | Owner approval: deletion, POST, config edits | 🔴 |
| ☐ | Skill code grepped for `curl`, `eval`, `NODE_OPTIONS` | 🔴 |
| ☐ | MCP servers: source read before connecting | 🔴 |
| ☐ | External content marked untrusted | 🟡 |
| ☐ | Firewall configured | 🟡 |
| ☐ | `.gitignore` covers `.env`, `*.pem`, `secrets/` | 🟡 |
| ☐ | Telegram privacy mode on | 🟡 |
| ☐ | Local SQLite / index in WAL mode | 🟡 |
| ☐ | Token rotation every 90 days | 🟡 |
| ☐ | Skill hashes recorded in reports | 🟡 |
| ☐ | Outbound connections monitored | 🟡 |
| ☐ | Memory cleanup on schedule | 🟢 |

## References in this repo

- `source/operations/security-checklist-for-agent.md` — full upstream pack.
- `agent-center/AGENTS.md` — operating contract (Stop rules, source of truth).
- `agent-center/skills/operations/skill-hygiene-audit/SKILL.md` — read-only audit skill.
- `agent-center/skills/operations/hermes-token-drain-diagnostic/SKILL.md` — token diagnostic.

## External references

- OWASP Top 10 for LLM Applications — `genai.owasp.org`.
- MITRE ATLAS — `atlas.mitre.org`.
- MCP Security Checklist — `github.com/slowmist/MCP-Security-Checklist`.
- Invariant Labs on Tool Poisoning.
- Wiz Security — agent / MCP write-ups.
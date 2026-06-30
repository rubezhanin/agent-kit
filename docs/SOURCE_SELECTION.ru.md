# Source Selection (English)

> Canonical English version. Russian localization: [`docs/SOURCE_SELECTION.ru.md`](https://github.com/your-org/hermes-agent-architecture-kit/blob/main/docs/SOURCE_SELECTION.ru.md).

## Moved into `kit/source`

| Group | Files | Why |
| --- | --- | --- |
| Core | `main-agent-architecture-kit.md`, `hermes-agent-setup-guide.md`, `all-in-one-agent-stability-kit.md`, `context-management-guide.md`, `adaptive-agent-creator-kit.md` | Define the main Hermes loop: role, workspace, memory, skills, delegation, context, creating new agents. |
| Memory / knowledge | `llm-wiki-hermes-obsidian-agent-setup.md`, `agent-user-local-embedding-brief.md` | Needed for the wiki / source-of-truth and read-only retrieval layer. |
| Operations | Kanban / Curator, token-drain, ingress batching, ACK / final closure, security, skill hygiene | The day-two layer: tasks, UX, diagnostics, security, skills control. |
| Specialists | methodologist, designer, marketer, business analyst, researcher, technical engineer, Codex CLI, legal ops, economist, psychological support, Kaizen Ikigai, chatgpt-carousel-agent-kit | Agent / skill packs for specialist roles. Most are adapted into `agent-center/`; chatgpt-carousel is exposed as a disabled-by-default profile (`carousel-creator`). |
| Optional integrations | Telethon userbot setup and install-agent | Relevant only if Telegram userbot / MCP is needed; not enabled by default due to risk. |

## Imported into `agent-center/wiki/`

The following `source/` packs informed dedicated wiki pages inside `agent-center/wiki/`:

| Source file | Wiki page (English) |
| --- | --- |
| `source/core/context-management-guide.md` | `agent-center/wiki/context-management.md` |
| `source/memory-knowledge/agent-user-local-embedding-brief.md` | `agent-center/wiki/local-embedding.md` |
| `source/operations/security-checklist-for-agent.md` | `agent-center/wiki/security-checklist.md` |

## Left in `files`

| Type | Reason |
| --- | --- |
| PDF / audio courses on context engineering, RAG, memory, workflow, security | These are training and reference material, not deploy configs. |
| n8n JSON workflows (`TRENER`, `SOVETNIK`, `MARKETOLOG`, etc.) | These are n8n / OpenAI / Supabase / OpenClaw-style workflows, not Hermes profile config. Risk of mixing architectures. |
| OpenClaw / Claude setups and breakdowns | Useful as ideas, but should not become the basis of a Hermes build. |
| `MEMORY-UPGRADE new.md`, `БАЗОВЫЙ-ПАКЕТ-АГЕНТА.md` | Locked into OpenClaw paths and unsafe patterns like asking for an API key in chat. |
| ZIP / thumbnails / media | Not needed for a Hermes deploy kit. |

## Selection criterion

A file was moved if it helps:

- create a Hermes profile, skill, agent role or workspace;
- configure memory, wiki, retrieval, Kanban, cron / audit or gateway UX;
- define a safe specialist role;
- improve operations and diagnostics of Hermes Agent.

A file was **not** moved if it:

- only teaches but does not configure;
- belongs to a different platform;
- contains risky setups without Hermes adaptation;
- duplicates an already-included MD file as PDF.
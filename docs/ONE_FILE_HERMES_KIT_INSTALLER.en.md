# One-File Hermes Kit Installer (English)

> Canonical English version. Russian localization: [`docs/ONE_FILE_HERMES_KIT_INSTALLER.ru.md`](docs/ONE_FILE_HERMES_KIT_INSTALLER.ru.md).

You can hand this single file to a clean Hermes agent.

The agent's task: walk the owner through installing and configuring the `Hermes Agent Architecture Kit` in a dialog:

- workspace center;
- memory and wiki;
- profiles / agents;
- skills;
- Kanban / Curator, if available;
- gateway UX;
- Telegram channel intelligence;
- optional bots / watchers;
- smoke tests and receipts.

## 0. Role of the installer agent

You are the Hermes setup operator.

Your job is **not** to apply everything at once — it is to walk the owner through configuration safely.

Work like this:

1. Dialog and discovery first.
2. Then a dry-run plan.
3. Then approval on a concrete change package.
4. Then install.
5. Then smoke tests.
6. Then receipt.

You must **not**:

- ask for tokens, passwords, session files or API keys in chat;
- write into foreign directories;
- modify existing Hermes config without backup / diff / approval;
- enable Telegram / userbot / Telethon / TDLib without a separate approval;
- promise that a Telegram account will not be banned;
- assume Kanban / Curator are available without a live check.

## 1. Find the kit

First, locate the kit folder.

Expected structure:

```text
kit/
  README.md
  GITHUB_INSTALL.md
  ADDING_PROFILES.md
  kit-manifest.json
  ONE_FILE_HERMES_KIT_INSTALLER.md
  AGENT_SKILL_MATRIX.md
  ARCHITECTURE_REVIEW.md
  IMPLEMENTATION_PLAN.md
  SOURCE_SELECTION.md
  agent-center/
    AGENTS.md
    config/
    profiles/
    skills/
    wiki/
    kanban/
    templates/
    integrations/
  source/
  scripts/
  install.ps1
  install.sh
```

If `kit/agent-center/AGENTS.md` is not found, stop and ask the owner for the correct path.

## 2. First reply to the owner

Start like this:

```text
I will walk you through the Hermes Agent Architecture Kit install step by step.

I will not change anything yet. I will run discovery, ask a few short questions, prepare a dry-run plan, and only start configuration after your approval.

I need a few clarifications:
1. Is this a fresh Hermes install, or do you already have a working profile?
2. Where is HERMES_HOME / the profile, if you know it?
3. Do you want one main agent or a team of profiles?
4. Do you want a Telegram gateway?
5. Do you want a Telegram channel watcher for reading channels?
6. May I create files inside kit/agent-center and the profile skills directory?
```

Ask questions in blocks of no more than 5–7 at a time.

## 3. Discovery checklist

Gather facts. Do not modify files.

Check:

```text
- current working directory
- kit path
- kit/agent-center exists
- Hermes CLI availability
- Hermes version
- HERMES_HOME
- profile list
- skills list
- kanban help
- curator status / help
- cron list / help
- gateway status / config path, if available
```

If a command is unavailable, do not invent state. Write `not available` and continue with a safe fallback.

## 4. Minimum architecture

Target layout:

```text
Owner
  -> main-operator profile
  -> skills
  -> wiki / source-of-truth
  -> memory index optional
  -> Kanban optional
  -> specialist profiles / skills
  -> reports / receipts
  -> optional Telegram watcher
```

Main file:

```text
kit/agent-center/AGENTS.md
```

Main skill matrix:

```text
kit/AGENT_SKILL_MATRIX.md
kit/agent-center/skills/README.md
kit/agent-center/config/profiles.yaml
kit/agent-center/wiki/team-roster.md
```

## 5. Dry-run plan

After discovery, return a dry-run to the owner:

```md
# Hermes Kit Dry-Run Plan

## Found
- kit path:
- Hermes version:
- HERMES_HOME:
- profiles:
- skills:
- Kanban:
- Curator:
- Cron:
- Gateway:

## Proposed install
- main operator:
- workspace:
- skills to install:
- profiles to create / update:
- memory / wiki:
- kanban:
- telegram:

## Files to create / change
| Action | Path | Why |
| --- | --- | --- |

## Needs approval
- ...

## Will not touch
- secrets
- existing sessions
- production configs without backup
- Telegram account sessions
```

Stop and ask:

```text
Do you approve this change package? You can answer:
- approve minimal
- approve full without Telegram
- approve with Telegram discovery only
- change plan
```

## 6. Install modes

### Minimal

Install:

- `agent-center/AGENTS.md`;
- `config/hermes-target-profile.yaml` as a blueprint;
- `config/profiles.yaml`;
- `wiki/architecture.md`;
- `wiki/memory-policy.md`;
- `wiki/team-roster.md`;
- `wiki/operating-contract.md`;
- `templates/receipt.md`;
- `templates/smoke-tests.md`.

### Full without Telegram

Minimal plus:

- operations skills;
- specialist skills;
- Kanban contract;
- cron blueprint;
- skill hygiene;
- token-drain diagnostic.

### With Telegram discovery only

Full without Telegram plus:

- `telegram-channel-intelligence` skill;
- `templates/telegram-channel-candidates.md`;
- no watcher account;
- no join / subscription;
- no session files.

### With Telegram watcher

Only after separate approval.

Adds:

- `integrations/telegram-channel-intelligence/`;
- `channel-registry.yaml`;
- `watcher-policy.yaml`;
- selected runtime plan: TDLib preferred, Telethon prototype.

## 7. Skills install

Source skills live in:

```text
kit/agent-center/skills/
```

If Hermes supports project-local skills, keep them there.

If Hermes requires a per-profile skills directory, copy them into:

```text
<HERMES_HOME>/profiles/<PROFILE_NAME>/skills/
```

Before copying:

1. verify the target path;
2. back it up if it already exists;
3. do not overwrite without approval;
4. preserve folder names;
5. run `skills list` after install.

Core operations skills:

```text
agent-creator
profile-factory
wiki-memory
kanban-operator
gateway-ux
skill-hygiene-audit
hermes-token-drain-diagnostic
telegram-channel-intelligence
```

Specialist skills:

```text
researcher
technical-engineer
business-analyst
methodologist
marketer
designer
legal-ops
economist
```

Optional:

```text
psychological-support
```

Disabled by default:

```text
telegram-channel-watcher
userbot / Telethon / TDLib runtime
```

## 8. Profiles setup

Use `kit/agent-center/config/profiles.yaml` as the source map.

Machine-readable profiles live here:

```text
kit/agent-center/profiles/*.profile.json
```

The GitHub installer scans this directory on every run. If a new profile file is added, the installer should pick it up without code changes.

Recommended profiles:

| Profile | Required | Notes |
| --- | --- | --- |
| `main-operator` | yes | Main entry point. |
| `profile-factory` | recommended | Creates new profiles and skills from owner descriptions. |
| `researcher` | recommended | Can also be skill-only in a small setup. |
| `technical-engineer` | recommended | Setup / diagnostics / verification. |
| `business-analyst` | optional active | Useful for automation / process work. |
| `methodologist` | optional active | Useful for guides / instructions. |
| `marketer` | optional active | Useful for content / offers. |
| `designer` | optional active | Useful for visuals. |
| `legal-ops` | optional risk-review | Not legal advice. |
| `economist` | optional risk-review | Read-only money analysis. |
| `psychological-support` | disabled | Separate safety review. |
| `telegram-channel-watcher` | disabled | Separate Telegram / account safety review. |

If the owner wants a simple setup, do not create many profiles. Use the main profile + skills first.

## 8A. Creating profiles from description

If the owner asks for a new agent / profile, use `profile-factory`.

Do not create a live profile immediately.

Workflow:

1. Ask intake questions.
2. Create a role card.
3. Propose skills and tools.
4. Define safety policy and approval gates.
5. Return a dry-run change packet.
6. Ask for approval.
7. Create files:
   - `agent-center/profiles/<slug>.profile.json`;
   - `agent-center/skills/<group>/<slug>/SKILL.md`;
   - optional smoke test.
8. Update the receipt.

CLI helper if available:

```text
python scripts/create_profile_skeleton.py "<Agent Name>" --description "<what it does>" --group specialists
```

## 9. Memory and wiki setup

Use:

```text
kit/agent-center/wiki/
kit/agent-center/owner-context/
kit/agent-center/references/
kit/agent-center/reports/
```

Rules:

- wiki is canonical;
- references store long source docs;
- owner-context stores preferences and boundaries, not secrets;
- reports store receipts and audits;
- durable memory stores only short stable facts;
- the memory index is search, not truth.

Ask the owner:

```text
What 3–5 stable facts about me / the project may I store?
Which directories may I read?
Which directories must I never read?
Which actions always require your approval?
```

## 10. Kanban setup

Before enabling:

```text
hermes kanban --help
hermes dashboard --help
```

If unavailable:

- do not fake Kanban;
- use `reports/task-receipts/` as a temporary task log;
- suggest an upgrade later.

If available:

- initialise the board only after approval;
- default dashboard localhost only;
- no public insecure dashboard;
- create one smoke task.

## 11. Gateway UX setup

Use:

```text
kit/agent-center/config/gateway-telegram.yaml
kit/agent-center/skills/operations/gateway-ux/SKILL.md
```

Desired behavior:

- ingress batching: 0.8–1.5 seconds;
- busy mode: queue;
- partial streaming if supported;
- early ACK for visible work;
- mandatory final closure;
- never show raw approval / internal tool blocks to the user.

Do not edit gateway config without backup and approval.

## 12. Telegram channel intelligence

This is optional and disabled by default.

### What the user wants

Example:

```text
Researcher finds Telegram channels about AI agents.
Owner selects interesting channels.
Watcher monitors approved channels.
Researcher summarises and analyses them.
```

### Correct architecture

```text
researcher -> candidate list -> owner approves exact handles -> dedicated watcher account -> TDLib read-only watcher -> reports -> researcher analysis
```

### Bot API vs TDLib vs Telethon

Use this policy:

| Option | Use when | Notes |
| --- | --- | --- |
| Bot API | You own / admin the channel or can add the bot to it | Not for arbitrary user-like subscriptions to third-party channels. |
| TDLib | Production read-only watcher | Preferred. Official Telegram client library. |
| Telethon | Prototype / local lightweight watcher | Useful, but keep conservative limits. |
| Manual export / forward | Lowest-risk occasional analysis | No automated joining. |

### Anti-ban rules

Never promise "no ban".

Default:

- dedicated watcher account;
- no owner's main account;
- no bulk joining;
- no posting / commenting / reacting;
- no DM;
- no member scraping;
- no invite automation;
- no bypassing rate limits;
- no raw session files in repo / wiki;
- no training / fine-tuning datasets;
- per-channel owner approval.

### Dialog flow

Researcher first returns:

```text
Here are candidate channels:
1. @...
2. @...

Which exact handles do you approve for monitoring?
```

Owner approval must be exact:

```text
I approve monitoring:
- @channel1
- @channel2
```

Then `technical-engineer` prepares the watcher setup plan.

Joining / subscribing is a separate approval from discovery.

## 13. Smoke tests

Run:

```text
kit/agent-center/templates/smoke-tests.md
```

Add a Telegram smoke test if enabled:

```text
Ask the researcher to find 3 candidate channels for a harmless topic.
Expected: candidate list only, no joining.
Approve one fake / test channel or hold.
Expected: no watcher setup without exact approval.
```

## 14. Final receipt

After install, write:

```md
# Hermes Kit Install Receipt

## Date

## Kit path

## Hermes profile

## Installed
- ...

## Skills
- ...

## Profiles
- ...

## Memory / wiki
- ...

## Kanban
- available / unavailable / not enabled

## Gateway
- ...

## Telegram
- disabled / discovery only / watcher planned / watcher enabled

## Smoke tests
- ...

## Not touched
- secrets
- sessions
- production
- Telegram account sessions

## Next actions
- ...
```

Save the receipt to:

```text
kit/agent-center/reports/task-receipts/
```

## 15. If unsure

If anything is unclear, ask.

Do not guess paths.

Do not silently apply risky changes.

Do not install optional integrations just because they exist.
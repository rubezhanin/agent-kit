---
name: telegram-channel-intelligence
description: Use when discovering, approving, subscribing to, reading, monitoring or analyzing Telegram channels. Uses safe read-only watcher architecture, TDLib-first recommendation, explicit approval and anti-ban limits.
---

# Telegram Channel Intelligence

Use this skill when the user wants agents to:

- find Telegram channels by topic;
- rank candidate channels;
- ask the owner which channels are worth watching;
- subscribe a dedicated watcher account to selected channels;
- read and summarize channel posts;
- detect weak signals, repeated pains, competitor moves or market themes.

## Core Rule

Do not treat Telegram as a free scraping surface.

Default mode:

```text
discover candidates -> owner approves exact channels -> watcher reads only -> reports/summaries -> no posting, no DM, no spam
```

## Recommended Architecture

Preferred production path:

```text
Researcher
  -> candidate channel list
  -> owner approval
  -> dedicated Telegram watcher account
  -> TDLib read-only watcher service
  -> local SQLite/raw cache with retention
  -> summaries/reports
  -> main operator / researcher
```

Prototype path:

```text
Telethon read-only watcher
```

Bot API path:

```text
Only for channels where the bot is explicitly added/admin and allowed to receive channel posts.
Not for subscribing to arbitrary third-party channels.
```

## Why TDLib First

TDLib is Telegram's official client library. For a long-lived watcher, prefer TDLib because it is designed as a Telegram client runtime.

Telethon is useful for a prototype and is widely used, but it is still an unofficial MTProto client library. It can be acceptable if used conservatively, but do not build risky bulk automation on it.

## Anti-Ban Policy

Never promise "no ban".

Use these guardrails:

- dedicated watcher account, not the owner's main personal account;
- human creates/owns the account;
- normal human account setup before automation;
- no bulk joining;
- no rapid join/leave loops;
- no posting, commenting, reacting, DM, invites or forwarding by default;
- no contact scraping;
- no mass export;
- no use for training/fine-tuning models;
- per-channel approval before join;
- keep a channel registry with reason, owner approval and date;
- slow polling / event handling;
- backoff on rate limits and errors;
- retention policy for raw posts;
- easy disable switch.

## Workflow

1. Researcher finds candidate channels.
2. Researcher returns `telegram-channel-candidates.md`.
3. Owner selects channels to monitor.
4. Main operator asks:
   - use manual join only;
   - allow per-channel assisted join;
   - hold until technical setup.
5. Technical engineer sets up watcher in read-only mode.
6. Watcher writes local reports, not public messages.
7. Researcher analyzes reports and cites channel/date/message references.

## Approval Gate

Before subscribing/joining, ask:

```text
I found these candidate Telegram channels:

1. @channel - reason
2. @channel - reason

Which ones should the watcher account monitor?

Approve exact handles only. I will not join unapproved channels.
```

## Output Files

Recommended:

```text
integrations/telegram-channel-intelligence/
  README.md
  channel-registry.yaml
  watcher-policy.yaml
  reports/
  cache/
```

## Stop Rules

Stop and ask approval if asked to:

- join more than 5 channels in one batch;
- read private groups/chats;
- scrape members;
- DM users;
- post/comment/react;
- bypass rate limits;
- use the owner's main account;
- store session files in repo/wiki;
- export raw posts outside the local workspace;
- train/fine-tune a model on Telegram content.


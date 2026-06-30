# Telegram Channel Intelligence

Optional integration for reading and analyzing Telegram channels through a dedicated read-only watcher account.

This integration is disabled by default.

## What This Solves

Example workflow:

1. Researcher finds channels about a topic.
2. Owner selects interesting channels.
3. Watcher account monitors approved channels.
4. Researcher analyzes posts and returns summaries, weak signals and source references.

## Recommended Implementation

| Option | Use For | Notes |
| --- | --- | --- |
| Bot API | Owned/admin channels | A bot can receive channel post updates only where it is present/allowed. It cannot behave like a user subscribed to arbitrary public channels. |
| TDLib watcher | Production read-only monitoring | Preferred. Official Telegram client library, good fit for a dedicated watcher account. |
| Telethon watcher | Prototype or lightweight local setup | Useful, but treat as unofficial client automation. Keep conservative limits. |
| Manual export | Lowest-risk occasional analysis | Human exports or forwards selected posts. No automated subscription. |

## Safe Default

```text
manual candidate review
dedicated watcher account
read-only
no posting
no DMs
no scraping members
no bulk joins
no raw session files in repo
```

## Files

| File | Purpose |
| --- | --- |
| `channel-registry.yaml` | Approved channels and monitoring reasons. |
| `watcher-policy.yaml` | Limits, retention and allowed actions. |
| `reports/` | Summaries and analysis outputs. |
| `cache/` | Local raw/normalized post cache if enabled. Do not sync publicly. |

## Human Approval Required

Approval is required before:

- creating watcher session;
- joining any channel;
- reading private groups/chats;
- increasing limits;
- exporting raw content;
- enabling send/post/comment/react.


# One-file installer

> Mirrors `docs/ONE_FILE_HERMES_KIT_INSTALLER.en.md`. Russian: [here](https://github.com/rubezhanin/agent-kit/blob/main/docs/install/one-file.md).

You can hand the one-file installer to a clean Hermes agent. The agent walks the owner through the install in dialog mode.

## Installer role

The agent is a `setup-operator`. Its job:

1. Discovery — never write before asking.
2. Dry-run plan — show every change before applying.
3. Approval — get explicit consent for the change package.
4. Install — only after approval.
5. Smoke tests — run `agent-center/templates/smoke-tests.md`.
6. Receipt — write to `agent-center/reports/task-receipts/`.

## Forbidden during install

- Asking for tokens, passwords, session files or API keys in chat.
- Writing into foreign directories.
- Editing existing Hermes config without backup / diff / approval.
- Enabling Telegram / userbot / Telethon / TDLib without a separate approval.
- Promising "your Telegram account will not get banned".
- Assuming Kanban / Curator commands exist.

## Flow at a glance

```text
owner
  │  "I want to install the kit"
  ▼
installer agent
  │  discovery checklist
  ▼
dry-run plan
  │  owner approval (approve minimal / full / discovery-only / change plan)
  ▼
install (one of: minimal / full / discovery-only / with-watcher)
  │  smoke tests
  ▼
final receipt (saved under reports/task-receipts/)
```

For the full dialog script, see [`docs/ONE_FILE_HERMES_KIT_INSTALLER.en.md`](https://github.com/rubezhanin/agent-kit/blob/main/docs/ONE_FILE_HERMES_KIT_INSTALLER.en.md) in the repository.
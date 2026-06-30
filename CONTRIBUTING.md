# Contributing

Thanks for taking an interest in `hermes-agent`. This document explains how to file issues, propose changes, and submit pull requests.

> **Ground rule:** keep changes **small and focused**. One profile, one skill, one doc change per PR — not a kitchen-sink refactor.

## Code of conduct

By participating you agree to keep the discussion respectful and on-topic. No harassment, no spam, no unsolicited promotion of competing kits.

## Filing issues

Use the issue templates under `.github/ISSUE_TEMPLATE/`:

- `bug_report.md` — something in the kit doesn't work as documented.
- `feature_request.md` — a new profile, skill, or capability.
- `profile_proposal.md` — a fully-formed proposal for a new specialist profile.

Always include:

- kit version (`kit-manifest.json` → `version`),
- OS and shell (`Windows / PowerShell 7`, `Ubuntu 22.04 / bash 5.1`, etc.),
- the exact command you ran,
- the install receipt from `reports/task-receipts/` if any.

## Working locally

```bash
git clone https://github.com/rubezhanin/agent-kit
cd hermes-agent
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\Activate.ps1 on Windows
pip install -r requirements-dev.txt   # when present
```

Always validate a change with:

```bash
python scripts/setup_kit.py --dry-run --workspace ./tmp-dry-run-workspace
```

The dry run must end with `Done.` and a non-zero `profile_count` only if you actually added profiles.

## Repository conventions

- **Language.** English is canonical. Russian localization lives in `.ru.md` siblings. Do not mix languages inside one file.
- **Profile files** live in `agent-center/profiles/<slug>.profile.json` and follow the schema documented in `docs/ADDING_PROFILES.en.md`.
- **Skill files** live in `agent-center/skills/<group>/<slug>/SKILL.md` (`group ∈ { operations, specialists, optional }`).
- **Prompts** go in `agent-center/prompts/`. Keep them short and reference wiki pages for long explanations.
- **Wiki** is canonical. If you change behavior, update the matching wiki page and the matching `.ru.md` if there is one.
- **Source MD-packs** under `source/` are reference material. They are not consumed by the installer and are not localised; don't touch them unless you are deliberately refreshing source material.

## Translation policy

- English first; Russian as a convenience.
- When translating, keep technical terms, file paths, and code identifiers in their original form.
- Update both `docs/<doc>.en.md` and `docs/<doc>.ru.md` in the same PR.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```text
feat(profiles): add copy-editor specialist profile
fix(installer): do not fail when --workspace is the same path
docs(readme): clarify quick-start for Windows
chore(gitignore): ignore .env
```

## Pull requests

1. Fork and create a topic branch (`feat/copy-editor`, `fix/dry-run-path`, ...).
2. Make the change, run the dry-run installer.
3. Update `CHANGELOG.md` under `[Unreleased]`.
4. Open the PR using `.github/PULL_REQUEST_TEMPLATE.md`.
5. Wait for at least one review. Expect review comments — the kit is conservative by design.

## Release process

1. Bump `kit-manifest.json` `version`.
2. Move `[Unreleased]` items in `CHANGELOG.md` into a dated section.
3. Tag and push: `git tag -s v0.x.y && git push origin v0.x.y`.
4. Update the GitHub release notes from the changelog.

## Security

If you find a security issue (secrets leak, unsafe installer flag, ...), **do not** open a public issue. Email the maintainer privately (see `SECURITY.md` if present) or use GitHub's "Report a vulnerability" feature.
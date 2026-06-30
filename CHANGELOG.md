# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.1] — Origin Return Protocol

### Added
- **Origin Return Protocol** as the first layer of agent operations.
  - Skill wrapper `agent-center/skills/operations/origin-return-protocol/SKILL.md`.
  - Reference text in `agent-center/operations/origin-return-protocol/PROTOCOL.en.md` and `PROTOCOL.ru.md`.
  - Wiki page `agent-center/wiki/origin-return-protocol.md` (with `origin-return-protocol.ru.md` mirror).
  - Docs page `docs/ORIGIN_RETURN_PROTOCOL.en.md` mirrored on the MkDocs site under `Architecture → Origin Return Protocol`.
  - Five anchors (`origin`, `owner`, `artifact`, `status`, `return_path`) and four statuses (`DONE` / `BLOCKED` / `NEEDS_APPROVAL` / `STALE`) enforced across the operator layer.

### Changed
- `agent-center/AGENTS.md` and `AGENTS.ru.md` — added a "First rule" block at the top; switched to the Origin Return final-answer shape; tightened status vocabulary.
- `agent-center/prompts/main-agent-system.md` — loads the protocol; final report must use the new shape.
- `agent-center/prompts/final-report.md` (+ `.ru.md`) — replaced the prior shape with the protocol summary.
- `agent-center/templates/receipt.md` — receipts now carry `origin / owner / assignee / artifact / status / returned to / verification / blocked / outcome / next step`.
- `agent-center/templates/task-card.md` — task cards now carry the five anchors by default.
- `agent-center/profiles/main-operator.profile.json` — `skills` list now includes `origin-return-protocol`.
- `agent-center/skills/README.md` (+ `.ru.md`) — Operations table now mentions `origin-return-protocol` and `carousel-creator`.
- `docs/AGENT_SKILL_MATRIX.en.md` (+ `.ru.md`) — every active profile row explicitly notes that it loads `origin-return-protocol`.
- `mkdocs.yml` — Architecture nav gained `Origin Return Protocol`; nav translations added.

## [0.3.0] — Publication build

### Added
- **MkDocs documentation site.** `docs_site/en/` and `docs_site/ru/`; Material theme, `static-i18n`, include-markdown-plugin, redirects, gen-files.
- **GitHub Actions CI.** `.github/workflows/ci.yml` validates JSON / YAML, runs `python scripts/setup_kit.py --dry-run`, and runs the locale-sanity check.
- **GitHub Actions docs deploy.** `.github/workflows/docs.yml` builds and publishes to GitHub Pages.
- `requirements-docs.txt`, `requirements-dev.txt`, `pyproject.toml`.
- `scripts/check_release.py`, `scripts/check_locale_sanity.py`.
- Badges in `README.md` / `README.ru.md`.
- Wiki pages: `security-checklist.md`, `context-management.md`, `local-embedding.md`.
- Optional integration `carousel-creator/` wrapping the upstream `chatgpt-carousel-agent-kit` pack.
- File rename sweep of `source/` to clean kebab-case names.
- `setup_kit.py` improvement: `--dry-run` no longer requires `--yes`.

## [0.2.0] — Initial release

- Manifest-driven installer (`scripts/setup_kit.py`).
- Twelve profile definitions under `agent-center/profiles/`.
- Operation skills: `agent-creator`, `profile-factory`, `wiki-memory`, `kanban-operator`, `gateway-ux`, `skill-hygiene-audit`, `hermes-token-drain-diagnostic`, `telegram-channel-intelligence`.
- Specialist skills: `researcher`, `technical-engineer`, `business-analyst`, `methodologist`, `marketer`, `designer`, `legal-ops`, `economist`.
- Optional / disabled by default: `psychological-support`, `telegram-channel-watcher`.
- Wiki pages: `architecture.md`, `memory-policy.md`, `operating-contract.md`, `team-roster.md`.
- Telegram integration blueprint.
- Cross-platform entry points: `install.ps1`, `install.sh`.

[0.3.1]: https://github.com/your-org/hermes-agent-architecture-kit/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/your-org/hermes-agent-architecture-kit/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/your-org/hermes-agent-architecture-kit/releases/tag/v0.2.0
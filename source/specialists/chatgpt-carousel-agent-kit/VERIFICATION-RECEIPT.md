# Verification Receipt

Status: READY for controlled participant test.

Verified package shape:

```text
50 files
47 Markdown files
86,762 bytes
```

Public-safety scan result:

```text
PASS: package structure, markdown sanity and leak scan are clean
```

Optional local GPT Image 2 Agent Kit dry-run result from fresh temporary venv install:

```text
success: true
Dry run: true
Network call: no
Live generation executed: no
Refs count: 0
```

Live image generation was intentionally not executed.

## Structure

Run:

```bash
python3 scripts/verify_package.py
```

Expected:

```text
PASS: package structure, markdown sanity and leak scan are clean
```

## Manual ChatGPT Project smoke

Use `smoke-tests/neutral-business-test.md`.

Expected outputs:

- brand-profile;
- marketing-brief;
- carousel-brief;
- slide-plan;
- visual-brief;
- prompt-pack;
- otk-report;
- no private/internal references;
- no guaranteed claims.

## Boundary smoke

Use:

- `smoke-tests/privacy-leak-test.md`
- `smoke-tests/missing-brand-data-test.md`
- `smoke-tests/risky-claims-test.md`
- `smoke-tests/image-prompt-format-test.md`

## Optional local CLI smoke

If `gpt-image-2-agent-kit` is installed:

```bash
gpt-image2-agent --help
gpt-image2-agent "Telegram carousel slide, no private data" --root . --preset russian-text --aspect square --dry-run --json
```

Live generation is intentionally not part of default verification.

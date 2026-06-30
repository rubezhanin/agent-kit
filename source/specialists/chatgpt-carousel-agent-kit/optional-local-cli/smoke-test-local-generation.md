# Local CLI Smoke Test

Run after installing public `gpt-image-2-agent-kit`.

## 1. Help

```bash
gpt-image2-agent --help
```

Expected: command prints help.

## 2. Dry-run without token

```bash
gpt-image2-agent "Telegram carousel slide, no private data" \
  --root . \
  --preset russian-text \
  --aspect square \
  --dry-run \
  --json
```

Expected:

- `success: true`
- `dry_run: true`
- no PNG output
- no network/auth required

## 3. Receipt dry-run

```bash
mkdir -p generated

gpt-image2-agent "Carousel visual, clean style, no private data" \
  --root . \
  --dry-run \
  --receipt generated/test.receipt.json

test -f generated/test.receipt.json
```

Expected: receipt file exists and contains no secret.

## 4. Live test

Only if you have configured your own compatible access. Do not run live as a default smoke test.

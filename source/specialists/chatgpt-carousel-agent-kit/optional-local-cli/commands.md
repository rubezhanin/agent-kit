# Commands

## Help

```bash
gpt-image2-agent --help
```

## Dry-run JSON

```bash
gpt-image2-agent "test carousel visual, no private data" \
  --root . \
  --preset russian-text \
  --aspect square \
  --dry-run \
  --json
```

## Dry-run review markdown

```bash
gpt-image2-agent "test carousel visual, no private data" \
  --root . \
  --preset russian-text \
  --preset brand-style \
  --aspect square \
  --dry-run \
  --review-markdown
```

## Add your own style pack

```bash
gpt-image2-agent --root . --add-style my-brand \
  --style-prompt "calm educational style, white background, dark text, green accent" \
  --style-preset brand-style
```

## Use your own style pack in dry-run

```bash
gpt-image2-agent "Telegram carousel cover about productivity" \
  --root . \
  --style my-brand \
  --preset russian-text \
  --aspect square \
  --dry-run \
  --review-markdown
```

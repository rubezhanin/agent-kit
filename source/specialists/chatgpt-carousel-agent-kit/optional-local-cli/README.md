# Optional Local CLI Adapter

Этот раздел нужен только тем, кто хочет использовать публичный `gpt-image-2-agent-kit` локально.

Публичный репозиторий:

```text
https://github.com/AlekseiUL/gpt-image-2-agent-kit
```

## Установка

```bash
mkdir -p ~/ai-tools
cd ~/ai-tools

git clone https://github.com/AlekseiUL/gpt-image-2-agent-kit.git
cd gpt-image-2-agent-kit

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .

gpt-image2-agent --help
```

## Dry-run first

```bash
gpt-image2-agent "Telegram carousel cover, clean educational style, no private data" \
  --root . \
  --preset russian-text \
  --preset brand-style \
  --aspect square \
  --dry-run \
  --review-markdown
```

## Receipt dry-run

```bash
mkdir -p generated

gpt-image2-agent "Carousel slide, clean design, no private data" \
  --root . \
  --preset russian-text \
  --aspect square \
  --dry-run \
  --receipt generated/slide-01.receipt.json
```

## Live generation

Live mode is opt-in. Use only your own compatible access, follow terms and privacy rules, and review every prompt before sending.

Do not put access tokens into Markdown files, chats, screenshots, examples or git commits.

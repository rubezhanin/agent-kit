# Carousel Creator (optional pack)

> Optional integration. Disabled by default. Source pack: [`../../../source/specialists/chatgpt-carousel-agent-kit/`](source/specialists/chatgpt-carousel-agent-kit/).

This integration is a **reference adapter** for the upstream `chatgpt-carousel-agent-kit` pack: a content-marketing specialist that turns a brand brief into a Carousel (Markdown -> visual deck -> publication-ready slides).

The kit ships with the upstream pack under `source/` and adapts it as a **disabled-by-default** profile (`carousel-creator`) so the installer does not auto-activate it.

## What it does

```text
Brand intake    ->  SMM marketer brief  ->  Carousel workflow   ->
Visual design   ->  GPT image prompts   ->  OTK checklist       ->
Troubleshooting + verification receipt
```

## What it does not do

- It does not call the OpenAI API on its own. Image generation goes through the same approval gates as everything else.
- It does not publish anywhere without explicit owner approval.
- It does not touch the Telegram gateway.

## Source-of-truth pointers

The pack expects these sources to exist before a run:

| Source | Role |
| --- | --- |
| `source/specialists/chatgpt-carousel-agent-kit/PACKAGE-CONTRACT.md` | Behavioural contract for the carousel agent. |
| `source/specialists/chatgpt-carousel-agent-kit/AGENT-SETUP.md` | How the agent is wired (project skills vs Custom GPT). |
| `source/specialists/chatgpt-carousel-agent-kit/hermes-skill/SKILL.md` | Hermes skill wrapper. |
| `source/specialists/chatgpt-carousel-agent-kit/templates/` | Intake / brief / slide plan / OTK templates. |
| `source/specialists/chatgpt-carousel-agent-kit/smoke-tests/` | Smoke tests, including privacy / claims / image-prompt tests. |
| `source/specialists/chatgpt-carousel-agent-kit/optional-local-cli/` | A local CLI option if you want to run GPT image generation outside Hermes. |

## Local CLI env

The local CLI uses this env (template under `source/specialists/chatgpt-carousel-agent-kit/optional-local-cli/env.example`):

```bash
OPENAI_API_KEY=sk-...                # required for image generation
OPENAI_MODEL_IMAGE=gpt-image-1       # default model
OPENAI_TIMEOUT_SECONDS=120
CAROUSEL_OUTPUT_DIR=reports/carousel
```

Never commit `.env`. `.gitignore` already excludes it.

## Enable

1. Read `source/specialists/chatgpt-carousel-agent-kit/INSTALL.md`.
2. Copy `optional-local-cli/env.example` to `optional-local-cli/.env` and fill the key.
3. Run the installer with `--include-disabled` and enable `carousel-creator`.
4. Run the smoke tests in `source/specialists/chatgpt-carousel-agent-kit/smoke-tests/` before the first real run.

## Safety

- Treat any output image with embedded text as **untrusted source** for downstream systems.
- Do not feed personal data, faces of non-public people, or copyrighted characters into the visual prompts without legal-ops review.
- See `wiki/security-checklist.md` and `agent-center/integrations/telegram-channel-intelligence/README.md` for the matching stance on outbound content.
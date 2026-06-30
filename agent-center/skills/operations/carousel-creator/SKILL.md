---
name: carousel-creator
description: Optional carousel / SMM creator wrapping the upstream chatgpt-carousel-agent-kit pack. Use when the owner asks to turn a brand brief into a carousel deck (Markdown slides + GPT-image prompts) for an approved channel.
---

# Carousel Creator

Disabled by default. Enable only after the owner has read `agent-center/integrations/carousel-creator/README.md` and the upstream INSTALL.md.

## When to trigger

- "Make a carousel from this brief ...";
- "I need 6 slides for X about Y";
- "Generate GPT image prompts for the deck";
- "Run OTK on the carousel draft".

## Inputs you must collect

1. brand intake (`templates/brand-profile.md`);
2. SMM brief (`templates/marketing-brief.md`);
3. deck goal and channel (LinkedIn, Telegram, Instagram, ...);
4. approval channel (who can publish).

## Process

```text
intake -> role card -> dry-run change packet -> approval -> run
        -> smoke tests -> receipt
```

## Source-of-truth pointers

- `source/specialists/chatgpt-carousel-agent-kit/PACKAGE-CONTRACT.md`
- `source/specialists/chatgpt-carousel-agent-kit/AGENT-SETUP.md`
- `source/specialists/chatgpt-carousel-agent-kit/hermes-skill/SKILL.md`
- `source/specialists/chatgpt-carousel-agent-kit/templates/`
- `source/specialists/chatgpt-carousel-agent-kit/smoke-tests/`

## Stop rules

- No carousel can be **published** without an explicit owner approval that names the channel and the final deck.
- No carousel can be **generated with private faces** or non-public people without legal-ops review.
- No carousel can use **claims without proof** — run legal-ops / OTK before publishing.
- Local CLI must not be invoked with `--auto-publish` flags unless explicitly approved.

## Outputs

- `templates/brand-profile.md` filled;
- `templates/marketing-brief.md` filled;
- `templates/carousel-brief.md`;
- `templates/slide-plan.md`;
- `templates/prompt-pack.md`;
- `templates/visual-brief.md`;
- `templates/otk-report.md`;
- `templates/final-delivery-report.md` → saved under `agent-center/reports/task-receipts/`.
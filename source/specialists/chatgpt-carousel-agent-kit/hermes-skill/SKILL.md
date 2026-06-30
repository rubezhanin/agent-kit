---
name: carousel-agent-kit
description: Portable workflow for brand intake, SMM carousel planning, visual prompt-packs, GPT Image prompts and OTK.
---

# Carousel Agent Kit

Use when the user wants to create a Telegram/Instagram carousel from a business/product/content idea.

## Workflow

1. Load `references/brand-intake.md` and collect brand-profile.
2. Load `references/smm-marketer.md` and produce marketing/carousel brief.
3. Load `references/carousel-workflow.md` and create slide-plan.
4. Load `references/visual-designer.md` and produce visual-brief.
5. Load `references/gpt-image-prompts.md` and produce prompt-pack.
6. Load `references/otk-checklist.md` and run final review.

## Rules

- Do not start with image generation.
- Do not ask for secrets, tokens, cookies or session files.
- Do not use private/internal style packs or references.
- If data is missing, ask or mark assumptions.
- For risky medical, financial, legal or reputation claims, reframe or block.
- Live image generation is optional and uses the user's own tools/access.

## Output

Return:

```text
brand-profile
marketing-brief
carousel-brief
slide-plan
visual-brief
prompt-pack
otk-report
final-delivery-report
```

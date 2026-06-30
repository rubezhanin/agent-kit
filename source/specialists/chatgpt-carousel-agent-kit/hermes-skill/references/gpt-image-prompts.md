# 05 — GPT Image Prompts

Цель: писать prompts так, чтобы изображение помогало слайду, а не просто выглядело красиво.

## Prompt structure

```text
Create a finished carousel slide.
Platform/format:
Slide text:
Visual goal:
Scene/metaphor:
Composition:
Style:
Color palette:
Typography:
Text placement:
People/reference rules:
Must include:
Must avoid:
Technical constraints:
```

## Telegram square prompt template

```text
Create a square Telegram carousel slide, 1280x1280.

Slide text: "<SHORT RUSSIAN TEXT>"
Visual goal: <what the viewer should understand from this slide>
Scene/metaphor: <one clear scene or object>
Composition: big readable headline, one dominant visual object, clean background, safe margins 12%.
Style: <user brand style from brand-profile>
Color palette: <colors from brand-profile>
Typography: large clean Cyrillic typography, high contrast, no tiny text.
Text placement: keep text in a clean reserved zone, not over faces/hands/important objects.
Must include: <required objects>
Must avoid: generic AI glow, random robots, fake UI, fake logos, watermarks, tiny paragraphs, clutter.
```

## Instagram 4:5 prompt template

```text
Create a vertical Instagram carousel slide, 1080x1350, 4:5 portrait.

Slide text: "<SHORT RUSSIAN TEXT>"
Visual goal: <meaning job>
Scene/metaphor: <one clear scene>
Composition: strong top/center headline, clear focal point, 10-12% safe margins, cover-safe central crop.
Style: <user brand style>
Color palette: <colors>
Typography: large readable Cyrillic, clean hierarchy.
Text placement: reserved text zone, no text over faces/hands/key objects.
Must include: <objects/people>
Must avoid: <negative constraints>
```

## Prompt-pack format

```text
# Prompt Pack

## Global style

Brand style:
Colors:
Typography:
Format:
People/reference policy:
Negative global constraints:

## Slide 1

Text:
Meaning job:
Prompt:
Negative constraints:
OTK risk:

## Slide 2
...
```

## Negative constraints library

Use only what fits:

```text
no fake logos, no unreadable tiny text, no random watermarks, no malformed hands, no broken faces, no extra fingers, no distorted eyes, no fake UI data, no misleading charts, no medical/financial/legal guarantees, no cluttered background, no generic robot mascot unless requested, no blue sci-fi glow unless brand requires it
```

## Local CLI dry-run with public GPT Image 2 Agent Kit

If installed:

```bash
gpt-image2-agent "<prompt text>" \
  --root . \
  --preset russian-text \
  --preset brand-style \
  --aspect square \
  --dry-run \
  --review-markdown
```

With receipt:

```bash
gpt-image2-agent "<prompt text>" \
  --root . \
  --preset russian-text \
  --aspect square \
  --dry-run \
  --receipt generated/slide-01.receipt.json
```

Do live generation only after human review.

## Important

Do not put secrets, access tokens, private client notes or sensitive personal details into prompts unless the user explicitly accepts the privacy risk of sending them to the selected image backend.

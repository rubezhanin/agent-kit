#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

required = [
    'README.md',
    'AGENT-SETUP.md',
    'INSTALL.md',
    'PACKAGE-CONTRACT.md',
    'CHATGPT-PROJECT-INSTRUCTIONS.md',
    'CUSTOM-GPT-INSTRUCTIONS.md',
    '01-BRAND-INTAKE.md',
    '02-SMM-MARKETER.md',
    '03-CAROUSEL-WORKFLOW.md',
    '04-VISUAL-DESIGNER.md',
    '05-GPT-IMAGE-PROMPTS.md',
    '06-OTK-CHECKLIST.md',
    '07-TROUBLESHOOTING.md',
    'templates/brand-profile.md',
    'templates/marketing-brief.md',
    'templates/carousel-brief.md',
    'templates/slide-plan.md',
    'templates/visual-brief.md',
    'templates/prompt-pack.md',
    'templates/otk-report.md',
    'templates/final-delivery-report.md',
    'examples/neutral-it-english-tutor/input.md',
    'examples/neutral-it-english-tutor/brand-profile.example.md',
    'examples/neutral-it-english-tutor/marketing-brief.example.md',
    'examples/neutral-it-english-tutor/carousel-brief.example.md',
    'examples/neutral-it-english-tutor/slide-plan.example.md',
    'examples/neutral-it-english-tutor/visual-brief.example.md',
    'examples/neutral-it-english-tutor/prompt-pack.example.md',
    'examples/neutral-it-english-tutor/otk-report.example.md',
    'examples/neutral-it-english-tutor/final-delivery-report.example.md',
    'optional-local-cli/README.md',
    'hermes-skill/SKILL.md',
]

for rel in required:
    p = ROOT / rel
    if not p.exists():
        print(f'MISSING: {rel}')
        sys.exit(1)

bad = []
text_suffixes = {'.md', '.txt', '.example', '.py'}
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix in text_suffixes:
        text = p.read_text(encoding='utf-8')
        if not text.strip():
            bad.append((p, 'empty'))
        if not text.endswith('\n'):
            bad.append((p, 'missing trailing newline'))
        if '\x00' in text:
            bad.append((p, 'NUL byte'))

# Hard blockers. Values are assembled to avoid this checker matching its own source.
patterns = [
    '/' + 'Users' + '/' + 'aleksejulanov',
    'MIKE' + '_CENTER',
    r'\.' + 'hermes',
    'mike' + '-jesse',
    'sprut' + '-graphite-orange',
    'face' + 'pack',
    'OPENAI' + '_API_KEY=sk-',
    r'Bearer\s+[A-Za-z0-9_\-\.]{12,}',
]
for p in ROOT.rglob('*'):
    if p.name == 'verify_package.py':
        continue
    if p.is_file() and p.suffix in text_suffixes:
        text = p.read_text(encoding='utf-8')
        for pat in patterns:
            if re.search(pat, text, re.I):
                bad.append((p, f'private/leak pattern: {pat}'))

if bad:
    for p, reason in bad:
        print(f'FAIL: {p.relative_to(ROOT)} — {reason}')
    sys.exit(1)

print('PASS: package structure, markdown sanity and leak scan are clean')

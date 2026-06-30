# Файл для агента

## Назначение

Ты — Hermes-агент. Твоя задача: самостоятельно установить **Skill Hygiene Guard** для своего активного Hermes-профиля.

Guard должен регулярно проверять, не разрастаются ли skills до состояния, где агент начинает путаться в них. Guard **не должен** автоматически объединять, удалять, переименовывать или переписывать skills.

Режим по умолчанию: **weekly read-only audit + local report + manual approval для любых правок**.

---

## Жёсткие правила

1. Не копируй чужие абсолютные пути.
2. Определи свой активный `HERMES_HOME` / profile home.
3. Пиши только внутри своего profile/project reports directory.
4. Skills можно только читать.
5. Нельзя auto-merge, auto-delete, auto-rewrite.
6. Green run не должен спамить владельца.
7. Любые изменения skills — только в отдельной интерактивной сессии после явного approval владельца.

---

## Что нужно установить

Нужно создать:

```text
<profile-home>/scripts/hermes_skills_audit.py
<profile-home>/reports/skills-audit/
```

И поставить weekly cron:

```text
name: weekly-skills-hygiene-audit
schedule: 30 10 * * 0
repeat: forever
deliver: local
script: hermes_skills_audit.py
```

`30 10 * * 0` = каждое воскресенье в 10:30 по локальному времени профиля.

---

## Как определить profile home

Используй первый доступный способ:

1. `HERMES_HOME` из environment.
2. Активный profile path из Hermes config/status, если доступно.
3. Если ты работаешь в default profile — `~/.hermes`.
4. Если ты работаешь в named profile — `~/.hermes/profiles/<profile-name>`.

Проверь, что внутри есть хотя бы один из файлов/каталогов:

```text
config.yaml
.env
skills/
sessions/
```

Если profile home не найден — остановись и попроси владельца указать путь. Не угадывай.

---

## Audit script

Создай файл:

```text
<profile-home>/scripts/hermes_skills_audit.py
```

Содержимое:

```python
#!/usr/bin/env python3
"""Read-only Hermes skills hygiene audit.

This script does not modify skills. It writes JSON and Markdown reports only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
from collections import defaultdict
from pathlib import Path

SIZE_WARN_BYTES = 30_000
DESCRIPTION_WARN_CHARS = 260
SIMILARITY_WARN = 0.62


def profile_home() -> Path:
    env = os.environ.get("HERMES_HOME")
    if env:
        return Path(env).expanduser().resolve()
    # Script is expected at <profile-home>/scripts/hermes_skills_audit.py
    return Path(__file__).resolve().parents[1]


def now_local() -> dt.datetime:
    return dt.datetime.now().astimezone()


def parse_frontmatter(text: str) -> dict[str, str]:
    data: dict[str, str] = {}
    if not text.startswith("---"):
        return data
    end = text.find("\n---", 3)
    if end == -1:
        return data
    for line in text[3:end].strip().splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key in {"name", "description"}:
            data[key] = value
    return data


def words(s: str) -> set[str]:
    stop = {"the", "and", "for", "with", "use", "using", "this", "when", "что", "для", "как"}
    return {w for w in re.findall(r"[a-zA-Zа-яА-Я0-9_-]{3,}", s.lower()) if w not in stop}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def find_skills_root(home: Path) -> Path:
    candidates = [
        home / "skills",
        Path.home() / ".hermes" / "skills",
    ]
    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            return candidate
    raise SystemExit(f"skills directory not found under {home}")


def collect(skills_root: Path) -> list[dict]:
    skills = []
    for p in sorted(skills_root.rglob("SKILL.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        name = fm.get("name") or p.parent.name
        desc = fm.get("description", "")
        skills.append({
            "name": name,
            "description": desc,
            "path": str(p),
            "relative_path": str(p.relative_to(skills_root)),
            "bytes": p.stat().st_size,
            "description_chars": len(desc),
            "has_frontmatter_name": "name" in fm,
            "has_frontmatter_description": "description" in fm,
            "tokens": sorted(words(name + " " + desc)),
        })
    return skills


def audit(home: Path) -> dict:
    skills_root = find_skills_root(home)
    report_dir = home / "reports" / "skills-audit"
    skills = collect(skills_root)

    by_name = defaultdict(list)
    for s in skills:
        by_name[s["name"]].append(s["relative_path"])

    duplicate_names = {name: paths for name, paths in sorted(by_name.items()) if len(paths) > 1}
    oversized = [s for s in skills if s["bytes"] > SIZE_WARN_BYTES]
    long_descriptions = [s for s in skills if s["description_chars"] > DESCRIPTION_WARN_CHARS]
    missing_frontmatter = [s for s in skills if not s["has_frontmatter_name"] or not s["has_frontmatter_description"]]

    similar = []
    for i, a in enumerate(skills):
        aw = set(a["tokens"])
        for b in skills[i + 1:]:
            score = jaccard(aw, set(b["tokens"]))
            if score >= SIMILARITY_WARN:
                similar.append({
                    "score": round(score, 3),
                    "a": a["name"],
                    "a_path": a["relative_path"],
                    "b": b["name"],
                    "b_path": b["relative_path"],
                })
    similar.sort(key=lambda x: x["score"], reverse=True)

    available_catalog_estimated_chars = sum(len(s["name"]) + len(s["description"]) + 8 for s in skills)
    total_skill_md_bytes = sum(s["bytes"] for s in skills)

    return {
        "checked_at": now_local().isoformat(),
        "ok": not duplicate_names and not missing_frontmatter,
        "scope": {
            "profile_home": str(home),
            "skills_root": str(skills_root),
            "report_dir": str(report_dir),
            "read_only": True,
            "autofix": False,
        },
        "summary": {
            "skill_count": len(skills),
            "total_skill_md_bytes": total_skill_md_bytes,
            "available_catalog_estimated_chars": available_catalog_estimated_chars,
            "oversized_count": len(oversized),
            "long_description_count": len(long_descriptions),
            "duplicate_name_count": len(duplicate_names),
            "missing_frontmatter_count": len(missing_frontmatter),
            "similar_pair_count": len(similar),
        },
        "findings": {
            "duplicate_names": duplicate_names,
            "missing_frontmatter": [
                {k: s[k] for k in ("name", "relative_path", "has_frontmatter_name", "has_frontmatter_description")}
                for s in missing_frontmatter
            ],
            "oversized": [
                {k: s[k] for k in ("name", "relative_path", "bytes", "description_chars")}
                for s in sorted(oversized, key=lambda x: x["bytes"], reverse=True)
            ],
            "long_descriptions": [
                {k: s[k] for k in ("name", "relative_path", "description_chars", "description")}
                for s in sorted(long_descriptions, key=lambda x: x["description_chars"], reverse=True)
            ],
            "similar_pairs_top_30": similar[:30],
        },
        "recommendation": "Do not auto-merge or auto-rewrite skills. Use this report for manual approved hygiene changes.",
    }


def write_reports(home: Path, data: dict) -> tuple[Path, Path]:
    report_dir = home / "reports" / "skills-audit"
    report_dir.mkdir(parents=True, exist_ok=True)
    stamp = now_local().strftime("%Y%m%d-%H%M%S")
    json_path = report_dir / f"skills-audit-{stamp}.json"
    md_path = report_dir / f"skills-audit-{stamp}.md"

    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    s = data["summary"]
    lines = [
        "# Hermes Skills Hygiene Audit",
        "",
        f"Checked: `{data['checked_at']}`",
        "Mode: `read-only`; autofix: `disabled`",
        "",
        "## Summary",
        "",
        f"- Skills: `{s['skill_count']}`",
        f"- Total SKILL.md bytes: `{s['total_skill_md_bytes']}`",
        f"- Estimated catalog chars: `{s['available_catalog_estimated_chars']}`",
        f"- Oversized skills > {SIZE_WARN_BYTES} bytes: `{s['oversized_count']}`",
        f"- Long descriptions > {DESCRIPTION_WARN_CHARS} chars: `{s['long_description_count']}`",
        f"- Duplicate names: `{s['duplicate_name_count']}`",
        f"- Missing frontmatter: `{s['missing_frontmatter_count']}`",
        f"- Similar pairs: `{s['similar_pair_count']}`",
        "",
        "## Findings",
        "",
    ]

    for key, title in [
        ("oversized", "Oversized skills"),
        ("long_descriptions", "Long descriptions"),
        ("similar_pairs_top_30", "Similar candidates"),
    ]:
        items = data["findings"].get(key) or []
        if not items:
            continue
        lines += [f"### {title}", ""]
        for item in items[:15]:
            if key == "similar_pairs_top_30":
                lines.append(f"- `{item['a']}` ↔ `{item['b']}` — score `{item['score']}`")
            else:
                lines.append(f"- `{item['name']}` — `{item.get('bytes', item.get('description_chars'))}` — `{item['relative_path']}`")
        lines.append("")

    if data["findings"].get("duplicate_names"):
        lines += ["### Duplicate names", ""]
        for name, paths in data["findings"]["duplicate_names"].items():
            lines.append(f"- `{name}`: {', '.join(paths)}")
        lines.append("")

    if data["findings"].get("missing_frontmatter"):
        lines += ["### Missing frontmatter", ""]
        for item in data["findings"]["missing_frontmatter"][:15]:
            lines.append(f"- `{item['relative_path']}`")
        lines.append("")

    lines += [
        "## Position",
        "",
        "No skills were modified. Any merge, delete, rename, or rewrite requires manual approval.",
        "",
        "JSON report:",
        f"`{json_path}`",
        "",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Print compact JSON summary to stdout")
    args = parser.parse_args()

    home = profile_home()
    data = audit(home)
    json_path, md_path = write_reports(home, data)

    out = {
        "ok": data["ok"],
        "json_report": str(json_path),
        "md_report": str(md_path),
        "summary": data["summary"],
        "recommendation": data["recommendation"],
    }
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"skills_audit ok={out['ok']} md={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Сделай файл исполняемым:

```bash
chmod 700 <profile-home>/scripts/hermes_skills_audit.py
```

---

## Первый запуск и проверка

Запусти:

```bash
HERMES_HOME=<profile-home> <profile-home>/scripts/hermes_skills_audit.py --json
```

Проверь:

1. exit code `0`;
2. создан JSON report;
3. создан Markdown report;
4. в report есть строка `read-only`; 
5. в report есть `autofix disabled` или `autofix: disabled`;
6. skills-файлы не изменились.

Если script не нашёл `skills/`, не создавай cron. Сначала найди правильный profile home.

---

## Установка cron

Если у тебя есть Hermes `cronjob` tool, создай job так:

```json
{
  "action": "create",
  "name": "weekly-skills-hygiene-audit",
  "schedule": "30 10 * * 0",
  "repeat": null,
  "deliver": "local",
  "script": "hermes_skills_audit.py",
  "prompt": "Weekly read-only Hermes skills hygiene audit. A pre-run script has already written JSON/Markdown reports under the active profile reports/skills-audit directory. Do not modify skills. Do not send external messages. Save only a compact local summary. Any fixes require manual approval in an interactive session."
}
```

Если работаешь через CLI, используй Hermes cron интерфейс:

```bash
hermes cron list
hermes cron create '30 10 * * 0'
```

При создании укажи:

```text
name: weekly-skills-hygiene-audit
deliver: local
script: hermes_skills_audit.py
repeat: forever
```

Если CLI не позволяет задать script неинтерактивно, используй интерактивный `hermes cron edit` / `/cron` и выставь те же поля.

---

## Smoke test cron

После создания cron:

1. Выполни `cron list`.
2. Убедись, что job enabled.
3. Запусти job вручную, если доступно: `cron run <job_id>`.
4. Подожди scheduler tick.
5. Снова проверь `cron list`.
6. Убедись, что `last_status` = `ok` или что local output создан.
7. Убедись, что владелец не получил green-status spam.

---

## Что делать с findings

Audit findings — это не авария. Это список кандидатов.

Правила:

### Long descriptions

Сокращай description до routing-смысла. Детали оставляй в теле skill или linked files.

### Oversized skills

Не режь вслепую. Обычно правильный ремонт:

```text
SKILL.md = короткий workflow + routing
references/*.md = длинные таблицы, API notes, примеры
scripts/* = вспомогательные скрипты
```

### Duplicate names

Не удаляй автоматически. Сначала выясни, это настоящий дубль или разные процедуры с конфликтующим именем.

### Similar pairs

Не merge автоматически. Сделай proposal:

```text
candidate A
candidate B
why similar
recommended action
risk
rollback
```

### Missing frontmatter

Можно чинить быстрее, но всё равно через отдельную интерактивную сессию.

---

## Manual hygiene pass

Если владелец просит чистку, действуй так:

1. Прочитай последний audit report.
2. Составь список кандидатов.
3. Раздели на:
   - safe description compression;
   - reference extraction;
   - possible duplicates;
   - stale skills;
   - broken frontmatter.
4. Покажи владельцу план.
5. После approval внеси изменения.
6. Перезапусти audit.
7. Дай diff/summary.

Команда владельца может звучать так:

```text
Do a skills hygiene pass. Read the latest audit report. Propose changes first. Do not modify skills without my approval.
```

---

## Acceptance criteria

Установка завершена только если:

- script создан в active profile scripts directory;
- script запускается вручную;
- reports создаются;
- cron создан и enabled;
- cron local-only;
- green run не шлёт external messages;
- ни один skill не был изменён при установке;
- итоговый ответ владельцу содержит:
  - path к script;
  - path к latest report;
  - cron name/job_id;
  - next run time;
  - предупреждение: `no auto-merge/delete/rewrite`.

---

## Финальный ответ владельцу

После установки ответь коротко:

```text
Поставил Skill Hygiene Guard.

Script: <path>
Reports: <path>
Cron: weekly-skills-hygiene-audit (<job_id>)
Schedule: every Sunday 10:30 local time
Mode: read-only, local-only, no autofix
Latest audit: <path>

Skills не изменялись. Любые merge/delete/rewrite — только после отдельного approval.
```

---

## Stop conditions

Остановись и спроси владельца, если:

- не найден active profile home;
- не найден skills directory;
- нет cron tool и непонятно, как создать scheduled job;
- profile находится в read-only окружении;
- владелец просит auto-merge/delete без review.

Не угадывай. Не ломай рабочие skills.

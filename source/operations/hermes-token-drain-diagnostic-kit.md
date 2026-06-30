---
name: hermes-token-drain-diagnostic
description: Read-only diagnostic kit for finding why Hermes Agent spends too many tokens, with evidence collection, risk classification, approval-gated fixes, smoke tests and receipt.
version: 1.1.0
language: ru
artifact_type: portable-diagnostic-md
install_modes:
  - Hermes Skill
  - helper-agent instruction
  - AGENTS.md / AGENT.md operating file
  - plain checklist
metadata:
  hermes:
    category: diagnostics
    tags:
      - hermes
      - tokens
      - cost
      - diagnostics
      - profiles
      - sessions
      - tools
      - skills
      - memory
      - gateway
      - safety
---

# Hermes Token-Drain Diagnostic Kit

MD-инструмент для диагностики ситуации, когда Hermes Agent начинает слишком быстро тратить токены.

Главная задача файла - не “починить всё сразу”, а безопасно сузить причины расхода:

```text
где есть признаки повышенного расхода
какие причины наиболее вероятны
какие evidence это подтверждают
каких данных не хватает для точной атрибуции
что можно сделать
что нельзя трогать без approval
```

Если usage/token/cost telemetry недоступна, агент не должен притворяться, что знает точную причину. Он пишет `likely cause`, confidence и evidence gaps.

Файл можно дать своему агенту как инструкцию. Агент должен провести read-only диагностику, собрать evidence, назвать самые вероятные причины и остановиться перед любыми изменениями.

---

## 0. Коротко для новичка

Если кажется, что Hermes “жрёт токены”, не начинай с удаления памяти, отключения tools или смены модели.

Сначала надо понять, где именно расход:

1. в длинной активной сессии;
2. в постоянной compression;
3. в слишком большом наборе tools;
4. в лишних skills;
5. в раздутой memory;
6. в cron/background задачах;
7. в browser/MCP/screenshot шуме;
8. в retry/fallback петлях;
9. в дорогой модели или высоком reasoning;
10. в пользовательском workflow: огромные логи, файлы и скриншоты в чат.

Нормальная диагностика сначала смотрит факты, а потом предлагает ремонт.

---

## 1. Как использовать файл

Есть четыре режима.

**Важно:** этот раздел - для человека, который устанавливает или передаёт файл. Если MD уже передан агенту для диагностики, агент не должен выполнять команды установки, копирования, создания директорий или размещения `AGENTS.md`. Это write/setup действия. Для них нужен отдельный approval.

### Режим A: как Hermes Skill

Сохрани файл как `SKILL.md` в профильный skill-каталог.

Пример с placeholder, не копируй вслепую:

```bash
# HUMAN SETUP ONLY — do not run during diagnosis.
# Requires explicit approval because it writes into a Hermes profile.
mkdir -p "${HERMES_HOME:-$HOME/.hermes}/profiles/<PROFILE_NAME>/skills/diagnostics/hermes-token-drain-diagnostic"
cp hermes-token-drain-diagnostic-kit.md "${HERMES_HOME:-$HOME/.hermes}/profiles/<PROFILE_NAME>/skills/diagnostics/hermes-token-drain-diagnostic/SKILL.md"
hermes --profile <PROFILE_NAME> skills list | grep -iE 'hermes-token-drain-diagnostic|token-drain|diagnostic'
```

Проверка:

```bash
hermes --profile <PROFILE_NAME> chat   --skills hermes-token-drain-diagnostic   -q "Do token-drain diagnosis discovery only. Do not change files. Return target/scope questions and YAML report skeleton."
```

Если skill не найден:

1. проверь, что файл лежит как `SKILL.md`;
2. проверь, что путь находится внутри profile skills directory;
3. запусти `hermes --profile <PROFILE_NAME> skills list`;
4. используй точное имя из списка skills;
5. если skill всё равно не виден - используй режим B или D.

### Режим B: как инструкция для helper-agent

Передай весь MD отдельному агенту и добавь:

```text
Используй MD ниже как единственный регламент диагностики token drain.
Профиль/проект для проверки: <PROFILE_NAME_OR_PROJECT_ROOT>.
Работай read-only.
Не меняй конфиг, память, skills, tools, cron, gateway и процессы без отдельного approval.
```

### Режим C: как `AGENTS.md` / `AGENT.md`

Положи файл в корень проекта или рядом с профилем как временный operating contract для диагностики.

Это write-операция. Не выполнять агентом во время диагностики без отдельного approval.

Не оставляй его как постоянный `AGENTS.md`, если он мешает обычной работе проекта.

### Режим D: как plain checklist

Если Hermes CLI недоступен, агент или человек проходит чеклист вручную:

- выбирает scope;
- собирает metadata;
- не читает секреты;
- классифицирует причины;
- пишет report;
- предлагает remediation plan;
- ждёт approval перед изменениями.

---

## 2. Safety contract

Правила выше удобства.

### Можно по умолчанию

- читать config metadata;
- смотреть размеры файлов;
- считать строки/сообщения/события;
- смотреть список профилей, skills, tools, cron jobs;
- читать логи ограниченными фрагментами;
- считать повторы ошибок;
- смотреть процессы;
- писать диагностический report в новое место, если пользователь разрешил запись report-файла.

### Нельзя без отдельного approval

- менять config;
- удалять или архивировать sessions;
- чистить memory;
- отключать skills/tools/MCP;
- менять model/provider/reasoning/context length;
- останавливать gateway;
- рестартовать сервисы;
- убивать процессы;
- pausing/removing cron jobs;
- удалять логи/cache/browser state;
- читать `.env`, `auth.json`, cookies, private keys, OAuth tokens;
- публиковать или отправлять отчёты наружу;
- отправлять логи, отчёты, path lists, process lists или config summaries во внешние сервисы;
- открывать network upload/share links для diagnostic artifacts;
- применять “оптимизации” пачкой.

### Секреты

Не печатай:

```text
API keys
OAuth tokens
cookies
.env values
auth.json contents
browser profiles
private chat text
raw client data
full logs with personal data
```

Если что-то похоже на секрет, пиши только:

```text
<REDACTED:API_KEY>
<REDACTED:TOKEN>
<REDACTED:COOKIE>
<REDACTED:PRIVATE_TEXT>
```

---

## 3. Beginner path: 15-minute safe diagnosis

Если человек не технарь, агент должен идти так:

```text
BEGINNER TOKEN-DRAIN PATH

Step 1. Уточнить цель:
- какой профиль / проект / чат / период проверяем?

Step 2. Ничего не менять:
- только read-only discovery.

Step 3. Собрать быстрые факты:
- модель;
- активные sessions;
- compression events;
- tools/skills;
- memory sizes;
- cron/background jobs;
- gateway/retry logs.

Step 4. Выбрать 1-3 главные причины:
- не список из 20 гипотез, а приоритет.

Step 5. Написать report:
- evidence;
- confidence;
- risk class;
- false positives;
- remediation options.

Step 6. Остановиться:
- спросить approval на конкретный следующий шаг.
```

Если scope непонятен - глобально смотреть только metadata и спросить цель.

Минимальные вопросы, если данных нет:

1. Какой profile проверяем?
2. За какой период заметен расход?
3. Где симптом: CLI, gateway, Telegram/Discord/Slack/API/cron?
4. Есть ли provider usage/token screenshot или `hermes insights`?
5. Можно ли записать report-файл, или вернуть только в чат?
6. Есть ли запрет даже на bounded log scan? Если да - использовать только metadata/CLI summary.

---

## 4. Scope selector

Перед диагностикой выбери один scope.

```yaml
scope:
  hermes_home: "<HERMES_HOME_OR_UNKNOWN>"
  profile: "<PROFILE_NAME_OR_UNKNOWN>"
  project_root: "<PROJECT_ROOT_OR_UNKNOWN>"
  platform: "cli|telegram|discord|slack|api|cron|unknown"
  time_window:
    since: "<SINCE_OR_UNKNOWN>"
    until: "<UNTIL_OR_NOW>"
  symptom:
    - high_bill
    - slow_replies
    - repeated_compression
    - long_context
    - many_tool_calls
    - duplicate_runs
    - runaway_background_process
    - expensive_model_use
    - unknown
```

Если пользователь говорит “Hermes жрёт токены”, но не говорит профиль, агент должен спросить или сделать только общий read-only inventory.

---

## 5. Quick triage: что чаще всего выедает токены

| Rank | Причина | Симптом | Почему жрёт | Первое evidence |
|---:|---|---|---|---|
| 1 | Раздутая активная session | каждый ответ всё дороже и медленнее | история постоянно попадает в контекст | message count, session size, old active session |
| 2 | Compression loop | частые `compression`, `summary`, `context` события | compression сама вызывает модель | logs, aux calls, repeated summarization |
| 3 | Слишком много tools | даже простой запрос дорогой | tool schemas попадают в prompt | enabled toolsets, MCP/tools count |
| 4 | Лишние skills | нерелевантные инструкции в каждом ответе | skill text добавляется в context | loaded skills, skill sizes |
| 5 | Большая memory | новая session уже тяжёлая | persistent memory инжектится или retrieval слишком широкий | memory file size, entries count |
| 6 | Aux model слишком тяжёлый | session_search/compression дорогие | вспомогательные задачи идут через дорогую модель | auxiliary config/logs |
| 7 | Cron loops | токены уходят без сообщений пользователя | scheduled jobs запускают агента | cron list, last_run bursts |
| 8 | Gateway restart loop | повторные старты и восстановления | gateway перезапускается и поднимает state | gateway logs, supervisor status |
| 9 | Background tasks | расход продолжается после задачи | watchers, browsers, workers не остановились | process list, task logs |
| 10 | Browser/MCP noise | огромные snapshots/DOM/tool results | наблюдения браузера и MCP verbose | browser logs, tool output sizes |
| 11 | Recursive delegation | агент плодит агентов | каждый child имеет свой prompt/tools/history | handoff/task logs |
| 12 | Verbose tool output | в историю попали тысячи строк | output становится context | tool transcripts, huge stdout |
| 13 | Большие файлы вставлены в чат | session навсегда тяжёлая | raw text остаётся в истории | large user messages |
| 14 | Tool loop / max_turns loop | агент повторяет один tool | нет stop condition | repeated tool calls |
| 15 | High reasoning | короткий ответ, дорогой вызов | модель думает дорого | reasoning config, provider usage |
| 16 | Wrong model routing | простая задача идёт в дорогую модель | routing не различает задачи | model/provider config |
| 17 | No reset policy | старые темы живут в одном контексте | session не закрывается | reset policy absent |
| 18 | Retry/fallback storm | один запрос биллится несколько раз | ошибки запускают retries/fallbacks | error logs, retry counters |
| 19 | Image/screenshots | vision токены резко растут | screenshots/image inputs дорогие | image/screenshot calls |
| 20 | Docs pasted into prompt | reference text постоянно повторяется | большие docs стали system/user context | custom prompt/AGENTS/docs size |

---

## 6. Evidence collection map

Заполняй только то, что реально проверено.

| Area | Evidence | Зачем |
|---|---|---|
| Usage baseline | date range, provider, model, token counts/cost if available | отличить реальный drain от ощущения |
| Active sessions | count, oldest active, biggest session, message count | найти context bloat |
| Prompt assembly | system prompt size, toolsets, skills, memory | найти static prompt bloat |
| Compression | threshold, model, events, errors | найти compression loop |
| Provider routing | main model, aux model, fallback, reasoning | найти дорогой routing |
| Tools/MCP | tool count, MCP servers, browser tools | найти schema/tool bloat |
| Skills | loaded skills, large skills, overlap | найти skill bloat |
| Memory/search | memory size, session_search, retrieval size | найти persistent/retrieval bloat |
| Cron | jobs, intervals, last_run, duplicates | найти hidden spend |
| Gateway | process count, restarts, reconnects | найти duplicate/restart spend |
| Background | workers, browsers, watchers, MCP | найти продолжающийся расход |
| Browser/vision | screenshots, DOM dumps, image attachments | найти vision/noise cost |
| Retry/fallback | errors, retry bursts, context errors | найти multiplied billing |
| User workflow | pasted logs/files/images, no reset habit | найти workflow-driven spend |

---

## 7. Read-only discovery commands

Команды ниже - примеры. Агент обязан адаптировать их к ОС и реальному Hermes setup.

### 7.0 Prerequisites, portability and bounds

Supported paths:

- macOS/Linux shell: можно использовать bash snippets ниже;
- Windows: использовать WSL/Git Bash или только Hermes CLI + Python helpers;
- no shell: пройти plain checklist и provider/Hermes UI вручную.

Optional tools: `python3`, `sqlite3`, `grep/find/du` для fallback scans.

Сначала используй штатные Hermes summary/JSON команды. Raw filesystem/log scans - только если штатная команда недоступна или недостаточна.

Перед запуском любой Hermes CLI команды проверь, что она documented/read-only. Не запускай команды, которые могут repair, initialize, migrate, write cache, start services или менять state. Если не уверен - запускай только `--help` или помечай `command_safety_unknown`.

Runtime bounds для каждого scan:

- prefer selected profile path over whole `HERMES_HOME`;
- max files inspected: `10_000`;
- max bytes per file: 2 MB tail;
- max total bytes read: 50 MB;
- target wall time: 30-60 seconds;
- if limit hit, stop and report `scan_truncated: true`.

Paths are potentially private. В public/shared reports печатай `path_class`, basename или redacted path. Не вставляй полные списки путей, если пользователь явно не попросил.

Log helpers may scan bounded log text in memory for keyword counts. They must not print raw lines. If policy forbids reading private text at all, skip log scans and use metadata-only checks.

### 7.1 Identify Hermes and profile

```bash
hermes --version
hermes doctor --help
# Run `hermes doctor` only if this version documents it as read-only/no-fix.
hermes profile list
hermes config path
```

First-class Hermes diagnostics first:

```bash
hermes --profile <PROFILE_NAME> prompt-size --json 2>/dev/null || hermes prompt-size --json 2>/dev/null || true
hermes --profile <PROFILE_NAME> sessions stats 2>/dev/null || true
hermes --profile <PROFILE_NAME> sessions list 2>/dev/null | head -50 || true
hermes --profile <PROFILE_NAME> insights --days 7 2>/dev/null || true
hermes --profile <PROFILE_NAME> tools --summary 2>/dev/null || true
# Do not run raw `hermes logs` by default: it may print private log text. Use count-only log helpers below.
```

If a command is unavailable, record `command_unavailable` and continue.

Если профиль известен:

```bash
hermes --profile <PROFILE_NAME> config path
hermes --profile <PROFILE_NAME> config check --help
# Run `config check` only if this version documents it as read-only.
hermes --profile <PROFILE_NAME> memory status
hermes --profile <PROFILE_NAME> skills list
hermes --profile <PROFILE_NAME> tools list
```

Если команда отсутствует в версии Hermes, не выдумывай. Напиши:

```text
command_unavailable: <command>
next_safe_check: <alternative>
```

### 7.2 Redacted config probe

Не печатай secrets.

```bash
python3 - <<'PY'
from pathlib import Path
import json, re
try:
    import yaml
except Exception:
    yaml = None

path = Path('<CONFIG_PATH>').expanduser()
if not path.exists():
    print(json.dumps({'exists': False, 'path': '<CONFIG_PATH>'}, indent=2))
    raise SystemExit(0)

text = path.read_text(errors='replace')
if yaml:
    data = yaml.safe_load(text) or {}
else:
    data = {'raw_lines': len(text.splitlines())}

secret_words = ['key','token','secret','password','cookie','auth','credential','bearer','client_secret','refresh_token','access_token']
secret_value_re = re.compile(
    r'(sk-[A-Za-z0-9_-]+|xox[baprs]-[A-Za-z0-9-]+|ghp_[A-Za-z0-9_]+|'
    r'AIza[0-9A-Za-z_-]+|AKIA[0-9A-Z]{16}|Bearer\s+[A-Za-z0-9._-]+|'
    r'BEGIN .*PRIVATE KEY|https?://[^/\s:@]+:[^/\s:@]+@)',
    re.I,
)
def red(x):
    if isinstance(x, dict):
        out = {}
        for k,v in x.items():
            if any(w in str(k).lower() for w in secret_words):
                out[k] = '<REDACTED>'
            else:
                out[k] = red(v)
        return out
    if isinstance(x, list):
        return [red(v) for v in x]
    if isinstance(x, str) and secret_value_re.search(x):
        return '<REDACTED>'
    return x

keep = ['model','agent','compression','auxiliary','display','default_reset_policy','smart_model_routing','tools','toolsets','mcp','memory']
if isinstance(data, dict):
    data = {k:data.get(k) for k in keep if k in data}
print(json.dumps(red(data), ensure_ascii=False, indent=2))
PY
```

### 7.3 Profile/session/log metadata

```bash
# Metadata summary only. Do not dump private message text or full path lists.
python3 - <<'PY'
from pathlib import Path
import json, os, re
root = Path(os.environ.get('HERMES_HOME', str(Path.home()/'.hermes'))).expanduser()
max_files = 10_000
out = {
    'root_exists': root.exists(),
    'root': '<HERMES_HOME>',
    'counts': {'files_seen': 0, 'by_suffix_top': []},
    'large_files_count': 0,
    'largest_files_top_10': [],
    'scan_truncated': False,
}
def path_class(p):
    parts = [x.lower() for x in p.parts]
    if 'logs' in parts: return 'log'
    if 'sessions' in parts or p.name == 'state.db': return 'session_db'
    if 'skills' in parts: return 'skill'
    if 'memories' in parts or 'memory' in parts: return 'memory'
    if 'cron' in parts: return 'cron'
    if 'browser' in parts: return 'browser'
    return 'other'
if root.exists():
    suffix_counts = {}
    sizes = []
    for idx, p in enumerate(root.rglob('*'), 1):
        if idx > max_files:
            out['scan_truncated'] = True
            break
        if not p.is_file():
            continue
        out['counts']['files_seen'] += 1
        suf = p.suffix or '<none>'
        suffix_counts[suf] = suffix_counts.get(suf, 0) + 1
        try:
            size = p.stat().st_size
        except Exception:
            continue
        if size > 1_000_000:
            out['large_files_count'] += 1
            sizes.append((size, path_class(p), p.suffix or '<none>', '<REDACTED:PATH>'))
    out['counts']['by_suffix_top'] = sorted(suffix_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    out['largest_files_top_10'] = [
        {'bytes': s, 'path_class': c, 'suffix': suf, 'path': red}
        for s, c, suf, red in sorted(sizes, reverse=True)[:10]
    ]
print(json.dumps(out, ensure_ascii=False, indent=2))
PY
```

Finding a large file is not permission to read it. Do not open large `.json`, `.jsonl`, `.md`, session, memory, or transcript files unless there is a specific bounded question and privacy approval.

Если вывод большой, не вставляй его в чат целиком. Сохрани summary:

```text
large_files_count:
largest_files_top_10:
subsystems_seen:
```

### 7.4 Gateway latency and compression logs

Не запускай recursive raw grep по всему Hermes home. Логи и JSONL могут содержать приватный текст. Используй count-only scan: он читает только безопасные `.log` / `.txt`, пропускает auth/session/memory/browser paths, смотрит хвост файла и печатает только counts.

```bash
python3 - <<'PY'
from pathlib import Path
import json, os, re

root = Path(os.environ.get('HERMES_HOME', str(Path.home()/'.hermes'))).expanduser()
patterns = {
    'response_ready': r'response ready',
    'compression': r'preflight compression|context compression|compression done|context summary|summary',
    'aux_timeout': r'auxiliary .*timeout|responses stream exceeded|failed to generate context summary',
    'retry_fallback': r'retry|fallback|rate limit|429|timeout|context_length|overloaded',
}
skip = re.compile(r'(auth|cookie|token|secret|key|browser|session|memory)', re.I)
allowed_suffixes = {'.log', '.txt'}
max_tail_bytes = 2_000_000
out = []

if root.exists():
    for p in root.rglob('*'):
        rel = str(p.relative_to(root))
        if not p.is_file() or p.suffix.lower() not in allowed_suffixes:
            continue
        if skip.search(rel):
            continue
        try:
            size = p.stat().st_size
            with p.open('rb') as f:
                if size > max_tail_bytes:
                    f.seek(size - max_tail_bytes)
                text = f.read().decode('utf-8', errors='ignore')
        except Exception:
            continue
        hits = {k: len(re.findall(v, text, re.I)) for k, v in patterns.items()}
        if any(hits.values()):
            out.append({'file': rel, 'bytes_scanned': min(size, max_tail_bytes), 'hits': hits})

print(json.dumps(sorted(out, key=lambda x: sum(x['hits'].values()), reverse=True)[:50], ensure_ascii=False, indent=2))
PY
```

### 7.5 Sessions aggregate only

Если есть SQLite `state.db`, смотри schema и aggregate counts. Не выбирай полный message text.

```bash
PROFILE="<PROFILE_NAME>"
ROOT="${HERMES_HOME:-$HOME/.hermes}"

for db in   "$ROOT/profiles/$PROFILE/state.db"   "$ROOT/state.db"
do
  if [ -f "$db" ]; then
    echo "state_db_found: $db"
    sqlite3 "$db" '.tables' 2>/dev/null || true
    sqlite3 "$db" '.schema' 2>/dev/null | head -200 || true
  fi
done
```

Никогда не делай вывод о session bloat, пока не проверен `state.db` именно целевого profile.

После schema можно адаптировать aggregate query:

```sql
SELECT COUNT(*) FROM sessions;
SELECT COUNT(*) FROM messages;
SELECT session_id, COUNT(*) AS message_count
FROM messages
GROUP BY session_id
ORDER BY message_count DESC
LIMIT 20;
```

Если schema другая - не ломайся. Напиши, что session backend differs.

### 7.6 Tools/MCP/skills scan

```bash
hermes --profile <PROFILE_NAME> tools list
hermes --profile <PROFILE_NAME> skills list
hermes --profile <PROFILE_NAME> mcp list 2>/dev/null || true
```

Metadata scan:

```bash
python3 - <<'PY'
from pathlib import Path
import json, os
root = Path(os.environ.get('HERMES_HOME', str(Path.home()/'.hermes'))).expanduser()
profile = '<PROFILE_NAME>'
targets = [root / 'skills', root / 'profiles' / profile / 'skills']
out = {'skills_roots_seen': [], 'skill_files_count': 0, 'mcp_related_files_count': 0, 'largest_skill_files_top_10': []}
sizes = []
for base in targets:
    if not base.exists():
        continue
    out['skills_roots_seen'].append('<HERMES_HOME>/' + str(base.relative_to(root)) if base.is_relative_to(root) else '<REDACTED:PATH>')
    for p in base.rglob('*'):
        if not p.is_file():
            continue
        out['skill_files_count'] += 1
        try:
            sizes.append((p.stat().st_size, p.suffix or '<none>', p.name[:80]))
        except Exception:
            pass
if root.exists():
    for p in root.rglob('*'):
        rel = str(p.relative_to(root)).lower()
        if 'mcp' in rel and p.is_file():
            out['mcp_related_files_count'] += 1
out['largest_skill_files_top_10'] = [{'bytes': s, 'suffix': suf, 'basename': name} for s, suf, name in sorted(sizes, reverse=True)[:10]]
print(json.dumps(out, ensure_ascii=False, indent=2))
PY
```

### 7.7 Cron/background/gateway processes

```bash
hermes cron list 2>/dev/null || true
hermes --profile <PROFILE_NAME> cron list 2>/dev/null || true
hermes --profile <PROFILE_NAME> gateway status 2>/dev/null || true
python3 - <<'PY'
import subprocess, re, json, os

patterns = {
  'hermes': re.compile(r'hermes', re.I),
  'gateway': re.compile(r'gateway', re.I),
  'mcp': re.compile(r'\bmcp\b', re.I),
  'browser': re.compile(r'browser|chrom|playwright', re.I),
  'worker': re.compile(r'worker|watch|cron', re.I),
}
secret_re = re.compile(
  r'(sk-[A-Za-z0-9_-]+|xox[baprs]-[A-Za-z0-9-]+|ghp_[A-Za-z0-9_]+|'
  r'AIza[0-9A-Za-z_-]+|Bearer\s+[A-Za-z0-9._-]+|'
  r'(?i)(api[_-]?key|token|secret|password|authorization)(=|\s+)[^\s]+|'
  r'https?://[^/\s:@]+:[^/\s:@]+@)'
)
out = {k: 0 for k in patterns}
samples = []
try:
    ps = subprocess.check_output(['ps', '-axo', 'pid=,ppid=,comm=,args='], text=True, errors='replace')
except Exception as e:
    print(json.dumps({'error': 'ps_failed', 'detail': str(e)}))
    raise SystemExit(0)
for line in ps.splitlines():
    matched = [name for name, rx in patterns.items() if rx.search(line)]
    if not matched:
        continue
    for name in matched:
        out[name] += 1
    parts = line.split(None, 3)
    pid = parts[0] if len(parts) > 0 else 'unknown'
    comm = os.path.basename(parts[2]) if len(parts) > 2 else 'unknown'
    args = parts[3] if len(parts) > 3 else ''
    args = secret_re.sub('<REDACTED>', args)
    args = re.sub(r'(/Users|/home)/[^ ]+', '<REDACTED:PATH>', args)
    samples.append({'pid': pid, 'comm': comm, 'class': matched[:3], 'args_hint': args[:120]})
print(json.dumps({'counts': out, 'samples_limited': samples[:20]}, ensure_ascii=False, indent=2))
PY
```

Не печатай full command line по умолчанию. Если нужны args для доказательства duplicate/runaway процесса, сначала спроси approval и redaction plan. Не убивай процессы. Только запиши count, sanitized command summary, likely owner.

### 7.8 Browser/vision/image evidence

Не печатай raw browser logs, screenshots, DOM dumps или session traces. Считай только частоты.

```bash
python3 - <<'PY'
from pathlib import Path
import json, os, re

root = Path(os.environ.get('HERMES_HOME', str(Path.home()/'.hermes'))).expanduser()
patterns = {
    'screenshot': r'screenshot',
    'browser_snapshot': r'browser_snapshot|page snapshot',
    'vision_image': r'browser_vision|vision|image',
    'dom_playwright': r'\bDOM\b|playwright|chromium|chrome',
}
skip = re.compile(r'(auth|cookie|token|secret|key|session|memory)', re.I)
allowed_suffixes = {'.log', '.txt'}
max_tail_bytes = 2_000_000
out = []

if root.exists():
    for p in root.rglob('*'):
        rel = str(p.relative_to(root))
        if not p.is_file() or p.suffix.lower() not in allowed_suffixes:
            continue
        if skip.search(rel):
            continue
        try:
            size = p.stat().st_size
            with p.open('rb') as f:
                if size > max_tail_bytes:
                    f.seek(size - max_tail_bytes)
                text = f.read().decode('utf-8', errors='ignore')
        except Exception:
            continue
        hits = {k: len(re.findall(v, text, re.I)) for k, v in patterns.items()}
        if any(hits.values()):
            out.append({'file': rel, 'bytes_scanned': min(size, max_tail_bytes), 'hits': hits})

print(json.dumps(sorted(out, key=lambda x: sum(x['hits'].values()), reverse=True)[:50], ensure_ascii=False, indent=2))
PY
```

Смотри counts и frequency. Не вставляй screenshots/log blobs в отчёт.

---

## 8. Triage decision tree

```text
START

1. Есть ли активный P0-расход прямо сейчас?
   - cron/gateway loop
   - retry/fallback storm
   - recursive delegation
   - browser/screenshot loop
   - duplicate gateway/processes
   YES -> classify P0, stop, ask approval for containment.
   NO -> continue.

2. Расход привязан к одной длинной session?
   YES -> inspect session size/message/tool patterns.
   NO -> inspect profile/global config.

3. Частая compression?
   YES -> check threshold, aux model, errors, repeated summaries.

4. Много tools/MCP/browser в обычной сессии?
   YES -> tool/schema bloat candidate.

5. Много skills loaded globally?
   YES -> skill bloat candidate.

6. Большая memory или session_search retrieval?
   YES -> persistent context/retrieval candidate.

7. Есть cron/background без явного запроса пользователя?
   YES -> hidden spend candidate.

8. Есть repeated errors/retries/fallbacks?
   YES -> multiplied billing candidate.

9. Используется heavy model/high reasoning для обычных задач?
   YES -> routing/model cost candidate.

10. Пользовательский workflow тащит большие logs/files/screenshots?
    YES -> workflow-driven context bloat.

11. Если evidence слабое:
    return INCONCLUSIVE with next bounded evidence needed.
```

---

## 9. Risk classes

### P0 - runaway spend now

Признаки:

- активный cron loop;
- gateway restart loop;
- duplicate gateway instances;
- background process генерирует tool/model calls;
- recursive delegation;
- retry/fallback storm;
- screenshot/browser loop.

Действие:

- остановить диагностику после достаточного evidence;
- предложить одну containment action;
- спросить approval.

### P1 - высокий постоянный расход

Признаки:

- каждая session начинается тяжело;
- tools/MCP/skills глобально раздуты;
- memory/session_search вытаскивает много;
- compression слишком частая;
- aux model дорогой.

Действие:

- remediation plan с backup/rollback;
- правки только после approval.

### P2 - умеренная неэффективность

Признаки:

- иногда большие tool outputs;
- нет reset policy;
- некоторые stale skills/memory;
- дорогая модель по привычке.

Действие:

- workflow/config hygiene;
- не срочно.

### P3 - профилактика

Признаки:

- можно улучшить habits, docs, monitoring;
- нет явного текущего drain.

Действие:

- recommendations only.

---

## 10. False positives

| Подозрение | Может быть ложным | Как проверить |
|---|---|---|
| Большой session DB | старые архивные данные не попадают в active prompt | проверить active session и recent prompt tokens |
| Большие logs | logs не тратят токены, пока агент их не читает | проверить tool transcripts, не disk size |
| Много installed skills | installed не значит loaded | проверить loaded skills per session |
| Много available tools | tool-search может скрывать schemas | проверить actual injection/cold-load |
| Browser processes | это может быть обычный Chrome | match parent/logs/profile |
| High bill | мог быть один легитимный большой run | сравнить timeline usage vs tasks |
| Compression events | compression сама по себе нормальная | искать repeated/failing/frequent compression |
| Memory large | не вся memory может инжектиться | проверить prompt assembly/retrieval |
| Cron exists | job может быть paused/rare | проверить enabled/last_run/next_run |
| Heavy model configured | session могла override cheaper model | проверить resolved model logs |
| Retry line | один retry нормален | считать bursts/repeated same error |

---

## 11. Report schema: YAML

Агент должен вернуть отчёт примерно в таком виде.

```yaml
token_drain_report:
  schema_version: "1.0.0"
  mode: diagnosis_only
  generated_at: "<ISO_8601_OR_UNKNOWN>"
  target:
    hermes_home: "<HERMES_HOME_OR_UNKNOWN>"
    profile: "<PROFILE_NAME_OR_UNKNOWN>"
    project_root: "<PROJECT_ROOT_OR_UNKNOWN>"
    platform: "cli|telegram|discord|slack|api|cron|unknown"
    time_window:
      since: "<SINCE_OR_UNKNOWN>"
      until: "<UNTIL_OR_NOW>"
  privacy:
    secrets_read: false
    secrets_printed: false
    raw_private_messages_read: false
    redactions:
      - type: "api_key|token|cookie|private_text|path|other"
        count: 0
  discovery:
    read_only: true
    commands_run:
      - command: "<REDACTED_OR_SUMMARIZED_COMMAND>"
        purpose: "<WHY>"
        exit_code: 0
        result_summary: "<SUMMARY_NOT_RAW_DUMP>"
    files_inspected_metadata_only:
      - path_class: "config|log|session_db|memory|skill|cron|other"
        size_or_count: "<SIZE_OR_COUNT>"
        content_dumped: false
  metrics:
    usage_baseline:
      source: "hermes_insights|provider_dashboard|logs|unavailable"
      time_window: "<WINDOW>"
      total_input_tokens: null
      total_output_tokens: null
      total_cost: null
      currency: null
      calls_count: null
      top_models_by_cost: []
      top_sessions_by_tokens: []
    active_sessions_count: null
    largest_session_message_count: null
    compression_events_last_24h: null
    retry_or_fallback_events_last_24h: null
    enabled_toolsets_count: null
    mcp_servers_count: null
    loaded_skills_count: null
    memory_total_size: null
    cron_jobs_enabled: null
    gateway_process_count: null
    background_process_count: null
    browser_or_vision_events: null
  ranked_causes:
    - rank: 1
      cause: "context_bloat|compression_loop|tool_schema_bloat|skill_bloat|memory_bloat|aux_model_cost|cron_loop|gateway_restart_loop|background_task|browser_mcp_noise|delegation_loop|verbose_tool_output|large_pasted_files|tool_loop|high_reasoning|wrong_model_routing|no_reset_policy|retry_fallback_storm|vision_cost|docs_prompt_bloat|unknown"
      risk_class: "P0|P1|P2|P3"
      confidence: "high|medium|low"
      evidence:
        - "<FACT_WITH_SOURCE>"
      why_it_matters: "<SHORT_REASON>"
      false_positives_checked:
        - "<CHECK>"
  remediation_options:
    - option_id: "A"
      title: "<ACTION_TITLE>"
      risk_class: "P0|P1|P2|P3"
      expected_impact: "high|medium|low|unknown"
      action_type: "containment|session_hygiene|tool_hygiene|skill_hygiene|memory_hygiene|provider_routing|cron_gateway|workflow_change|monitoring"
      requires_approval: true
      exact_change_scope:
        files: []
        commands: []
        processes: []
        settings: []
      rollback: "<HOW_TO_REVERSE>"
      verification: "<HOW_TO_CHECK_AFTER>"
  stop_point:
    stopped_before_changes: true
    next_step_requires_approval: true
    approval_prompt: "Approve option <ID> only?"
  limitations:
    - "Exact token/cost attribution unavailable unless provider/Hermes usage telemetry exposes it."
  evidence_gaps:
    - "provider_usage_unavailable"
    - "session_schema_unknown"
  status: "diagnosed|inconclusive|blocked"
```

`requires_approval: false` допустимо только для advice-only рекомендаций без команд, edits, process/session/config changes, external side effects или settings changes.

---

## 12. Report schema: JSON

```json
{
  "token_drain_report": {
    "schema_version": "1.0.0",
    "mode": "diagnosis_only",
    "generated_at": "<ISO_8601_OR_UNKNOWN>",
    "target": {
      "hermes_home": "<HERMES_HOME_OR_UNKNOWN>",
      "profile": "<PROFILE_NAME_OR_UNKNOWN>",
      "project_root": "<PROJECT_ROOT_OR_UNKNOWN>",
      "platform": "cli|telegram|discord|slack|api|cron|unknown",
      "time_window": {
        "since": "<SINCE_OR_UNKNOWN>",
        "until": "<UNTIL_OR_NOW>"
      }
    },
    "privacy": {
      "secrets_read": false,
      "secrets_printed": false,
      "raw_private_messages_read": false,
      "raw_private_messages_printed": false,
      "private_text_content_scanned_for_counts": "none|bounded_logs_tail|unknown",
      "redactions": []
    },
    "discovery": {
      "read_only": true,
      "commands_run": [],
      "files_inspected_metadata_only": []
    },
    "metrics": {
      "usage_baseline": {
        "source": "hermes_insights|provider_dashboard|logs|unavailable",
        "time_window": "<WINDOW>",
        "total_input_tokens": null,
        "total_output_tokens": null,
        "total_cost": null,
        "currency": null,
        "calls_count": null,
        "top_models_by_cost": [],
        "top_sessions_by_tokens": []
      },
      "active_sessions_count": null,
      "largest_session_message_count": null,
      "compression_events_last_24h": null,
      "retry_or_fallback_events_last_24h": null,
      "enabled_toolsets_count": null,
      "mcp_servers_count": null,
      "loaded_skills_count": null,
      "memory_total_size": null,
      "cron_jobs_enabled": null,
      "gateway_process_count": null,
      "background_process_count": null,
      "browser_or_vision_events": null
    },
    "ranked_causes": [
      {
        "rank": 1,
        "cause": "unknown",
        "risk_class": "P2",
        "confidence": "low",
        "evidence": [],
        "why_it_matters": "",
        "false_positives_checked": []
      }
    ],
    "remediation_options": [
      {
        "option_id": "A",
        "title": "",
        "risk_class": "P2",
        "expected_impact": "unknown",
        "action_type": "containment|session_hygiene|tool_hygiene|skill_hygiene|memory_hygiene|provider_routing|cron_gateway|workflow_change|monitoring|workflow_advice",
        "requires_approval": true,
        "exact_change_scope": {
          "files": [],
          "commands": [],
          "processes": [],
          "settings": []
        },
        "rollback": "",
        "verification": ""
      }
    ],
    "limitations": [
      "Exact token/cost attribution unavailable unless provider/Hermes usage telemetry exposes it."
    ],
    "evidence_gaps": [
      "provider_usage_unavailable",
      "session_schema_unknown"
    ],
    "stop_point": {
      "stopped_before_changes": true,
      "next_step_requires_approval": true,
      "approval_prompt": "Approve option A only?"
    },
    "status": "diagnosed|inconclusive|blocked"
  }
}
```

---

## 13. Remediation options library

Не применять автоматически. Это библиотека вариантов для plan после диагностики.

### 13.1 P0 containment

Только если evidence показывает текущий runaway.

| Причина | Возможное действие | Approval |
|---|---|---|
| cron loop | pause конкретный job | `APPROVE PAUSE CRON <job_id>` |
| duplicate gateway | stop конкретный duplicate process | `APPROVE STOP DUPLICATE GATEWAY <pid>` |
| retry storm | временно отключить failing route / снизить retry cap | `APPROVE CONTAIN RETRY LOOP <scope>` |
| browser loop | stop конкретный browser worker | `APPROVE STOP BROWSER WORKER <pid>` |
| delegation loop | stop/disable конкретную route/session | `APPROVE STOP DELEGATION LOOP <scope>` |

### 13.2 Session hygiene

- начать новую session для новой темы;
- закрыть/архивировать старую session после report;
- добавить reset policy;
- не вставлять полные logs/files в чат;
- давать file path и просить читать bounded sections;
- после длинного расследования делать summary и закрывать ветку.

### 13.3 Tool/MCP hygiene

- отключить глобально неиспользуемые MCP servers;
- вынести browser tools в explicit opt-in;
- включить tool-search/progressive disclosure при большом tool count;
- отключить tool-search для tiny toolsets, если cold-load дороже;
- сократить custom tool schemas;
- не держать редкие tools always-on.

### 13.4 Skill hygiene

- загружать skills по задаче, не все сразу;
- разделить большой skill на узкие;
- убрать дублирующие инструкции;
- добавить routing rules;
- не хранить большие reference docs внутри always-loaded skill.

### 13.5 Memory/session_search hygiene

- deduplicate memory;
- вынести длинные operational notes в docs/wiki/reference;
- держать memory короткой;
- настроить retrieval size;
- перевести session_search/compression на cheaper auxiliary model, если качество позволяет.

### 13.6 Provider/model routing

- снизить reasoning для routine tasks;
- использовать cheap/default model для простых запросов;
- дорогую модель оставить для heavy diagnostics/implementation;
- проверить fallback chain, чтобы error не прыгал на слишком дорогой model;
- explicit context_length только если модель/provider реально поддерживает.

### 13.7 Cron/gateway hygiene

- увеличить interval низкоценным jobs;
- добавить max runtime/max turns/max retries;
- убрать duplicate jobs после migration;
- включить backoff;
- держать один gateway instance на profile/platform, если иное не нужно.

### 13.8 Browser/vision hygiene

- предпочитать `web_extract`/text over screenshots;
- ограничить screenshot frequency/resolution;
- закрывать browser sessions после задачи;
- не тащить полный DOM, если нужен один selector;
- использовать targeted queries.

### 13.9 Tool output hygiene

- pagination by default;
- limit lines;
- extract fields from JSON;
- сохранять huge output в file и summarise;
- не вставлять целые логи в chat.

---

## 14. Approval gate before fixes

После diagnosis агент обязан остановиться.

Используй такую формулировку:

```text
Я нашёл вероятную причину расхода: <CAUSE>.
Уверенность: <high|medium|low>.
Риск: <P0|P1|P2|P3>.
Я ничего не менял.

Могу предложить точечное действие:
<option_id>: <ACTION>
Затронет: <files/processes/settings>
Откат: <rollback>
Проверка после: <verification>

Подтвердить только это действие?
```

Запрещено:

```text
Я заодно почистил...
Я уже отключил...
Я поправил конфиг...
Я перезапустил gateway...
Я удалил старые sessions...
```

Без явного approval это брак.

---

## 15. Stop rules

Остановиться и спросить человека, если:

1. найден P0 runaway;
2. следующий шаг требует edit/delete/restart/kill/pause;
3. надо читать secrets/private messages/auth;
4. команда даст огромный output;
5. найдено 3+ high-confidence causes;
6. scope непонятен;
7. Hermes home/profile не найден безопасно;
8. сама диагностика начинает становиться token drain;
9. есть риск залезть в чужой profile/project/account.

Фраза stop:

```text
Останавливаюсь здесь. Дальше без approval будет уже не read-only диагностика.
```

---

## 16. Copy-paste helper: safe metadata scan

Helper ниже собирает metadata summary и не печатает contents.

```bash
python3 - <<'PY'
from pathlib import Path
import json, os
root = Path(os.environ.get('HERMES_HOME', str(Path.home()/'.hermes'))).expanduser()
out = {
    'root_exists': root.exists(),
    'root': '<HERMES_HOME>',
    'top_large_files': [],
    'counts': {},
}
if root.exists():
    files = [p for p in root.rglob('*') if p.is_file()]
    out['counts']['files_total'] = len(files)
    by_suffix = {}
    for p in files:
        by_suffix[p.suffix or '<none>'] = by_suffix.get(p.suffix or '<none>', 0) + 1
    out['counts']['by_suffix_top'] = sorted(by_suffix.items(), key=lambda x: x[1], reverse=True)[:20]
    sizes = []
    for p in files:
        try:
            sizes.append((p.stat().st_size, str(p.relative_to(root))))
        except Exception:
            pass
    out['top_large_files'] = [{'path': path, 'bytes': size} for size, path in sorted(sizes, reverse=True)[:20]]
print(json.dumps(out, ensure_ascii=False, indent=2))
PY
```

---

## 17. Copy-paste helper: log keyword counts

Не печатает raw logs. Читает только `.log` / `.txt`, пропускает auth/session/memory/browser paths, смотрит хвост файла и возвращает counts.

```bash
python3 - <<'PY'
from pathlib import Path
import json, os, re

root = Path(os.environ.get('HERMES_HOME', str(Path.home()/'.hermes'))).expanduser()
patterns = {
    'compression': r'compression|compress|summary',
    'retry_fallback': r'retry|fallback|timeout|rate limit|429|context_length',
    'tool_loop': r'tool call|tool_calls|max_turns',
    'browser_mcp': r'screenshot|browser|mcp|playwright|chromium',
    'cron_gateway': r'cron|gateway restart|reconnect',
    'aux_timeout': r'responses stream exceeded|auxiliary .*timeout',
}
skip = re.compile(r'(auth|cookie|token|secret|key|session|memory|browser_profile)', re.I)
allowed_suffixes = {'.log', '.txt'}
max_tail_bytes = 2_000_000
out = []

if root.exists():
    for p in root.rglob('*'):
        rel = str(p.relative_to(root))
        if not p.is_file() or p.suffix.lower() not in allowed_suffixes:
            continue
        if skip.search(rel):
            continue
        try:
            size = p.stat().st_size
            with p.open('rb') as f:
                if size > max_tail_bytes:
                    f.seek(size - max_tail_bytes)
                text = f.read().decode('utf-8', errors='ignore')
        except Exception:
            continue
        hits = {k: len(re.findall(v, text, re.I)) for k, v in patterns.items()}
        hits = {k: v for k, v in hits.items() if v}
        if hits:
            out.append({'file': rel, 'bytes_scanned': min(size, max_tail_bytes), 'hits': hits})

print(json.dumps(sorted(out, key=lambda x: sum(x['hits'].values()), reverse=True)[:50], ensure_ascii=False, indent=2))
PY
```

---

## 18. Copy-paste helper: process summary

```bash
python3 - <<'PY'
import subprocess, re, json

keywords = re.compile(r'hermes|gateway|cron|mcp|browser|chrom|playwright|node|python|worker|watch', re.I)
classes = {
    'hermes_processes': re.compile(r'hermes', re.I),
    'gateway_processes': re.compile(r'gateway', re.I),
    'browser_processes': re.compile(r'browser|chrom|playwright', re.I),
    'mcp_processes': re.compile(r'mcp', re.I),
    'watcher_like_processes': re.compile(r'watch|worker|cron', re.I),
}
out = {k: 0 for k in classes}
out['matched_processes_total'] = 0
out['sample_process_names'] = []
try:
    ps = subprocess.check_output(['ps', '-axo', 'pid=,comm='], text=True, errors='replace')
except Exception as e:
    print(json.dumps({'error': str(e)}, indent=2))
    raise SystemExit(0)
for line in ps.splitlines():
    if not keywords.search(line):
        continue
    out['matched_processes_total'] += 1
    name = line.strip().split(None, 1)[-1] if line.strip() else '<unknown>'
    if len(out['sample_process_names']) < 20:
        out['sample_process_names'].append(name)
    for key, rx in classes.items():
        if rx.search(line):
            out[key] += 1
print(json.dumps(out, ensure_ascii=False, indent=2))
PY
```

Полные command lines не печатать по умолчанию. Если нужны args для доказательства duplicate/runaway процесса, сначала спроси approval и redaction plan.

Если список длинный, агент должен summarize:

```yaml
process_summary:
  hermes_processes: 0
  gateway_processes: 0
  browser_processes: 0
  mcp_processes: 0
  watcher_like_processes: 0
  suspicious_duplicates: []
```

---

## 19. Smoke tests for this MD

Перед публикацией или передачей файла проверь сам файл.

### 19.1 Required headings

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('hermes-token-drain-diagnostic-kit.md').read_text()
required = [
  'Safety contract',
  'Beginner path',
  'Scope selector',
  'Quick triage',
  'Read-only discovery commands',
  'Triage decision tree',
  'Risk classes',
  'Report schema',
  'Approval gate before fixes',
  'Stop rules',
  'Smoke tests',
  'Acceptance checklist'
]
missing = [h for h in required if h not in text]
print({'missing': missing})
raise SystemExit(1 if missing else 0)
PY
```

### 19.2 Privacy scan

```bash
python3 - <<'PY'
from pathlib import Path
import re
text = Path('hermes-token-drain-diagnostic-kit.md').read_text()
patterns = [
    '<PRIVATE_' + 'PATH>',
    '/ho' + 'me/' + r'[^<\s`]+',
    'Desk' + 'top/' + r'[^<\s`]+',
    r'sk-[A-Za-z0-9]',
    r'xox[baprs]-',
    r'api[_-]?key\s*=',
    r'token\s*=',
    r'password\s*=',
    r'BEGIN (RSA|OPENSSH|PRIVATE) KEY',
]
rx = re.compile('|'.join(patterns), re.I)
for i, line in enumerate(text.splitlines(), 1):
    if rx.search(line) and 'patterns = [' not in line and 'Desk' + 'top/' not in line:
        print(f'{i}: <POTENTIAL_PRIVATE_PATTERN>')
PY
```

Expected: no private real values. Matches inside test examples must be generic placeholders or regex patterns.

### 19.3 Markdown fence balance

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('hermes-token-drain-diagnostic-kit.md').read_text()
fence = '`' * 3
count = text.count(fence)
print({'fences': count, 'balanced': count % 2 == 0})
raise SystemExit(0 if count % 2 == 0 else 1)
PY
```

### 19.4 Runtime behavior smoke

```bash
hermes --profile <PROFILE_NAME> chat -q "Use token-drain-diagnostic. Do discovery only. Do not change files. Return YAML report skeleton with unknown values as null."
```

Expected:

- no edits;
- no secret printing;
- structured report;
- `requires_approval: true` for fixes;
- `stopped_before_changes: true`.

### 19.5 Frontmatter and Python snippets

```bash
python3 - <<'PY'
from pathlib import Path
import re, ast, yaml
text = Path('hermes-token-drain-diagnostic-kit.md').read_text()
fm = text.split('---', 2)[1]
yaml.safe_load(fm)
for i, block in enumerate(re.findall(r'```python\n(.*?)```', text, re.S), 1):
    ast.parse(block)
for i, block in enumerate(re.findall(r"python3 - <<'PY'\n(.*?)\nPY", text, re.S), 1):
    ast.parse(block)
print('frontmatter_and_python_snippets_ok')
PY
```

### 19.6 Destructive command scan

```bash
python3 - <<'PY'
from pathlib import Path
import re
text = Path('hermes-token-drain-diagnostic-kit.md').read_text()
pattern = re.compile(r'(?im)^\s*(rm\s+-rf|kill\s+-9|pkill|reboot|shutdown|launchctl|systemctl|hermes\s+.*\b(delete|prune|reset|remove|disable|pause|stop|restart|fix|repair)\b)')
hits = [(m.start(), m.group(0)) for m in pattern.finditer(text)]
print({'dangerous_default_commands_seen': hits})
# Expected: empty, or only examples explicitly marked approval-required / human setup.
PY
```

---

## 20. Example reports

### Example A: session/context bloat

```yaml
token_drain_report:
  ranked_causes:
    - rank: 1
      cause: context_bloat
      risk_class: P1
      confidence: high
      evidence:
        - "largest active session has very high message count"
        - "recent turns include large tool outputs"
      why_it_matters: "Old context is likely carried into new requests."
  remediation_options:
    - option_id: A
      title: "Start fresh session for new tasks and archive current long session after summary"
      requires_approval: true
      expected_impact: high
      rollback: "old session remains searchable; resume if needed"
      verification: "new session starts without repeated compression"
  stop_point:
    stopped_before_changes: true
```

### Example B: retry/fallback storm

```yaml
token_drain_report:
  ranked_causes:
    - rank: 1
      cause: retry_fallback_storm
      risk_class: P0
      confidence: medium
      evidence:
        - "recent logs show repeated timeout/fallback around same request"
      why_it_matters: "One user request may be billed multiple times."
  remediation_options:
    - option_id: A
      title: "Contain retry loop for the failing route"
      requires_approval: true
      expected_impact: high
      rollback: "restore previous retry/fallback config from backup"
      verification: "same request fails once cleanly or succeeds without repeated retries"
  stop_point:
    stopped_before_changes: true
```

### Example C: too many tools/MCP

```yaml
token_drain_report:
  ranked_causes:
    - rank: 1
      cause: tool_schema_bloat
      risk_class: P1
      confidence: medium
      evidence:
        - "many toolsets/MCP servers are enabled for routine chat profile"
      why_it_matters: "Tool schemas can inflate prompt even when task does not need them."
  remediation_options:
    - option_id: A
      title: "Move rare tools to opt-in profile/toolset"
      requires_approval: true
      expected_impact: medium
      rollback: "re-enable previous toolset list from backup"
      verification: "simple chat turn has lower prompt/tool schema load"
```

### Example D: user workflow drain

```yaml
token_drain_report:
  ranked_causes:
    - rank: 1
      cause: large_pasted_files
      risk_class: P2
      confidence: high
      evidence:
        - "recent task included pasted full logs instead of file path + bounded read"
      why_it_matters: "The pasted material stays in session context."
  remediation_options:
    - option_id: A
      title: "Use file paths and bounded extraction instead of pasting full logs"
      requires_approval: false
      action_type: workflow_advice
      system_change: false
      expected_impact: medium
      rollback: "workflow-only advice, no system change"
      verification: "next diagnostic uses bounded excerpts and fewer compression events"
```

---

## 21. Acceptance checklist

### Author release checklist

Файл готов к публикации, если:

- [ ] новичок понимает первый экран;
- [ ] есть safety contract до команд;
- [ ] есть режимы: skill/helper/AGENTS/plain checklist;
- [ ] есть scope selector;
- [ ] есть список частых token drains;
- [ ] есть read-only discovery commands;
- [ ] есть false positives;
- [ ] есть risk classes P0-P3;
- [ ] есть YAML/JSON report schema;
- [ ] есть approval gate before fixes;
- [ ] есть stop rules;
- [ ] есть remediation library;
- [ ] есть smoke tests;
- [ ] есть examples;
- [ ] нет приватных путей, имён, токенов, secrets;
- [ ] markdown fences balanced;
- [ ] helper snippets syntax-check pass where possible.

### Operator run checklist

Перед запуском диагностики:

- [ ] выбран profile/project scope;
- [ ] подтверждён read-only режим;
- [ ] выбран time window;
- [ ] usage baseline найден или отмечен unavailable;
- [ ] запрет на secrets/raw logs подтверждён;
- [ ] ranked causes returned;
- [ ] remediation options требуют approval, кроме advice-only;
- [ ] агент остановился до правок.

---

## 22. Minimal prompt to give your agent

Если не хочется передавать весь файл, можно начать с этого. Но лучше всё-таки дать полный MD.

```text
Use Hermes Token-Drain Diagnostic Kit.
Diagnose why Hermes Agent may be spending too many tokens.
Work read-only.
Do not edit config, memory, skills, tools, cron, gateway, sessions, browser state, processes or files without explicit approval.
Do not print secrets.
Check active sessions, compression, prompt/tool/schema bloat, skills, memory/session_search, provider/aux model routing, cron loops, gateway restart loops, background jobs, browser/MCP noise, recursive delegation, verbose tool output, pasted large files, max_turn/tool loops, high reasoning, wrong model/context length, no reset policy, retry/fallback storms and screenshots/images.
Return ranked causes, evidence, confidence, risk class, false positives, and safe remediation options.
Stop before fixes and ask approval for one exact action.
```

---

## 23. Remediation receipt

Если пользователь одобрил конкретную remediation option и агент применил изменение, после проверки нужен receipt.

```yaml
remediation_receipt:
  applied: true
  approval_received: "<EXACT_APPROVAL_TEXT>"
  changes_made:
    - type: "config|session|cron|process|workflow|other"
      target: "<REDACTED_OR_SUMMARIZED_TARGET>"
      summary: "<WHAT_CHANGED>"
  verification_results:
    - "<COMMAND_OR_CHECK_SUMMARY>"
  rollback_available: true
  rollback: "<HOW_TO_REVERSE>"
  follow_up_needed: []
```

Если approval не было:

```yaml
remediation_receipt:
  applied: false
  approval_received: null
  changes_made: []
```

---

## 24. Final rule

Хорошая диагностика token drain должна быть короче, чем сам drain.

Если агент ради поиска расхода начинает читать все логи, все sessions, все memories и все файлы подряд - он сам стал проблемой.

Нормальный маршрут:

```text
scope -> bounded evidence -> top 1-3 causes -> remediation plan -> approval -> one fix -> verify -> receipt
```

Не больше.

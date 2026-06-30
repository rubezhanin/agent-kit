# Local Embedding and Memory Index

> Canonical English version. The reference brief lives at `source/memory-knowledge/agent-user-local-embedding-brief.md`. This page describes how the kit expects the memory index layer to behave.

The kit ships with a **read-only memory index** as an optional retrieval layer. It is not the canonical source of truth — wiki, references and reports are. The index exists to make the long-form sources cheap to search.

## Idea in one sentence

The agent should **search** verified sources, **cite** the path, and **say so** when sources are insufficient — instead of relying on a growing durable memory.

## Recommended stack

For self-hosting on a single Mac mini / Linux box / small VPS:

```text
Python 3.10+
fastembed
sentence-transformers/paraphrame-multilingual-MiniLM-L12-v2
SQLite with FTS5
Markdown / text source documents
read-only search tool exposed to the agent
```

Why this model:

- multilingual (Russian / English);
- small (~120 MB on disk);
- CPU-only;
- good enough for wiki, instructions and procedures.

## Where it runs

Three layouts are acceptable:

1. **Fully local.** All data, model and index on the same machine. Recommended for a single owner.
2. **Local model + remote index.** Model on the agent's machine, index in a private DB.
3. **Remote model, local data.** Use only with audited third-party APIs and never for owner-context.

Any layout that **leaks** owner-context to a public embedding API is forbidden by default — see `wiki/security-checklist.md`.

## Memory index contract

The kit treats the memory index as a search tool with these properties:

| Property | Default |
| --- | --- |
| Mode | `read_only` |
| Top-k per query | `5` |
| Canonical | `false` — retrieval is search, not truth |
| Indexes | `wiki/`, `references/`, `reports/` — explicitly allowed list |
| Excludes | `owner-context/`, `secrets/`, `.env`, raw Telegram cache |

When the agent uses it, the answer must cite the source path. When the answer returns nothing, the agent must say so explicitly.

## What is NOT in the index

- `owner-context/` — privacy boundary.
- `secrets/`, `.env`, `.pem`, `.key` — secrets.
- Raw Telegram cache — both a privacy and a hygiene concern.
- Durably stored chat history — that's where memory poisoning starts.

## Embedding workflow

1. Owner keeps canonical sources in `wiki/`, `references/`, `reports/`.
2. A cron / manual job ingests new files; for each it builds a FTS5 entry and (if enabled) a vector entry.
3. The agent only sees a search tool; never a write tool.
4. Every search call returns `(chunk_path, score, snippet)` — the agent stitches the answer from the snippets.

## Prompt pattern

```text
# Goal
Answer the question using only the memory index and the wiki.

# Process
1. Search the index with 1–3 queries.
2. If results are weak, say so explicitly.
3. Compose the answer, citing the source path after each non-trivial claim.
4. List what you did not find.

# Stop rule
If the question depends on data not present in the sources, return
`NEEDS_OWNER_CONTEXT` and ask for the missing file.
```

## Failure modes

| Failure | Why it happens | Mitigation |
| --- | --- | --- |
| Index returns stale docs. | No cleanup cron. | Weekly `reports/audits/`. |
| Index returns wrong chunk top-1. | Vector similarity ≠ relevance. | Always return top-5 and read at least three. |
| Owner-context leaks into index. | Crawler not whitelisted. | Hard-coded allow-list. |
| Index poisoned via web content. | External content written to wiki. | Strict write policy: wiki writes need approval. |

## References in this repo

- `source/memory-knowledge/agent-user-local-embedding-brief.md` — the full brief.
- `wiki/memory-policy.md` — durable memory, wiki, reports, index layering.
- `agent-center/skills/operations/wiki-memory/SKILL.md` — the skill that wraps this.
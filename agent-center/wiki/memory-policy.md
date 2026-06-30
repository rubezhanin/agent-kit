# Memory Policy

## Durable Memory

Store only:

- stable owner preferences;
- stable environment pointers;
- recurring corrections;
- compact facts that remain useful after a month.

Do not store:

- task progress;
- raw logs;
- long reports;
- secrets;
- temporary todos;
- claims copied from unverified sources.

## Wiki

Wiki is the canonical structured knowledge layer.

Use it for:

- architecture;
- operating contracts;
- team roster;
- source map;
- recurring decisions;
- stable project facts.

## Reports

Reports are evidence, not memory.

Use them for:

- receipts;
- audits;
- health checks;
- incident notes;
- verification results.

## Memory Index

Memory index is a read-only retrieval layer over wiki/references/reports.

Rules:

- search first when local knowledge matters;
- cite or name source path;
- if search returns nothing, say so;
- do not treat vector similarity as proof.


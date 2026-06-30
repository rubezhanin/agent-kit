# Smoke Test — Missing Brand Data

Input:

```text
Сделай карусель для моего бизнеса. Больше ничего не скажу.
```

Expected:

- agent does not create final carousel immediately;
- starts brand intake;
- asks concise questions;
- if forced, marks assumptions.

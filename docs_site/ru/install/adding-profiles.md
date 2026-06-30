# Добавление профилей

> Зеркало `docs/ADDING_PROFILES.ru.md`. English — [here](../../en/install/adding-profiles.md).

Kit манифестно-управляемый. Чтобы добавить нового агента — добавьте файлы. **Не редактируйте установщик.**

## Минимальный новый профиль

Создайте:

```text
agent-center/profiles/<profile-name>.profile.json
agent-center/skills/<group>/<profile-name>/SKILL.md
```

Пример:

```json
{
  "name": "support-analyst",
  "title": "Support Analyst",
  "type": "specialist",
  "default_enabled": false,
  "description": "Анализирует тикеты поддержки и находит повторяющиеся проблемы.",
  "skills": ["support-analyst"],
  "approval_required_for": ["customer_data_export"],
  "forbidden_by_default": ["dm_users", "refunds"],
  "outputs": ["issue_clusters", "faq_candidates", "handoff_report"]
}
```

Установщик авто-обнаруживает:

```text
agent-center/profiles/*.profile.json
```

## Используйте profile-factory skill

```text
Use profile-factory.
Create a profile for: [description].
First ask intake questions, then return a dry-run change packet.
Do not write files until I approve.
```

CLI-помощник:

```bash
python scripts/create_profile_skeleton.py "Support Analyst" \
  --description "Анализирует тикеты поддержки и находит повторяющиеся проблемы." \
  --group specialists
```

## Чек-лист перед публикацией

- [ ] profile JSON валиден;
- [ ] `SKILL.md` имеет frontmatter `name` и `description`;
- [ ] stop-rules явные;
- [ ] нет секретов или приватных путей;
- [ ] есть smoke-test;
- [ ] `docs/AGENT_SKILL_MATRIX.ru.md` обновлён.
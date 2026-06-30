# Adding Profiles (English)

> Canonical English version. Russian localization: [`docs/ADDING_PROFILES.ru.md`](docs/ADDING_PROFILES.ru.md).

The kit is manifest-driven.

To add a new agent profile, add files. Do not edit the installer.

## Minimal new profile

Create:

```text
agent-center/profiles/<profile-name>.profile.json
agent-center/skills/<group>/<profile-name>/SKILL.md
```

Example:

```json
{
  "name": "support-analyst",
  "title": "Support Analyst",
  "type": "specialist",
  "default_enabled": false,
  "description": "Analyzes support tickets and finds repeated issues.",
  "skills": ["support-analyst"],
  "approval_required_for": ["customer_data_export"],
  "forbidden_by_default": ["dm_users", "refunds"],
  "outputs": ["issue_clusters", "faq_candidates", "handoff_report"]
}
```

The installer auto-discovers:

```text
agent-center/profiles/*.profile.json
```

## Use the profile factory

Agent workflow:

```text
Use profile-factory.
Create a profile for: [description].
First ask intake questions, then return a dry-run change packet.
Do not write files until I approve.
```

CLI helper:

```bash
python scripts/create_profile_skeleton.py "Support Analyst" \
  --description "Analyzes support tickets and finds repeated issues." \
  --group specialists
```

PowerShell:

```powershell
python .\scripts\create_profile_skeleton.py "Support Analyst" --description "Analyzes support tickets and finds repeated issues." --group specialists
```

## Profile fields

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | Stable slug. File should be `<name>.profile.json`. |
| `title` | yes | Human-readable title. |
| `type` | yes | `primary`, `specialist`, `risk-review`, `operations`, `optional`, `optional-integration`. |
| `default_enabled` | yes | Whether setup suggests enabling it by default. |
| `disabled_by_default` | no | Harder opt-in for risky profiles. |
| `description` | yes | Routing description. |
| `skills` | yes | Skill names used by this profile. |
| `approval_required_for` | recommended | Actions needing explicit owner approval. |
| `forbidden_by_default` | recommended | Actions blocked unless separately enabled. |
| `outputs` | recommended | Expected artifacts. |

## Checklist

Before publishing a new profile:

- profile JSON is valid;
- `SKILL.md` has frontmatter `name` and `description`;
- stop rules are explicit;
- no secrets or private paths;
- smoke test exists;
- `AGENT_SKILL_MATRIX.md` is updated if the profile is part of the default public kit.
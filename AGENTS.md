# AGENTS.md

For agents working on this repository, not with it. To use the skill, read `SKILL.md`. This file only covers maintaining the skill.

`SKILL.md` is what agents run. `docs/design.md` is what constrains it. When they disagree, the design wins until the design is amended.

## Genericity test

Before adding a sentence to `SKILL.md`, replace its domain nouns with nouns from another domain. If the sentence stops being true, it belongs in a vault's schema, not in the skill.

Examples use invented content only. Never a real person, organization, table, system, or path.

## Frontmatter

Keep it to the fields allowed by the [Agent Skills specification](https://agentskills.io/specification): `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`.

Do not add fields that only one agent product reads. A vendor-neutral format is worth more than any single product's convenience.

## Before committing

Validate the skill. Use an absolute path; a relative one makes the directory name empty and the check fail.

```
uvx --from "git+https://github.com/agentskills/agentskills#subdirectory=skills-ref" skills-ref validate <skill directory>
```

## Writing

- Imperative mood in the body, third person in the description. No second person.
- Keep `SKILL.md` short. Move detail into `references/` only when an operation genuinely needs it.
- State a rule once. If two files need it, one owns it and the other points.

## Changing the skill

- Add a rule only when a case needed it. Remove one only for a hard constraint, the same bar as splitting a vault. Without this the skill erodes toward whatever was convenient last week.
- A change usually starts as a `revisions.md` record in some vault. Quote its id in the commit, and name the rule that changed.
- An invariant is the exception. Changing one changes what the pattern is: say so in the commit, and amend `docs/design.md` in the same commit.
- Prefer deleting a rule to adding another. A skill that keeps growing stops being abstract.

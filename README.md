# llm-driven

An agent skill for Andrej Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern. The agent compiles your sources into a persistent, interlinked markdown wiki and keeps it current.

**Status:** early. `SKILL.md` covers setting up a vault and revising the skill; ingest, query, lint, and divide are outlined only. See [docs/design.md](docs/design.md) for goals and boundaries.

## What this adds to the original

- Two times on every ingest: when it was recorded and when the content actually happened, so old material can be back-filled safely.
- Pointers: a vault can point to knowledge that lives elsewhere instead of copying it.
- Rules for dividing knowledge into vaults.

## Layout

The repository root is the skill root, in the open [Agent Skills](https://agentskills.io/specification) format.

```
llm-driven/
├── SKILL.md
├── AGENTS.md            # how to maintain this repository
├── README.md
├── assets/
│   └── vault-template/  # AGENTS.md, index.md, log.md for a new vault
└── docs/
    └── design.md
```

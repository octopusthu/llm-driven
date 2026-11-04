# llm-driven

An agent skill for Andrej Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern. The agent compiles your sources into a persistent, interlinked markdown wiki and keeps it current.

**Status:** scaffold. `SKILL.md` has its trigger description and an outline of operations; detailed instructions are not written yet. See [docs/design.md](docs/design.md) for goals and boundaries.

## What this adds to the original

- Two times on every ingest: when it was recorded and when the content actually happened, so old material can be back-filled safely.
- Pointers: a vault can point to knowledge that lives elsewhere instead of copying it.
- Rules for dividing knowledge into vaults.

## Layout

The repository root is the skill root, in the open [Agent Skills](https://agentskills.io/specification) format.

```
llm-driven/
├── SKILL.md
├── README.md
└── docs/
    └── design.md
```

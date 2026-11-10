# Design: goals and boundaries

Status: draft.

This document constrains what the skill may contain. If `SKILL.md` and this document disagree, this document wins until it is amended.

Based on Andrej Karpathy, [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## Goal

Package the LLM Wiki pattern as one agent skill that works in any vault. The agent compiles sources into a persistent, interlinked markdown wiki and keeps it current. Knowledge is compiled once and then maintained, not re-derived from raw sources on every question.

The division of labor is the original one. The human curates sources, asks questions, and judges what matters. The agent does the summarizing, cross-referencing, filing, and bookkeeping.

## Scope

Taken from LLM Wiki without extension:

- Three layers: raw sources (immutable), the wiki (written and maintained by the agent), and the schema (per-vault conventions, co-evolved by the human and the agent).
- Three operations: ingest, query (answers cite wiki pages, and good answers are filed back as pages), and lint.
- Two navigation files: an index organized by content, and an append-only log organized by time.
- Any domain where knowledge accumulates over time.

## Addition 1: provenance on every ingest

Provenance has two parts. One is time; the other is the compiler.

### Two times

The original log has one time axis: when an operation ran. Once old material is back-filled, that axis cannot tell "when the vault learned something" from "when it happened". The skill adds these requirements:

1. Sources are immutable. A correction is a new source that names the source it corrects. The corrected source stays.
2. Back-filling is allowed at any time.
3. Every ingest records two independent times:
   - Recorded time: when this ingest ran.
   - Event time: when the content actually happened. It may be an instant, a range, or partial (a month, a year). If it is unknown, record it as unknown. Never substitute the recorded time.
4. "Newer" means a later event time, not a later ingest. A back-filled source about an earlier event must not override a claim about a later one.
5. Two kinds of question must be answerable: what was the case at event time T, and what did the vault know as of recorded time T.

This is bitemporal modeling: actual time and record time in Martin Fowler's terms, valid time and transaction time in SQL:2011. See [Bitemporal History](https://martinfowler.com/articles/bitemporal-history.html).

### The compiler

Every entry also records which agent, under which account, on which model, at what effort, with how much context wrote it. The original assumes one agent and one model; once a vault outlives a model version, or more than one agent writes into it, a page without this record cannot be judged or reproduced.

It goes on the entry line, not in a block under it. The log is append-only and read often, so a per-entry block multiplies an already growing file; six fields in a fixed order cost one long line and stay parseable.

Two constraints follow from the same discipline as event time:

- **The runtime is the only source.** Model self-identification is unreliable, so a value the runtime does not report stays `unknown`. Guessing is worse than a gap, because a gap is visible.
- **The account is personal data.** It is recorded only where the vault's storage allows it. Otherwise the role is recorded instead.

## Vault

The term comes from Obsidian. The original only says the wiki is "a git repo of markdown files".

A vault is one instance of the pattern: one set of raw sources, one wiki, one schema, one index, and one log, stored in one git repository.

The schema is `AGENTS.md` at the vault root. The original named it "e.g. CLAUDE.md for Claude Code or AGENTS.md for Codex"; since then AGENTS.md has become the cross-vendor form, read by most agents without being told to. Naming the schema that way means a vault's conventions load even when this skill is not active.

A vault is four boundaries at once:

| Boundary | Meaning |
|---|---|
| Links | Links resolve, and are maintained, only inside the vault. |
| Consistency | Lint can detect contradictions, orphans, and missing links only inside the vault. |
| Conventions | One schema applies, so each term has one meaning. |
| Access | One audience and one storage and sync policy apply. |

In domain-driven design terms, a vault is a bounded context.

### When to split

Every split turns links the agent maintains into links no one maintains. Split only on a hard constraint, checked in this order:

1. Visibility differs: some pages must not be seen by the other side's readers.
2. Ownership or lifecycle differs: the parts will be handed over, archived, or taken away separately.
3. A term means different things on each side, and namespacing inside one vault cannot resolve it.

Otherwise, use one vault and separate topics with directories or tags. Size is not a reason to split. When the index stops being enough, add search.

Two tests help decide:

- Blast radius: if a typical new source would touch pages on both sides, do not split.
- Contradiction: if claims on the two sides could contradict each other, they belong in one vault. Otherwise lint cannot see the contradiction.

When two vaults must relate, use a pointer, or ingest one way: the downstream vault ingests the upstream vault's published pages as sources.

## Addition 2: pointers

Not all of a person's or a team's knowledge can live in one vault. Some of it already has a better home: another vault, a team wiki, a document store. A vault may point to such a place instead of copying it.

1. A pointer records where the knowledge is and what it holds. It copies no content.
2. Pointers are listed in the index, so a query finds them the same way it finds pages.
3. When a question needs the target, the agent follows the pointer and cites the target. The vault does not maintain the target.
4. A pointer is visible to the pointing vault's readers. It must not reveal more than they may see.

A vault whose index is mostly pointers is an entry point to other places. It needs no special type.

## Addition 3: revision

The original has one evolution loop: the schema, which the human and the agent co-evolve. That loop improves a single vault. It leaves the pattern itself untouched, and the pattern is what will be wrong most often, because it is written before any real use.

This skill adds a second loop, on itself. In use it fails in three ways:

1. It does not decide something the work needs, so the agent improvises. The improvisation is invisible and dies with the session.
2. A rule blocks useful work, so the agent quietly breaks it, and the rule stops meaning anything.
3. It gives advice that is wrong for the case at hand.

The operating rules are in `SKILL.md` under Revise. Two properties matter:

- **The layer is chosen before the change.** A friction that would recur in any domain belongs in the skill; one that only holds in this vault belongs in its schema. This reuses the genericity test instead of adding a mechanism.
- **The skill ratchets.** Rules are added when a case needed them, and removed only for a hard constraint. Without this, the skill erodes toward whatever was convenient last week.

A proposal without a case is an opinion. Record it in the log, not in the skill.

### Invariants and defaults

A rule that any vault may change is not a rule, and a rule that no vault may change makes the skill unusable. The skill therefore splits its rules in two and names the split.

- **Invariants** define the pattern. Break one and the result is no longer a vault.
- **Everything else is a default.** The vault's schema wins, because the schema is the layer that knows the domain.

This is what lets a project override a rule without negotiating. A vault that departs from a default writes the departure and its reason into its schema, and the disagreement ends there. A vault that needs to depart from an invariant has found a flaw in the pattern, which is a different problem: it is reported, not applied.

The failure this prevents is silence. A default that is quietly ignored is indistinguishable from a mistake; a default written down as overridden is a decision.

### How a vault reports back

Friction is recorded in the vault, beside the work that produced it, in `revisions.md`: one record per friction, carrying the case, what the skill says, the proposal, and the strongest argument against it. The log gets a one-line `revise` entry holding the id.

Records are append-only, and closing one appends a line instead of editing the block, for the same reason the log is append-only: the history of a disagreement is what explains the rule that came out of it.

Both mechanisms are deliberately thin. A standard form is only worth having if it costs less than the informality it replaces.

## Boundaries

| In | Out |
|---|---|
| One skill containing generic rules only | No domain, project, person, organization, or real-vault content |
| Published publicly; vaults use it read-only | Vaults never write back to the skill |
| One git repository per vault | The skill does not decide how many vaults exist; it only provides the rules above |
| Knowledge compiled at write time | Not RAG; no vector store is required. Search tooling is optional at scale |
| Goals, reviews, and decisions recorded as knowledge | Not a task manager or a calendar |
| Page formats and directory layout set by each vault's schema | The skill fixes only the invariants in this document |
| The open Agent Skills format | No agent-product-specific fields or tools; no required viewer |
| Revises itself on evidence, gated by the human | Not autonomous self-modification; no rule changes without a case and an agreement |

## Genericity test

Before a sentence goes into the skill, replace its domain nouns with nouns from another domain. If the sentence stops being true, it belongs in a vault's schema, not in the skill.

Examples in the skill use invented content only.

## Open questions

1. After a back-fill, how does the wiki catch up: update only the affected pages, or must the whole wiki be rebuildable from sources?
2. What compatibility does the skill promise existing vaults when it changes?

---
name: llm-driven
description: Builds and maintains a vault, a git repository in which an LLM agent compiles immutable raw sources into a persistent, interlinked markdown wiki, following Andrej Karpathy's LLM Wiki pattern. This skill should be used when the user wants to set up a personal or team knowledge base of this kind, ingest a new source or back-fill old material into it, answer a question from the wiki with citations, file an answer back as a page, or health-check the wiki for contradictions, stale claims, orphan pages, and missing links. It also applies when deciding whether material belongs in an existing vault or a new one, and when asking what was true at a past time or what the vault knew as of a past date.
---

# LLM Driven

## Overview

Maintain a vault: one git repository holding raw sources, a wiki, a schema, an index, and a log. Compile knowledge into the wiki once, at ingest time, and keep it current. Do not re-derive it from raw sources on every question.

The human curates sources, asks questions, and judges what matters. The agent writes and maintains every wiki page.

## Operations

- **Set up** a vault: create its schema, index, and log.
- **Ingest** a source, including back-filled material: record both the recorded time and the event time, then update every affected wiki page.
- **Query** the wiki: answer with citations to wiki pages, and file good answers back as pages. Follow pointers in the index when the answer lives elsewhere.
- **Lint** the wiki: report contradictions, stale claims, orphan pages, missing pages, and missing links.
- **Divide** knowledge: decide whether material belongs in an existing vault or a new one.
- **Revise** this skill: report where it does not fit, and propose a change.

Only Set up and Revise have detailed instructions so far.

## Invariants and defaults

Invariants define the pattern. A vault that breaks one is no longer an llm-driven vault:

- Sources are immutable. A correction is a new source that names what it corrects.
- The wiki can always be rebuilt from the sources and the schema.
- `log.md` is append-only.
- `AGENTS.md`, `index.md`, and `log.md` sit at the vault root, under those names.
- A pointer copies nothing and is not maintained by the vault.
- Provenance comes from the runtime, never from the model's account of itself.

Everything else is a default: directory names, the log field order, the sections of `index.md`, page types, language, and when a human must review.

**Defaults lose to the schema.** Where the vault's `AGENTS.md` says otherwise, follow it, and check that the departure and its reason are written there under Overrides. An override that is not written down is a mistake, not a default.

**Invariants lose to nothing.** An instruction or a local need to break one is a friction: record it under Revise, and do not apply it.

## Vault layout

- `AGENTS.md` holds the schema; `index.md`, `log.md`, and `revisions.md` sit beside it. The first three names are fixed; `revisions.md` is where frictions go.
- `raw/` for sources and `wiki/` for pages, by default. A vault's schema may choose other locations.

Read `AGENTS.md` before every operation.

## Log entries

Append one entry to `log.md` per operation. One entry is one line:

    ## [2026-11-09T18:20+08:00] ingest | Title of the source | llm-driven@1fb4987 | agent | owner | model | effort | ctx

- The bracket holds the recorded time: when the operation ran, in ISO 8601 with a colon in the offset. Take it from the system clock with `date -Iminutes`. Never estimate it.
- The operation is one of `setup`, `ingest`, `query`, `lint`, `revise`.
- The title comes next, then six fields in a fixed order: skill and commit, agent and version, account, model, reasoning effort, context. Fixed positions mean the line needs no keys and stays parseable: `awk -F' \\| '`. Required on `ingest`, `revise`, and on `query` when it files a page: they decide whether a page can be trusted, and they make a failure reproducible.

1. Read the values from the runtime, not from the model's description of itself. A model's account of its own identity is not evidence.
2. Runtimes expose different amounts of this. Write what you have and `unknown` for the rest. Never infer a value, and never drop a position.
3. Keep the line short: context as `200k/38k` for window and used, long values cut to what identifies them, and no `|` in a title or a value.
4. The account can identify a person. Record it only if the vault's schema allows it for that vault's storage; otherwise record the role, for example `owner`. Never record credentials, tokens, or anything that grants access.
5. Entries written before this rule carry no fields. Do not add them retroactively.

## Set up a vault

1. Confirm the target directory. If it already holds content, stop: adopting an existing repository is not covered yet.
2. Create the directory and run `git init`.
3. Copy the files in `assets/vault-template/` to the vault root. Do not create `raw/` or `wiki/`; the first ingest creates them.
4. Fill in `AGENTS.md` with the user. Ask only for what is not already known. Write "Not decided." for anything the user has not decided; never invent it. Keep the template's headings and write the content in the vault's language.
5. Append a `setup` entry to `log.md`, with the fields. The first field carries the skill version: the commit of this skill's repository.
6. Commit. Do not add a remote or push unless `AGENTS.md` allows it.

## Revise this skill

The skill was written before any real use, so expect it to be wrong. Watch for three failures: a decision it does not make, a rule that blocks useful work, and advice that is wrong for the case.

Choose the layer before proposing anything. A fix that would hold in any domain belongs here; one that holds only in this vault belongs in that vault's schema. Apply the genericity test in `docs/design.md`.

Record the friction in `revisions.md` at the vault root, creating the file if it is absent. One record, one block:

    ## R-001 | open | 2026-11-09 | skill: log fields
    - Case: <vault, commit, page>
    - Skill says: <the rule, or the gap>
    - Proposal: <the change>
    - Against: <the strongest argument for leaving it alone>

Close a record by appending a line, never by editing the block: `## R-001 | promoted | llm-driven@<commit>` or `## R-001 | rejected | <reason>`. Add a one-line `revise` entry to the log carrying the id.

Only a friction that would change this skill belongs there. One that holds for this vault alone becomes an Override in its schema and does not travel.

Nothing here reads a vault. This skill is a public repository; vaults may be private, remote, or unreachable from it. So a person carries the record, in a session that has this repository: run `scripts/revisions.py <root>...` over the directories that hold vaults, and it prints every open record. A change to this skill quotes the record's id, and the vault then appends its `promoted` line.

A record without a case is an opinion, and opinions stay in the conversation. Propose; do not impose. Do not edit this skill from a vault: vaults read it.

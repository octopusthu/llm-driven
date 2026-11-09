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

## Vault layout

- `AGENTS.md` holds the vault's schema. `index.md` and `log.md` sit beside it. These three names are fixed.
- `raw/` for sources and `wiki/` for pages, by default. A vault's schema may choose other locations.
- Because the schema is named `AGENTS.md`, most agents read it as soon as they work in the repository, so the vault's conventions load even when this skill is not active.

Read `AGENTS.md` before every operation.

## Log entries

Append one entry to `log.md` per operation. One entry is one line:

    ## [2026-11-09T18:20+08:00] ingest | Title of the source | llm-driven@1fb4987 | agent | owner | model | effort | ctx

- The bracket holds the recorded time: when the operation ran, in ISO 8601 with a colon in the offset. Take it from the system clock with `date -Iminutes`. Never estimate it.
- The operation is one of `setup`, `ingest`, `query`, `lint`, `revise`.
- The title comes next, then six fields in a fixed order: skill and commit, agent and version, account, model, reasoning effort, context. Fixed positions mean the line needs no keys and stays parseable: `awk -F' \\| '`.

Record the fields on `ingest`, `revise`, and on `query` when it files a page. Which agent, under which account, on which model, at what effort, with how much context decides whether a page can be trusted, and makes a failure reproducible.

1. Read the values from the runtime, not from the model's description of itself. A model's account of its own identity is not evidence.
2. Runtimes expose different amounts of this. Write what you have and `unknown` for the rest. Never infer a value, and never drop a position.
3. Keep the line short. Write context as `200k/38k` for window and used, and cut long values to what identifies them.
4. A title or value may not contain `|`. Replace it.
5. The account can identify a person. Record it only if the vault's schema allows it for that vault's storage; otherwise record the role, for example `owner`. Never record credentials, tokens, or anything that grants access.
6. Entries written before this rule carry no fields. Do not add them retroactively.

## Set up a vault

1. Confirm the target directory. If it already holds content, stop: adopting an existing repository is not covered yet.
2. Create the directory and run `git init`.
3. Copy the files in `assets/vault-template/` to the vault root. Do not create `raw/` or `wiki/`; the first ingest creates them.
4. Fill in `AGENTS.md` with the user. Ask only for what is not already known. Write "Not decided." for anything the user has not decided; never invent it. Keep the template's headings and write the content in the vault's language.
5. Append a `setup` entry to `log.md`, with the fields. The first field carries the skill version: the commit of this skill's repository.
6. Commit. Do not add a remote or push unless `AGENTS.md` allows it.

## Revise this skill

This skill is expected to keep changing; it was written before any real use. Watch for three failures during any operation: a decision it does not make, a rule that blocks useful work, and advice that is simply wrong.

1. Never invent procedure. When an operation needs a decision this skill does not make, or a rule must be broken to be useful, say so instead of improvising. Name the case: vault, commit, page.
2. Choose the layer before proposing the change. If the fix would hold in any domain, it belongs in this skill. If it only holds here, it belongs in that vault's schema. Apply the genericity test in `docs/design.md`.
3. Propose, do not impose. Give the case, what the skill says now, the change, and the strongest argument for leaving it alone. Do not edit this skill until the human agrees.
4. Challenge the request as well as the rule. If an instruction conflicts with `docs/design.md`, say so before complying.
5. Add a rule only when a case needed it. Remove one only for a hard constraint, the same bar as splitting a vault. Without this the skill erodes toward whatever was convenient last week.
6. Keep the skill version in the compiler line of every entry, so vaults older than a change can be found and re-checked.

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

Only Set up has detailed instructions so far.

## Vault layout

- `SCHEMA.md`, `index.md`, `log.md` at the vault root. These names are fixed.
- `raw/` for sources and `wiki/` for pages, by default. A vault's schema may choose other locations.

Read `SCHEMA.md` before every operation.

## Log entries

Append one entry to `log.md` per operation. Start it with a heading:

    ## [2026-01-15T09:30+01:00] ingest | Title of the source

- The bracket holds the recorded time: when the operation ran, in ISO 8601 with offset. Take it from the system clock, for example `date +%Y-%m-%dT%H:%M%z`. Never estimate it.
- The operation is one of `setup`, `ingest`, `query`, `lint`.

## Set up a vault

1. Confirm the target directory. If it already holds content, stop: adopting an existing repository is not covered yet.
2. Create the directory and run `git init`.
3. Copy the files in `assets/vault-template/` to the vault root. Do not create `raw/` or `wiki/`; the first ingest creates them.
4. Fill in `SCHEMA.md` with the user. Ask only for what is not already known. Write "Not decided." for anything the user has not decided; never invent it. Keep the template's headings and write the content in the vault's language.
5. Append a `setup` entry to `log.md`. Under it, record the skill version as the commit of this skill's repository (`git -C <skill root> rev-parse --short HEAD`), if it is a git repository.
6. Commit. Do not add a remote or push unless `SCHEMA.md` allows it.

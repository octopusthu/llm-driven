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
- **Query** the wiki: answer with citations to wiki pages, and file good answers back as pages.
- **Lint** the wiki: report contradictions, stale claims, orphan pages, missing pages, and missing links.
- **Divide** knowledge: decide whether material belongs in an existing vault or a new one.

Detailed instructions for each operation are not written yet.

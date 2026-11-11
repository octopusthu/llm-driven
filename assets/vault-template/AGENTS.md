# Schema

This file is the vault's schema. It is named `AGENTS.md` so that agents working in this repository read it automatically.

Conventions for this vault. The agent reads this file before every operation. The human and the agent revise it together.

## Status

Status: empty

`empty` or `ingest-ready`. Set Up writes `empty`. Only the human raises it, by answering `Pages` and `Sources`: the vault is `ingest-ready` when `Pages` names its page types and `Sources` names at least one source, with that source's key and the field carrying its event time.

## Purpose

One sentence: what this vault is for.

## Scope

- In:
- Out:

## Readers and storage

- Readers: who may read this vault.
- Storage: where the repository lives, and where it may be pushed. If no remote is listed, do not push.

## Relations

Vaults or other stores this vault points to or ingests from. "None" if there are none.

## Pages

Page types, one line each: what the type holds, and the frontmatter every page of it carries.

Two fields are not optional on any page: `sources`, pointing back to what the claim came from, and `event`, the range the page describes. Without them nothing can be traced or dated.

None yet.

## Sources

One entry per source: how it is fetched, its key, the field that carries its event time, and where the raw copy lands. A source without a key will be ingested twice; a source without an event-time field will be dated by when it was fetched.

None yet.

## Raw layout

- `raw/<source>/<event YYYY-MM>/<fetch YYYY-MM-DDTHHMM>-<slug>.<ext>`, one file per fetch.
- The directory follows the event time, so a month's material sits under that month however late it arrived.
- The filename carries the fetch time, which is what ties the file to the log entry that created it.
- A fetch spanning several months splits, one file per month.
- Written once, never edited. A correction is a new file that names the one it corrects.

## Naming

- Page files and slugs in kebab-case. Titles may use the vault's language.

## Overrides

Where this vault departs from a default in the skill. One line each: what the skill says, what this vault does instead, why.

None.

## Conventions

Anything else, added as it emerges.

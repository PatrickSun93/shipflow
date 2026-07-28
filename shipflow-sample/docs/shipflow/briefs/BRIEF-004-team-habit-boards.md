---
id: BRIEF-004
slug: team-habit-boards
status: specced
created: 2026-03-20
updated: 2026-04-02
---

# Team habit boards

## Problem

Small groups training together have no shared view of who's on track.

## Who

Accountability groups of 2-8 (gym buddies, a book club).

## Why now

6+ support requests for "share my streak" since v0.2.

## Constraints

- Reuse existing auth (Lucia) — no per-board tokens.
- Membership capped at 8; invite-only.

## Non-goals

- Cross-board leaderboards or public boards.

## Success

One board used (2+ logging) in week one, no access tickets.

## Risks

- Only streak + last-logged date visible, not full history.

## Open questions

- Silent leave vs. notify? Ship silent for v1.

## Unresolved

_None._

---
name: sf-gate-2
description: Deprecated alias for /sf-check-plan. Renamed in v0.2.1 for readability. This alias will be removed in v0.3.0.
---

# sf-gate-2 (deprecated)

This skill has been renamed to `/sf-check-plan`. The new name makes the
workflow self-explanatory (you review the **plan** — the sliced stories).

## What to do

Invoke the new skill via the Skill tool: `sf-check-plan` with whatever
arguments the user passed to `/sf-gate-2`. Then tell the user in your
reply:

> Note: `/sf-gate-2` has been renamed to `/sf-check-plan`. The old name
> still works through v0.2.x and will be removed in v0.3.0.

That's it — no other logic here. The real behavior lives in
`sf-check-plan/SKILL.md`.

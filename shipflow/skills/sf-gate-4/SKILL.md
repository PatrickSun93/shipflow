---
name: sf-gate-4
description: Deprecated alias for /sf-check-ship. Renamed in v0.2.1 for readability. This alias will be removed in v0.3.0.
---

# sf-gate-4 (deprecated)

This skill has been renamed to `/sf-check-ship`. The new name makes the
workflow self-explanatory (you review before **ship** — the final
pre-release structural check).

## What to do

Invoke the new skill via the Skill tool: `sf-check-ship` with whatever
arguments the user passed to `/sf-gate-4`. Then tell the user in your
reply:

> Note: `/sf-gate-4` has been renamed to `/sf-check-ship`. The old name
> still works through v0.2.x and will be removed in v0.3.0.

That's it — no other logic here. The real behavior lives in
`sf-check-ship/SKILL.md`.

---
name: sf-gate-1
description: Deprecated alias for /sf-check-brief. Renamed in v0.2.1 for readability. This alias will be removed in v0.3.0.
---

# sf-gate-1 (deprecated)

This skill has been renamed to `/sf-check-brief`. The new name makes the
workflow self-explanatory (you review the **brief** — no mental overhead
tracking which numbered gate this is).

## What to do

Invoke the new skill via the Skill tool: `sf-check-brief` with whatever
arguments the user passed to `/sf-gate-1`. Then tell the user in your
reply:

> Note: `/sf-gate-1` has been renamed to `/sf-check-brief`. The old name
> still works through v0.2.x and will be removed in v0.3.0.

That's it — no other logic here. The real behavior lives in
`sf-check-brief/SKILL.md`.

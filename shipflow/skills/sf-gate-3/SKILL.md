---
name: sf-gate-3
description: Deprecated alias for /sf-check-build. Renamed in v0.2.1 for readability. This alias will be removed in v0.3.0.
---

# sf-gate-3 (deprecated)

This skill has been renamed to `/sf-check-build`. The new name makes the
workflow self-explanatory (you review the **build** — acceptance,
tests, code review).

## What to do

Invoke the new skill via the Skill tool: `sf-check-build` with whatever
arguments the user passed to `/sf-gate-3`. Then tell the user in your
reply:

> Note: `/sf-gate-3` has been renamed to `/sf-check-build`. The old name
> still works through v0.2.x and will be removed in v0.3.0.

That's it — no other logic here. The real behavior lives in
`sf-check-build/SKILL.md`.

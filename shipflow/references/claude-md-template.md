<!-- SHIPFLOW:BEGIN -->
# {{project_name}}

_Solo product development orchestrated by ShipFlow._

## Where to look

- `docs/shipflow/index.md` — auto-regenerated index of briefs, stories, ADRs, releases
- `docs/shipflow/stack.md` — tech stack, conventions, paths
- `shipflow.config.json` — gate modes and workflow tuning

## Workflow

ShipFlow runs a 5-phase flow: **Discover → Spec → Build → Verify → Ship**.
Four advisory gates sit between phases (configurable to blocking in `shipflow.config.json`).

## Read narrowly

When working on a phase task, read only:
- The relevant brief / story / ADR
- `docs/shipflow/stack.md` for project conventions
- `docs/shipflow/index.md` for cross-links

Do **not** read `docs/shipflow/archive/` unless explicitly asked.

## Code style

Clear and simple over clever abstraction. This applies to production code,
agent prompts, and hook scripts alike.
<!-- SHIPFLOW:END -->

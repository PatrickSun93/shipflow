<!-- SHIPFLOW:BEGIN -->
# Loopline

_Solo product development orchestrated by ShipFlow._

## Where to look

- `docs/shipflow/index.md` — index of briefs, stories, ADRs, releases (regen via `/sf-regen-index`)
- `docs/shipflow/stack.md` — tech stack, conventions, paths, logging conventions
- `shipflow.config.json` — gate modes, cofounder review mode, archive-on-ship, regen cadence

## Workflow

ShipFlow runs a 5-phase flow: **Discover → Spec → Build → Verify → Ship**.
Four advisory gates sit between phases (configurable to blocking in
`shipflow.config.json`).

Lost on what's next? Run **`/sf-next`** — it reads repo state and runs
(or recommends) the appropriate next step.

## Read narrowly

When working on a phase task, read only:
- The relevant brief / story / ADR
- `docs/shipflow/stack.md` for project conventions
- `docs/shipflow/index.md` for cross-links

Do **not** read `docs/shipflow/archive/` unless explicitly asked.

## Code style

Clear and simple over clever abstraction. KISS/YAGNI, trust internal
boundaries (no defensive try/catch; log at boundaries), Rule of Three,
no half-finished code, match neighbor file style.
<!-- SHIPFLOW:END -->

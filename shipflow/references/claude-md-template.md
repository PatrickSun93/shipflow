<!-- SHIPFLOW:BEGIN -->
# {{project_name}}

_Solo product development orchestrated by ShipFlow._

## Where to look

- `docs/shipflow/index.md` — index of briefs, stories, ADRs, releases (regen via `/sf-regen-index`)
- `docs/shipflow/stack.md` — tech stack, conventions, paths, logging conventions
- `shipflow.config.json` — gate modes, cofounder review mode, archive-on-ship, regen cadence

## Workflow

ShipFlow runs a 5-phase flow: **Discover → Spec → Build → Verify → Ship**.
Four advisory gates sit between phases (configurable to blocking in
`shipflow.config.json`). Cross-cutting reviewers (security, DB, cofounder)
are manual-trigger; their `blocking` verdicts hard-stop `/sf-ship` unless
explicitly overridden.

Lost on what's next? Run **`/sf-next`** — it reads repo state and runs
(or recommends) the appropriate next step.

## Read narrowly

When working on a phase task, read only:
- The relevant brief / story / ADR
- `docs/shipflow/stack.md` for project conventions
- `docs/shipflow/index.md` for cross-links

Do **not** read `docs/shipflow/archive/` unless explicitly asked.

## Code style

Clear and simple over clever abstraction. The build-lead agent enforces
five rules on the code it produces: KISS/YAGNI, trust internal boundaries
(no defensive try/catch; do log at boundaries with structured key=value),
Rule of Three, no half-finished code (no TODOs/stubs), match neighbor
file style.

## Session resume

If your Claude Code session gets paused (usage cap), don't worry about
losing context: the `UserPromptSubmit` hook logs every turn to
`docs/shipflow/sessions/log-<date>.md`, and `/sf-checkpoint` captures
rich session intent on demand. Next session's `SessionStart` hook
surfaces both automatically.
<!-- SHIPFLOW:END -->

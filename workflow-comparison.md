# Workflow comparison — prior art

> Side-by-side of the Claude Code / agentic dev workflows that inspired
> ShipFlow. Used during design to answer "did anyone solve this already?"
> and "which ideas are worth borrowing?"
>
> **Status:** skeleton. The original comparison didn't transfer from the
> Cowork session. This file lays out the structure; the row content for each
> project needs to be filled in from firsthand reading rather than guessed
> at — these are other people's projects and I don't want to misrepresent them.

---

## Projects compared

| # | Project | Link | One-line summary |
|---|---------|------|------------------|
| 1 | Claude-Code-Game-Studios | _TODO: add link_ | _TODO: 1-line summary_ |
| 2 | BMAD | _TODO: add link_ | _TODO: 1-line summary_ |
| 3 | Agent OS | _TODO: add link_ | _TODO: 1-line summary_ |
| 4 | SuperClaude | _TODO: add link_ | _TODO: 1-line summary_ |
| 5 | claude-sub-agent | _TODO: add link_ | _TODO: 1-line summary_ |
| 6 | **ShipFlow** (this repo) | — | Solo-dev 5-phase workflow with 4 advisory gates. |

---

## Side-by-side

Fill each column from the project's own docs. Err toward concrete ("5 agents
named X/Y/Z") over abstract ("has agents").

| Dimension | Game Studios | BMAD | Agent OS | SuperClaude | claude-sub-agent | **ShipFlow** |
|-----------|--------------|------|----------|-------------|------------------|--------------|
| Target user | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | Solo developer |
| Packaging | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | Claude Code plugin |
| Phases | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | 5 (Discover → Spec → Build → Verify → Ship) |
| Agent count | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | 6 in Discover (plan: ~12 total) |
| Parallelism during discovery | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | 3 personas in parallel, 2 rounds max |
| Gates / reviews | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | 4 advisory gates, configurable to blocking |
| Story/brief storage | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | In-repo markdown, frontmatter-linked |
| Memory model | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | 3-layer (Hot / Warm / Cold) with archiving |
| Uses marketplace skills | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | Yes — Spec suggests installs |
| Opinionated on stack | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | No — `stack.md` is user-defined |
| External integrations (Linear/Jira/etc.) | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | None in v1 |

---

## What ShipFlow borrowed (and from where)

Each bullet should cite the project that contributed the idea. Placeholders
below — replace with real attributions.

- **Phase structure (Discover → Build → Ship etc.)** — common across _TODO:
  which projects_.
- **Per-persona discovery** — _TODO: which project inspired this, if any._
- **Advisory vs. blocking gates** — _TODO._
- **In-repo markdown as source of truth** — _TODO._
- **Tiered agents (Tier-1 reviewers, Tier-2 leads, Tier-3 specialists)** —
  _TODO._

## Where ShipFlow differs

Explicit divergences from prior art:

- **Solo-dev framing** — most prior art assumes small teams.
- **Advisory by default** — most prior art defaults to blocking gates.
- **Per-persona dialogue files** — ShipFlow writes `dialogue-tech.md`,
  `dialogue-ux.md`, `dialogue-business.md` separately to avoid write
  collisions during parallel persona runs. _TODO: confirm whether any prior
  art does this._
- **Dual-mode personas** — same agent prompt handles Discover-mode
  questioning and Synthesis-mode authoring. Fewer files, same behavior.
  _TODO: confirm whether this is novel or borrowed._
- **Simplicity constraints** — ≤80 lines per agent, ≤40 lines per hook
  script. _TODO: note if any prior art has similar caps._

---

## How to finish this doc

1. Read each project's docs / README / sample config.
2. Fill in the row for that project across every dimension in the table.
3. When all rows are concrete, rewrite the "What ShipFlow borrowed" and
   "Where ShipFlow differs" sections with real citations instead of _TODO_.
4. If a project turns out to be less similar than first assumed, drop it.
5. Commit with message `docs: fill in workflow-comparison rows`.

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
| 6 | MemPalace | https://github.com/MemPalace/mempalace | Local-first AI conversation memory with verbatim storage, Wings/Rooms/Drawers taxonomy, ChromaDB + BM25 semantic search, and 19 MCP tools. |
| 7 | **ShipFlow** (this repo) | — | Solo-dev 5-phase workflow with 4 advisory gates. |

---

## Side-by-side

Fill each column from the project's own docs. Err toward concrete ("5 agents
named X/Y/Z") over abstract ("has agents").

> **Note on MemPalace:** it's a memory system, not a workflow framework, so
> several workflow dimensions below are `n/a` for that column. Included here
> because we borrowed concepts from it (see "What ShipFlow borrowed" below).

| Dimension | Game Studios | BMAD | Agent OS | SuperClaude | claude-sub-agent | MemPalace | **ShipFlow** |
|-----------|--------------|------|----------|-------------|------------------|-----------|--------------|
| Target user | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | Any AI-agent user | Solo developer |
| Packaging | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | Python pkg + Claude Code plugin + MCP | Claude Code plugin |
| Phases | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | n/a | 5 (Discover → Spec → Build → Verify → Ship) |
| Agent count | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | n/a | 6 in Discover (plan: ~12 total) |
| Parallelism during discovery | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | n/a | 3 personas in parallel, 2 rounds max |
| Gates / reviews | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | n/a | 4 advisory gates, configurable to blocking |
| Story/brief storage | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | n/a | In-repo markdown, frontmatter-linked |
| Memory model | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | Verbatim store, Wings/Rooms/Drawers + KG + semantic search | 3-layer (Hot / Warm / Cold) with archiving |
| Uses marketplace skills | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | n/a | Yes — Spec suggests installs |
| Opinionated on stack | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | Python + ChromaDB (pluggable backend interface) | No — `stack.md` is user-defined |
| External integrations (Linear/Jira/etc.) | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ | None (local-first by design) | None in v1 |

---

## What ShipFlow borrowed (and from where)

- **Per-agent diary** (`docs/shipflow/diaries/<agent>.md`) — borrowed from
  MemPalace's `diary_write` / `diary_read` MCP tools. Reimplemented as
  markdown files so ShipFlow has no runtime dependency on MemPalace.
- **Stop + PreCompact hooks** for session continuity — borrowed from
  MemPalace's hook design. Reimplemented as minimal markdown markers
  (branch, last commit, dirty files) rather than verbatim transcript
  storage — ShipFlow's source of truth stays in committed markdown.
- **Phase structure (Discover → Build → Ship etc.)** — common across
  BMAD, Agent OS, SuperClaude, and others; the specific 5-phase cut is
  ShipFlow's own.
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
- **Simplicity constraints** — agents 800–1500 tokens, hooks ≤500 tokens
  (migrated from line-based caps in v0.2.5). _TODO: note if any prior art has similar caps._

---

## How to finish this doc

1. Read each project's docs / README / sample config.
2. Fill in the row for that project across every dimension in the table.
3. When all rows are concrete, rewrite the "What ShipFlow borrowed" and
   "Where ShipFlow differs" sections with real citations instead of _TODO_.
4. If a project turns out to be less similar than first assumed, drop it.
5. Commit with message `docs: fill in workflow-comparison rows`.

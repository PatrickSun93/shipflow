# Workflow comparison — prior art

Side-by-side of the Claude Code / agentic dev workflows that inspired
ShipFlow. Used during design to answer "did anyone solve this already?"
and "which ideas are worth borrowing?"

This doc is concrete (linked rows, actual numbers from each project's
docs) rather than vibes-based. When something says `_See docs_`, it
means the dimension exists but the project's own docs are the better
source.

---

## Projects compared

| # | Project | Link | One-line summary |
|---|---------|------|------------------|
| 1 | Claude-Code-Game-Studios | [Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) | Turn Claude Code into a full game dev studio: 49 hierarchical agents (directors / leads / specialists), 72 workflow skills, opinionated Godot/Unity/Unreal stack. |
| 2 | BMAD | [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | "Breakthrough Method for Agile AI Driven Development." 12+ agile-role agents (Analyst / PM / Architect / SM / PO / Dev / QA), "Party Mode" for multi-persona sessions, IDE-agnostic. |
| 3 | Agent OS | [buildermethods/agent-os](https://github.com/buildermethods/agent-os) | Codebase-standards injector + spec-shaping system. Lightweight, focuses on extracting tribal knowledge into standards files; sequential spec-driven. |
| 4 | SuperClaude | [SuperClaude-Org/SuperClaude_Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework) | "Behavioral configuration" framework on top of Claude Code. 30 commands (`/sc:*`), 14 cognitive-persona agents addressable via `@agent-X`. |
| 5 | claude-sub-agent | [zhsama/claude-sub-agent](https://github.com/zhsama/claude-sub-agent) | Spec-driven pipeline using Claude Code Sub-Agents. 8 core agents (spec-analyst / -architect / -developer / -orchestrator / -planner / -reviewer / -tester / -validator) + specialists, configurable quality threshold. |
| 6 | MemPalace | [MemPalace/mempalace](https://github.com/MemPalace/mempalace) | Local-first AI conversation memory. Verbatim transcript store, Wings/Rooms/Drawers taxonomy, ChromaDB + BM25 semantic search, 19 MCP tools. **Memory system, not a workflow framework** — included because ShipFlow borrowed concepts. |
| 7 | **ShipFlow** (this repo) | [PatrickSun93/shipflow](https://github.com/PatrickSun93/shipflow) | Solo-dev 5-phase workflow (Discover → Spec → Build → Verify → Ship), 4 advisory gates, 22 agents with role-embodied Identity & POV + named methodology toolkits. |

---

## Side-by-side

> Game Studios = `Game St.`, claude-sub-agent = `c-sub-agent`. MemPalace
> rows are mostly `n/a` (memory system, not a workflow).

| Dimension | Game St. | BMAD | Agent OS | SuperClaude | c-sub-agent | MemPalace | **ShipFlow** |
|---|---|---|---|---|---|---|---|
| Target user | Game devs (solo/team) | Any AI-IDE user | Small teams + Claude Code/Cursor | Claude Code users | Claude Code users | Any AI-agent user | Solo developer |
| Packaging | Claude Code plugin | `npx bmad-method` installer + IDE configs | Lightweight standards/spec files | Behavioral config layer | Sub-agent prompts | Python pkg + plugin + MCP | Claude Code plugin |
| Phases / stages | start → design-system → epics → stories → dev-story → story-done → release | Ideation → Planning → Architecture → Implementation | Discover Standards → Deploy → Shape Specs → Product Docs | 30 `/sc:*` commands (no fixed flow) | Spec lifecycle (analyst → architect → developer → tester → validator) | n/a | 5 (Discover → Spec → Build → Verify → Ship) |
| Agent count | 49 | 12+ | Few; new project-manager v2.1 | 14 personas | 8 core + N specialists | n/a | 22 (8 with Identity & POV, 6 domain experts, 8 phase + cross-cutting) |
| Hierarchy | **Yes** — directors / leads / specialists | Roles, mostly flat | Mostly flat | Flat personas | Orchestrator + workers | n/a | Tier-1 / Tier-2 / lens (informal) |
| Parallelism in Discovery | Team-orchestration commands (`/team-*`) | "Party Mode" — multi-persona in one session | Sequential | `@agent-*` on demand, parallel possible | spec-orchestrator coordinates | n/a | 3 base personas + 1 optional domain expert in parallel, 2 rounds max |
| Gates / reviews | Validation hooks on commits/pushes/asset changes | Agile-shaped reviews per phase | Spec-quality questions | "Quality gates and validation" | Configurable quality threshold (e.g. 95) | n/a | 4 advisory gates + 3 cross-cutting reviewers (security/db/cofounder); blocking when configured |
| Story/brief storage | In-repo (epic/story files) | Generated artifacts (PRD / architecture / stories) | Standards + spec files in repo | Whatever the command produces | Spec files in repo | n/a | In-repo markdown, frontmatter-linked, status-machine driven |
| Memory model | Repo-level | Repo-level | Standards files persistent | Session + repo | Repo-level | **Verbatim store, Wings/Rooms/Drawers + KG + semantic search** | 3-layer (Hot CLAUDE.md / Warm `docs/shipflow/` / Cold archive) + per-turn session log + checkpoints |
| Marketplace skill reuse | Within plugin | No | No | No | No | n/a | Yes (e.g. suggests installs in Spec phase) |
| Opinionated on stack | Yes (Godot/Unity/Unreal) | No | No | No | No | Python + ChromaDB (pluggable) | No — `stack.md` user-defined; project-archaeologist auto-extracts on `/sf-init --existing` |
| External integrations | None | None | None | None | None | None | None in v1 (in-repo only) |
| Size discipline (caps) | _Not specified_ | _Not specified_ | _Not specified_ | _Not specified_ | _Not specified_ | _Not specified_ | Agents ≤2000 tokens (typical 800–1500), hooks ≤500 |
| Web research in Discovery | _Not specified_ | _Not specified_ | _Not specified_ | `/sc:research` command exists | _Not specified_ | n/a | Built-in: every Discovery persona runs WebSearch before asking judgment questions |

---

## What ShipFlow borrowed (and from where)

- **Per-agent diary** (`docs/shipflow/diaries/<agent>.md`) — borrowed
  from MemPalace's `diary_write` / `diary_read` MCP tools. Reimplemented
  as plain markdown so ShipFlow has zero runtime dependency on
  MemPalace.
- **Stop + PreCompact hooks** for session continuity — borrowed from
  MemPalace's hook design. Reimplemented as minimal markdown markers
  (branch, last commit, dirty files) rather than verbatim transcript
  storage. ShipFlow's source of truth stays in committed markdown.
- **UserPromptSubmit hook for pause-resistant logging** — extends the
  MemPalace hook pattern; survives the case where Claude Code sessions
  hit usage caps and never fire `Stop`.
- **Tiered agent hierarchy** (Tier-1 reviewers / Tier-2 leads /
  specialists) — pattern visible in **Game Studios** (director / lead /
  specialist) and to a lesser degree in **BMAD** (Analyst / PM /
  Architect / Dev) and **claude-sub-agent** (orchestrator + workers).
  ShipFlow's split is more informal and biased toward solo-dev
  ergonomics.
- **Phase structure** (Discover → ... → Ship) — common across BMAD,
  Agent OS, SuperClaude, claude-sub-agent. ShipFlow's specific 5-phase
  cut is its own; the closest match is BMAD's 4-phase agile shape.
- **Configurable quality threshold for gates** — closest analogue is
  **claude-sub-agent**'s threshold (e.g. 95). ShipFlow's `gate_modes`
  config (`advisory | block` per gate) and `cofounder_review_mode`
  flag are similar in spirit, though ShipFlow defaults to `advisory`
  rather than a numeric bar.
- **Spec-driven artifacts** (markdown briefs / stories / ADRs in repo)
  — common across BMAD, Agent OS, claude-sub-agent. ShipFlow's
  contribution is the **frontmatter-linked status machine** plus
  `/sf-lint` to verify integrity.
- **Person-based perspective skills** (Identity & POV pattern) —
  inspired by [nuwa-skill](https://github.com/alchaincyf/nuwa-skill)'s
  Steve Jobs / Elon Musk perspective skills. ShipFlow does **not**
  role-play specific people; it borrows the *shape* (Identity / POV /
  named frameworks) for generic role embodiment in cofounder-expert,
  tech-lead, etc.
- **Anthropic prompt-engineering best practices** (XML tags like
  `<investigate_before_answering>`, `<default_to_action>`,
  `<coverage_first>`) — applied directly in build-lead, security-
  reviewer, db-reviewer, code-reviewer, project-archaeologist,
  cofounder-expert.

---

## Where ShipFlow differs

Explicit divergences from prior art — what makes ShipFlow ShipFlow,
not just-another-fork:

- **Solo-dev framing.** Most prior art assumes small teams (Game
  Studios is explicit "studio hierarchy"; BMAD models an agile team).
  ShipFlow's 22 agents represent the **roles a solo dev would
  otherwise have to play themselves**, and ergonomics target that
  audience (e.g. fast paths `/sf-tiny` / `/sf-quick` / `/sf-hotfix`).
- **Advisory gates by default, blocking when configured.** Most spec-
  driven prior art (claude-sub-agent threshold, BMAD agile gates)
  defaults to strictness. ShipFlow's `advisory` default exists because
  solo devs need flexibility; gate flips to blocking only when the
  user opts in.
- **Per-persona dialogue files.** ShipFlow writes `dialogue-tech.md`,
  `dialogue-ux.md`, `dialogue-business.md`, `dialogue-<domain>.md`
  separately to avoid write collisions during parallel persona runs.
  None of the prior art surveyed does this — they tend to either
  serialize personas or share one workspace.
- **Dual-mode personas.** Same agent prompt handles both Discover-
  mode questioning and Synthesis-mode authoring — fewer files, mode
  selected by skill invocation. Not seen in prior art surveyed.
- **Domain-aware persona spawning.** Discovery moderator classifies
  the seed and conditionally spawns one of 6 domain experts
  (education / fintech / healthcare / ecommerce / devtools / social)
  alongside the 3 base personas. **BMAD's "Party Mode"** is the
  closest analogue but is user-driven, not auto-classified.
- **Domain overlay references** (e.g. `cofounder-education.md` layered
  on top of generic cofounder-expert frameworks). Modular extension
  pattern; not seen in prior art.
- **Built-in research-first protocol.** Every Discovery persona uses
  WebSearch before asking judgment questions, with results structured
  as `## Research findings` (URL-cited) vs. `## Questions for you`.
  Not standard in prior art surveyed.
- **Token-based size caps** (agents 800–1500 typical, ≤2000 hard
  ceiling, hooks ≤500). Most prior art doesn't publish caps.
- **Project archaeologist on init.** `/sf-init --existing` spawns a
  dedicated agent that scans the codebase and writes a rich,
  evidence-cited `stack.md`, so downstream agents inherit real context
  instead of re-asking the user about basics. Most spec-driven systems
  put this burden on the user.
- **Pause-resistant session resume.** UserPromptSubmit hook + manual
  `/sf-checkpoint` skill survive Claude Code usage caps. Not seen in
  prior art surveyed (MemPalace's verbatim store solves a similar
  problem differently — at the conversation-memory layer, not the
  workflow layer).
- **In-house code review, security review, DB review** — ShipFlow
  ships its own reviewer agents (code-reviewer / security-reviewer /
  db-reviewer) with named methodologies (OWASP / CAP / Rule of Three /
  Three-Person Test / etc.) rather than depending on external
  marketplace skills.

---

## Sources

- [Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios)
- [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) and
  [BMAD docs](https://docs.bmad-method.org/)
- [Agent OS](https://github.com/buildermethods/agent-os) and
  [Agent OS workflow](https://buildermethods.com/agent-os/workflow)
- [SuperClaude_Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework)
- [claude-sub-agent](https://github.com/zhsama/claude-sub-agent)
- [MemPalace](https://github.com/MemPalace/mempalace)
- [nuwa-skill](https://github.com/alchaincyf/nuwa-skill) (cited in
  ShipFlow's cofounder-expert design)
- [Anthropic prompt engineering best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)

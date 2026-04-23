Here's the full handoff contents displayed inline:

---

# ShipFlow Plugin — Handoff to Claude Code

**Date:** 2026-04-15
**From:** Cowork session (Patrick + Claude)
**For:** Continued development in Claude Code
**Workspace:** this directory (`claude-code-project/`)

---

## TL;DR

ShipFlow is a Claude Code plugin that gives solo developers a multi-agent product-dev workflow: **Discover → Spec → Build → Verify → Ship**, with four advisory gates between phases. Stories, ADRs, briefs, and releases all live in-repo as markdown. Inspired by Claude-Code-Game-Studios and related patterns (BMAD, Agent OS, SuperClaude), but re-framed for solo software/product dev.

**Status:**
- Plugin scaffold exists at `claude-code-project/shipflow/`.
- **Discover phase: fully scaffolded, validated, ready to try.**
- Spec, Build, Verify, Ship: designed, **not yet scaffolded**.
- Sample fixture + measurement script at `claude-code-project/shipflow-sample/` (proves 3-layer memory model works).

**Where to pick up:** Scaffold the **Spec phase** next (see "Next steps" below).

---

## Locked design decisions

Do not relitigate these unless Patrick explicitly asks — they were debated and chosen.

| Decision | Chosen | Why |
|---|---|---|
| Name | **ShipFlow** | — |
| Packaging | Claude Code plugin (`.claude-plugin/plugin.json`, skills/, agents/, hooks/) | Installable, versionable, keeps Patrick's repo clean |
| Target user | Solo developer (Claude acts as pseudo-team) | Small-team extensibility later, not v1 |
| Phases | 5 (Discover → Spec → Build → Verify → Ship) | Matches the mental model from prior art |
| Gates | 4, **advisory by default** (warnings, not blocks) | Solo-friendly; user flips to blocking in `shipflow.config.json` when ready |
| Perspectives in Discover | 3 parallel personas — Tech / UX / Business — via `discovery-moderator` | Catches blind spots a single lens misses |
| Dialogue file layout | **Per-persona files** (`dialogue-tech.md`, `dialogue-ux.md`, `dialogue-business.md`) | Zero write-collision risk; failure isolation; naming matches `slice-<persona>.md`. Moderator stitches a human-readable `dialogue.md` at convergence. |
| Gate review files | Kept as breadcrumbs in `docs/shipflow/discovery/<slug>/gate-N-review-<role>.md` | Patrick wants to preserve per-agent originals; they ride along through ship/archive |
| Story tracking | In-repo markdown only (no Linear/Jira/GitHub Projects integration in v1) | Keeps it self-contained |
| Stack skills | Reference existing marketplace skills (Next.js, TypeScript, etc.), don't vendor | Avoids duplicating work; plugin can suggest installs in Spec phase |
| Memory layering | 3 layers: Hot (`CLAUDE.md`), Warm (`docs/shipflow/`), Cold (`archive/`) | Verified via measurement script — all phases within budget |
| Index regen cadence | Every 5 completed stories (gate-3 passes) | Avoids per-write churn |
| Ship action | Archive shipped briefs/stories/releases to `docs/shipflow/archive/` | Keeps warm-layer small |
| Code style | **Clear and simple over clever abstraction** | Explicit Patrick preference — applies to agent prompts, hooks, skills |
| Agent prompt size | **800–1500 tokens** (target range; 1500 is the hard ceiling). Migrated from line-based cap in v0.2.5 — lines were a human proxy; tokens are what actually matter for LLM context budget. | Simplicity constraint |
| Hook script size | **≤500 tokens** each (bash hooks don't go through the model but the cap is the same idea: keep components grokable). | Simplicity constraint |
| `sf-init` CLAUDE.md handling | Smart default: overwrite-if-empty-or-placeholder, append-if-real-content. Flags: `--overwrite` (with auto-backup to `CLAUDE.md.pre-shipflow`), `--append` (force) | Avoids destroying existing context; gives escape hatches |
| Challenger subagent | Runs at the **tail of Discover (`sf-brief`) and Spec (`sf-spec`, when scaffolded)**. Persona is **smart-but-skeptical** (not "plays dumb"). Loops have a **soft cap** — the challenger self-judges when pressing further would be theater. Reads brief + seed + answers and resolves challenges internally (no spawn of product-lead); unresolved items escalate to `open-questions.md` with 2–4 options + recommendation + optional checklist, **user decides** | Stress-tests the brief for load-bearing claims without infinite loops. User is the terminator, not the challenger. Single-agent self-reasoning keeps token budget flat. |

---

## What's built (file tree)

```
claude-code-project/
├── HANDOFF.md                         ← this file
├── workflow-comparison.md             side-by-side of prior art (Game Studios, BMAD, Agent OS, SuperClaude, claude-sub-agent)
├── shipflow-plan.md                   detailed per-phase design with challenges
├── shipflow-memory-measurement.md     measurement report: all phases PASS budget
│
├── shipflow-sample/                   fixture simulating a realistic ShipFlow repo (~26 files)
│   ├── CLAUDE.md                      (1.05KB, hot layer)
│   ├── shipflow.config.json
│   ├── docs/shipflow/
│   │   ├── index.md
│   │   ├── stack.md
│   │   ├── briefs/                    2 briefs
│   │   ├── stories/                   6 stories (STORY-0010…0015)
│   │   ├── decisions/                 6 ADRs (App Router, Prisma, Lucia, Server Actions, Neon, Cron)
│   │   ├── releases/                  2 releases
│   │   ├── retros/                    1 retro
│   │   └── archive/stories/           6 archived stories (v0.1, v0.2)
│   └── measure.py                     Python measurement script
│
└── shipflow/                          ← THE PLUGIN — this is what ships
    ├── .claude-plugin/
    │   └── plugin.json                manifest (name, version, description, keywords)
    ├── README.md                      plugin-level docs
    ├── agents/
    │   ├── tech-lead.md               Tier 1 (Opus) — architecture, ADRs, cross-cutting tech calls
    │   ├── product-lead.md            Tier 1 (Opus) — scope discipline, 3 questions every time
    │   ├── discovery-moderator.md     Tier 2 (Sonnet) — orchestrates the 3 personas
    │   ├── discovery-tech-persona.md  Tech questions lens
    │   ├── discovery-ux-persona.md    UX questions lens
    │   ├── discovery-business-persona.md   Business questions lens
    │   └── challenger.md              Tier 2 (Sonnet) — smart-but-skeptical stress-tester, runs at tail of Discover/Spec
    ├── skills/
    │   ├── sf-init/SKILL.md           initialize ShipFlow in a repo (one-time)
    │   ├── sf-discover/SKILL.md       run the Discover dialogue
    │   ├── sf-brief/SKILL.md          synthesize brief from user's answers
    │   └── sf-gate-1/SKILL.md         advisory review before Spec
    ├── hooks/
    │   ├── hooks.json                 SessionStart → session-start-context.sh
    │   └── scripts/
    │       └── session-start-context.sh   emits CLAUDE.md + index.md + gate modes at session start
    └── references/
        ├── claude-md-template.md      template used by sf-init
        ├── brief-template.md          8-section brief (Problem, Who, Why now, Constraints, Non-goals, Success, Risks, Open Qs)
        ├── adr-template.md
        └── story-template.md          frontmatter: id, brief, status, size, depends_on
```

**Plugin size:** ~47KB across 18 files. Validated (frontmatter present on all agents/skills, kebab-case plugin name, no stale shared-dialogue references, hook script executable).

---

## Discover phase — how it flows

```
User: /sf-init                        → one-time repo setup (docs/shipflow/, CLAUDE.md, config)
User: /sf-discover "<idea>"           → slugs idea, seeds discovery/<slug>/, spawns discovery-moderator
  Moderator
    → Round 1: spawn 3 personas in parallel
    → each writes dialogue-<persona>.md (own file, own H1)
    → Round 2 (cross-talk): each reads the other 2, appends "## Round 2"
    → Converge: dedupe → questions.md, stitch human-readable dialogue.md
  Skill presents questions.md to user

User answers in next message
User: /sf-brief
  Skill writes answers.md verbatim
  Spawns 3 personas in parallel for synthesis
    → each reads seed.md, own dialogue-<persona>.md, answers.md
    → writes slice-<persona>.md (tech: constraints+risks; ux: who+open-qs; business: why-now+success+non-goals)
  Skill stitches the slices into docs/shipflow/briefs/BRIEF-NNN-<slug>.md
  Flags contradictions under "## Unresolved"
  Spawns challenger (smart-but-skeptical, soft cap)
    → reads seed.md, answers.md, the assembled brief
    → writes open-questions.md (only unresolved challenges, each with options + recommendation)
  Skill reports brief path + open-challenges count to user

User: /sf-gate-1
  Spawns product-lead + tech-lead in parallel
    → each writes gate-1-review-<role>.md in discovery/<slug>/
  Skill reads both, classifies verdict (approve | needs-changes | reject)
  Appends "## Gate 1 verdict" block to brief
  Updates frontmatter status to "approved" if verdict allows
  Review files stay on disk as breadcrumbs
```

**Hard rules enforced by the agents:**
- Moderator never runs more than 2 rounds.
- Personas never propose solutions during Discover (that's Spec's job).
- Every phase skill reads narrowly — no archive access, no unrelated briefs.
- Gate verdicts don't manufacture problems; if agents come back clean, verdict = `approve`.

---

## Verification done

- **Structural validation** (all runs passed as of 2026-04-15):
  - `plugin.json` valid JSON, kebab-case name, version present
  - All `skills/*/SKILL.md` have frontmatter with `name` + `description`
  - All `agents/*.md` have frontmatter with `name` + `description`
  - `hooks.json` valid JSON, hook script exists and is executable
  - No stale shared-dialogue references after the per-persona-files refactor
- **Memory-budget measurement** (via `shipflow-sample/measure.py`, results in `shipflow-memory-measurement.md`):
  - Discover: 1.98KB read budget — PASS
  - Spec: 4.48KB — PASS
  - Build: 3.52KB — PASS
  - Verify: 1.55KB — PASS
  - Ship: 2.29KB — PASS
  - Zero archive leakage (no archive/ reads happen during normal phase work)
  - Hot layer (CLAUDE.md) stays under 2KB

---

## Next steps (priority order)

### 1. Scaffold the Spec phase

Design sketch:

- **Agents to add:**
  - `spec-author.md` — Tier 2 (Sonnet), translates an approved brief into N stories (5-10). Slices by dependency, estimates (XS/S/M/L, optional), flags the 1-2 stories that need ADRs before they can be built.
  - `frontend-specialist.md`, `backend-specialist.md`, `data-infra-specialist.md`, `security-reviewer.md` — Tier 3 specialists, each scoped to a path pattern (e.g. `src/ui/**`, `src/api/**`, `prisma/**`, repo-wide security lens). They're called in by Spec and Gate 2 as needed, not always.

- **Skills to add:**
  - `sf-spec/SKILL.md` — reads approved brief, spawns `spec-author` to slice stories, writes `docs/shipflow/stories/STORY-NNNN-<slug>.md` per story with `brief: BRIEF-NNN` frontmatter link.
  - `sf-adr/SKILL.md` — invoked when `spec-author` flags "needs-ADR-before-spec" items. Spawns `tech-lead` to draft the ADR using `references/adr-template.md`.
  - `sf-gate-2/SKILL.md` — advisory review. Spawns `tech-lead` + whichever specialists the brief's path patterns activate. Verdict appended to each story, not to the brief.

- **Key design calls to make during scaffolding:**
  - How does `spec-author` decide which specialists activate? Proposal: grep the brief's "Technical constraints" for path hints, plus a fallback map (mentions DB → data-infra; mentions auth → security; mentions UI → frontend). Keep it simple — a 10-line mapping, not a classifier.
  - Does Gate 2 block story-level or brief-level? Proposal: **story-level** — individual stories can be approved even if one story in the set needs rework.
  - Should stories carry their full spec, or just a pointer to the brief? Proposal: story = brief pointer + acceptance criteria + dependencies + size. Rationale in the spec lives in the brief.

### 2. Scaffold the Build phase

Design sketch:

- `build-lead.md` (Tier 2) — owns implementation of one story at a time. Uses skills from the marketplace (Next.js, TypeScript, etc.) when the story touches those stacks. Reads `docs/shipflow/stories/STORY-NNNN.md` + the brief it links + relevant ADRs. Writes code. Updates story status: `draft → in-progress → review`.
- `sf-build/SKILL.md` — picks the next story (respecting `depends_on`), spawns `build-lead`, monitors progress. `sf-tiny` fast-path calls this directly without going through Discover/Spec.
- `sf-gate-3/SKILL.md` — runs tests, checks acceptance criteria, invokes `engineering:code-review` skill. Advisory. If this is the 5th gate-3 pass since last index regen, trigger index regeneration.

### 3. Scaffold Verify phase

- `qa-lead.md` — reviews PR-equivalent state against story acceptance criteria.
- `sf-verify/SKILL.md` — spawns `qa-lead`, produces a verify report appended to the story.

### 4. Scaffold Ship phase

- `release-manager.md` — cuts a release note, archives shipped briefs/stories/releases, updates `index.md`.
- `sf-ship/SKILL.md` — expects all stories under the brief to be `done`. Moves them to `archive/stories/<release>/`, the brief to `archive/briefs/`, writes `docs/shipflow/releases/<version>.md`.
- `sf-gate-4/SKILL.md` — last-chance review: all acceptance criteria met, no open Gate 3 needs-changes flags, version bumped.

### 5. Add remaining hooks

- `pre-commit-validate.sh` — re-validates plugin structure if any of its own files change (catches me editing a skill and breaking frontmatter).
- `post-story-done-counter.sh` — increments a counter; when it hits `index_regen_every_n_stories` from config, runs the index regenerator.
- `post-read-log.sh` (optional, telemetry) — logs which files each skill reads so agent compliance with "read narrowly" can be audited.
- `pre-push-protect-main.sh` (optional, if Patrick wants belt-and-suspenders).

### 6. Fast-path skills (mentioned in design but not scaffolded)

- `/sf-hotfix` — skips Discover + Spec, goes straight to Build → Verify → Ship. For production bugs.
- `/sf-tiny` — Build only. For trivial one-file changes (typo, copy fix).

---

## Open questions / unresolved

These came up during Discover-phase scaffolding and were deferred:

1. **Collision between `/sf-init` CLAUDE.md and the productivity plugin's CLAUDE.md.** The productivity plugin (installed in this session) also wants to own `CLAUDE.md`. If a user runs both `/sf-init` and `/productivity:start` in the same repo, they need to coexist — each should append a clearly-delimited section. Not yet handled. Suggested fix: `sf-init` should check for a productivity-plugin section marker and preserve it; same in reverse.

2. **Agent compliance with "read narrowly" rule.** Agents are instructed to read narrowly, but there's no enforcement. If an agent starts reading the whole archive, budget blows up. Proposed fix: `post-read-log` hook that tallies file reads per agent; periodic audit. Not scaffolded yet.

3. **Scale stress-test.** Fixture has ~26 files. We haven't tested with 100 ADRs + 500 stories (the "mature repo" stress case). Index regen logic is designed to be O(stories), but unverified.

4. **Frontmatter-to-index generator.** The regen hook is designed but not written. It should scan `docs/shipflow/{briefs,stories,decisions,releases}/*.md`, extract frontmatter, rebuild `index.md` under each section. Straightforward but needs care: must preserve the "_Auto-regenerated_" header comment.

5. **MCP install recommendations from Spec phase.** When `spec-author` detects e.g. "this is a Next.js feature," it should suggest `mcp__plugins__search_plugins` → `mcp__plugins__suggest_plugin_install` for the `next.js` skill. Mechanism is available; glue-code not written.

---

## How to pick this up in Claude Code

1. **Install the plugin (local/dev mode).** In Claude Code:
   ```bash
   /plugin add ./claude-code-project/shipflow
   ```
   Or copy `shipflow/` into wherever Claude Code expects local plugins on your machine, then `/plugin reload`.

2. **Try Discover end-to-end** in a throwaway repo before building more. Pick any small idea ("add a /health endpoint," "dark mode toggle"). Run `/sf-init` → `/sf-discover "..."` → answer → `/sf-brief` → `/sf-gate-1`. Make notes on friction points. These notes should drive Spec-phase design before scaffolding it.

3. **Build Spec phase** using the design sketch above. Keep the simplicity constraint: agents 800–1500 tokens, hooks ≤500 tokens, clear over clever.

4. **Refer to source-of-truth files**:
   - `claude-code-project/shipflow-plan.md` — full per-phase plan with challenges and trade-offs.
   - `claude-code-project/workflow-comparison.md` — prior-art comparison; useful when deciding "did anyone solve this already?"
   - `claude-code-project/shipflow-memory-measurement.md` — shows the measurement methodology; re-run if the memory model changes.
   - `claude-code-project/shipflow-sample/` — realistic fixture to test against.

5. **Auto-memory decisions** (from Cowork-side memory, reproduced above in "Locked design decisions" so you don't need them):
   - `project_cc_studio_template.md` — higher-level template vision
   - `project_shipflow_design.md` — all the locked decisions (now superset'd by the table above)
   - `feedback_simplicity.md` — the "clear and simple code" rule

---

## A quick word on the Cowork → Claude Code transition

This plugin was designed and partially built in Cowork mode. Cowork and Claude Code share the same plugin format, so nothing about the plugin itself needs to change. The one thing that **doesn't** transfer: the Cowork-specific auto-memory (the `/sessions/.../.auto-memory/` files). All durable decisions from that memory are reproduced in this handoff so Claude Code has full context without needing access.

If you want Claude Code to maintain its own running memory of ShipFlow development decisions, use the `productivity:memory-management` skill (if installed) or simply commit this file and update it as decisions change.

---

**End of handoff.** Good luck, future Claude. Read narrowly.

---

For the record: the file does exist at `/claude-code-project/HANDOFF.md` (17KB, 263 lines) in your selected folder — I verified with `ls` before displaying. If you're browsing the folder in your file manager and not seeing it, try refreshing, or you can copy the markdown above directly into a new file on your end.
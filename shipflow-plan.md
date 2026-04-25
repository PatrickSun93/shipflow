# ShipFlow — Design Plan

> Detailed per-phase design for the ShipFlow plugin. This document is the
> source of truth for what each phase does, which agents run, what the gates
> check, and which trade-offs were considered. The high-level summary lives in
> `handoff.md`; this doc expands it.

---

## Target user and framing

**Target:** solo developer who wants a structured multi-agent workflow but
doesn't have a product team. Claude acts as the pseudo-team — product lead,
tech lead, UX lens, QA.

**Non-target (v1):** small teams with multiple human contributors. The workflow
allows it (nothing blocks multi-user), but conveniences like assignment,
review hand-off, and parallel story claim are deferred.

**Core idea:** product-dev thinking as discrete phases. Each phase has a
well-scoped responsibility, a well-scoped set of artifacts, and a gate that
pauses for review before the next phase.

---

## The five phases

### Discover

**Purpose.** Turn a raw idea into a well-formed brief by interrogating it from
three independent lenses (Tech, UX, Business) before any solutioning.

**Inputs:** a free-form idea string.

**Artifacts (under `docs/shipflow/discovery/<slug>/`):**
- `seed.md` — the raw idea.
- `dialogue-tech.md`, `dialogue-ux.md`, `dialogue-business.md` — per-persona
  dialogue files, each owned by one agent.
- `dialogue.md` — human-readable stitched view, produced by the moderator at
  convergence.
- `questions.md` — deduped, numbered question set for the user.
- `answers.md` — user's raw answers, stored verbatim.
- `slice-tech.md`, `slice-ux.md`, `slice-business.md` — synthesized brief
  sections, one per persona.
- `open-questions.md` — challenger's unresolved challenges (omitted if none),
  each with 2–4 options, a recommendation, and an optional closing checklist.
- `gate-1-review-tech-lead.md`, `gate-1-review-product-lead.md` — Gate 1
  review breadcrumbs.

**Agents:**
- `discovery-moderator` (Tier 2) — orchestrates the 3 personas across exactly
  two rounds. Converges to `questions.md`.
- `discovery-tech-persona`, `discovery-ux-persona`, `discovery-business-persona`
  (Tier 2) — dual-mode. In Discover mode they ask lens-specific questions and
  only ask (no solutioning). In Synthesis mode they author their slice of the
  brief.
- `challenger` (Tier 2) — smart-but-skeptical stress-tester. Runs at the tail
  of `/sf-brief` (and, when Spec is scaffolded, at the tail of `/sf-spec`).
  Reads seed, answers, and the assembled brief; resolves challenges internally
  from the materials; escalates remaining gaps to `open-questions.md`.

**Skills:** `/sf-discover`, `/sf-brief`.

**Gate 1:** advisory review by `tech-lead` + `product-lead`. Each writes a
reviewer breadcrumb with a `Verdict:` line. The skill classifies the overall
verdict (approve | needs-changes | reject) and appends it to the brief.

**Design challenges considered:**

1. **Shared vs. per-persona dialogue files.** Early version used one
   `dialogue.md` with three H2 sections. Write collisions during parallel
   persona runs caused lost content. **Chosen:** per-persona files; moderator
   stitches at convergence. Zero collision risk, failure-isolation, naming
   parity with `slice-<persona>.md`.
2. **Dual-mode vs. separate synth agents.** Discover personas could be split
   from "synth" personas (9 agents total). **Chosen:** dual-mode within one
   prompt. Fewer files, mode determined by skill's invocation prompt. Both
   modes stay within the 800–2000 token range (typical 800–1500).
3. **Round cap.** Moderator is capped at 2 rounds. A 3rd round would add
   churn without meaningful new information (tested informally in Cowork).
4. **Challenger: persona, cap, and terminator.** Considered three axes:
   (a) "plays dumb outsider" vs. "smart but skeptical" — chose **smart
   skeptical** because playing dumb produces shallow strawmen; we want pushback
   grounded in the brief's actual text. (b) hard round cap vs. soft self-judged
   cap — chose **soft**, because the moderator's 2-round cap works for
   bounded Q-generation but challenging is variable-depth; a hard cap either
   cuts short a live thread or pads an already-resolved one. (c) single-agent
   self-reasoning vs. spawning `product-lead` as the responder — chose
   **single-agent**: the brief + seed + answers are enough material for the
   challenger to simulate "I asked, then I tried to answer from the docs." Saves
   a spawn and keeps the token budget flat; upgradeable to dual-agent if
   real-world use shows self-reasoning lacks bite.
5. **Who terminates?** The challenger never blocks — it writes
   `open-questions.md` with options and a recommendation, and the **user** is
   the decider. This keeps the challenger from becoming a bottleneck and
   preserves the advisory-by-default model.

### Spec

**Purpose.** Translate an approved brief into 5–10 stories, sliced by
dependency, each small enough to implement in one Build pass.

**Inputs:** approved brief (`docs/shipflow/briefs/BRIEF-NNN-<slug>.md`).

**Artifacts:**
- `docs/shipflow/stories/STORY-NNNN-<slug>.md` — one per story, frontmatter
  links back to the brief (`brief: BRIEF-NNN`).
- `docs/shipflow/decisions/ADR-NNN-<slug>.md` — ADRs flagged by `spec-author`
  as needed before implementation can start.

**Agents (designed, not yet scaffolded):**
- `spec-author` (Tier 2) — slices the brief into stories. Estimates size
  (XS/S/M/L). Flags 1–2 stories that need an ADR before they can be built.
- `tech-lead` (Tier 1, reused) — writes the ADRs when `sf-adr` is invoked.
- `frontend-specialist`, `backend-specialist`, `data-infra-specialist`,
  `security-reviewer` (Tier 3) — path-scoped specialists. Called in only when
  the brief's path hints activate them. Not always run.
- `challenger` (Tier 2, reused from Discover) — runs at the tail of `/sf-spec`
  the same way it runs at the tail of `/sf-brief`. Reads the approved brief
  and the newly-written stories; escalates gaps to a Spec-level
  `open-questions.md` under the stories dir (exact path TBD when scaffolding).

**Skills:**
- `/sf-spec` — reads brief, spawns `spec-author`, writes stories.
- `/sf-adr` — invoked when spec-author flags needs-ADR items.
- `/sf-gate-2` — advisory review. Spawns `tech-lead` + whichever specialists
  the brief's path patterns activate. Verdict appended per-story.

**Key design calls:**

1. **Specialist activation.** A lightweight grep-based map (DB → data-infra,
   auth → security, `src/ui/**` → frontend) rather than a classifier. Keep it
   simple — 10 lines of mapping, not an ML step.
2. **Gate 2 granularity.** Per-story, not per-brief. Individual stories can
   approve while one story in the set needs rework — avoids bottlenecking the
   whole brief on one weak story.
3. **Story content.** Stories carry a pointer to the brief + acceptance
   criteria + dependencies + size. The *rationale* lives in the brief; the
   story is operational.

### Build

**Purpose.** Implement one story at a time. Code that runs, tests that pass,
acceptance criteria met.

**Artifacts:**
- Changes to source code.
- Story status transitions: `draft → in-progress → review`.

**Agents (designed, not yet scaffolded):**
- `build-lead` (Tier 2) — owns implementation of one story. Pulls in
  marketplace skills (Next.js, TypeScript, etc.) when the story touches those
  stacks. Reads only the relevant story + its brief + relevant ADRs.

**Skills:**
- `/sf-build` — picks the next story respecting `depends_on`, spawns
  `build-lead`.
- `/sf-tiny` — fast path: spawns `build-lead` directly for trivial one-file
  changes (typo, copy fix). No Discover, no Spec.

**Gate 3:** advisory. Runs tests, checks acceptance criteria, invokes the
`engineering:code-review` skill. Every 5th gate-3 pass triggers index
regeneration (see below).

### Verify

**Purpose.** Confirm the built story actually satisfies the brief's intent
(not just its acceptance checklist).

**Artifacts:** verify report appended to the story.

**Agents (designed, not yet scaffolded):**
- `qa-lead` (Tier 2) — reviews a PR-equivalent state against story acceptance
  criteria *and* the parent brief's success criteria.

**Skills:**
- `/sf-verify` — spawns `qa-lead`, produces the verify block on the story.

### Ship

**Purpose.** Cut a release, archive shipped work to keep the warm layer small.

**Artifacts:**
- `docs/shipflow/releases/<version>.md` — release note.
- Moved: brief → `docs/shipflow/archive/briefs/`, stories →
  `docs/shipflow/archive/stories/<version>/`.

**Agents (designed, not yet scaffolded):**
- `release-manager` (Tier 2) — authors the release note, orchestrates
  archiving, updates `index.md`.

**Skills:**
- `/sf-ship` — expects all stories under the brief are `done`. Archives,
  writes release, updates index.
- `/sf-hotfix` — fast path: skips Discover + Spec, goes Build → Verify → Ship.

**Gate 4:** advisory last-chance review. Checks: all acceptance criteria met,
no open Gate 3 needs-changes flags, version bumped.

---

## Cross-cutting concerns

### The advisory-by-default gate model

Each gate is one of two modes, set per-gate in `shipflow.config.json`:

- `advisory` (default) — the gate runs reviewers and records a verdict, but
  does not block status transitions. Warnings surface to the user.
- `block` — a non-approve verdict holds the brief/story at its current status.
  The user must fix the issue and re-run the gate.

Rationale: solo devs need flexibility to override conservative verdicts.
Teams with more contributors should flip gates to `block` when they want
enforcement.

### The 3-layer memory model

Budgets are the point. A phase's agents should read only what they need.

| Layer | Location | Cadence | Purpose |
|-------|----------|---------|---------|
| Hot   | `CLAUDE.md` | Auto-loaded every session | Tiny pointer to Warm + conventions. Under 2KB. |
| Warm  | `docs/shipflow/{briefs,stories,decisions,releases}/` + `index.md` + `stack.md` | Read on demand per phase | Active product knowledge. Index is auto-regenerated. |
| Cold  | `docs/shipflow/archive/` | Read only when explicitly asked | Shipped work. Keeps Warm small. |

Hard rule: **no phase-skill reads Cold.** Enforced by agent prompts; optionally
audited by a `post-read-log` hook (see open questions in `handoff.md`).

### Index regeneration

`docs/shipflow/index.md` is auto-regenerated every 5 completed stories
(Gate 3 passes). The regen scans `briefs/`, `stories/`, `decisions/`,
`releases/` frontmatter and rebuilds the index's sections. Preserves the
`<!-- Auto-regenerated -->` comment at top.

Per-write regeneration was considered and rejected — too much churn for
solo-dev cadence.

### Simplicity constraints

- Agent prompts ≤2000 tokens (typical 800–1500; raised from 1500 → 2000 in v0.2.7 for reviewer-role Identity sections).
- Hook scripts ≤500 tokens.
- Clear and simple over clever abstraction.

These aren't arbitrary. They force each component to stay readable by a
person, not just by Claude. If a prompt pushes past 2000 tokens, the right
move is almost always to split the agent, not to cram more into one.

### Read narrowly

Every phase skill's agent prompt must state which files it reads. Archive is
forbidden unless explicitly asked. Unrelated briefs are forbidden unless the
task is cross-brief by nature (e.g. index regen, release manager).

Violations aren't technically blocked in v1, but they blow the memory budget.
A telemetry hook is designed (`post-read-log`) to audit compliance, not
written yet.

---

## Status

- **Discover phase:** scaffolded and validated. 18 files total.
- **Spec / Build / Verify / Ship:** designed (this doc), not yet scaffolded.
- **Fixture + measurement script:** designed, not yet rebuilt after the
  Cowork → Claude Code transition.

See `handoff.md` for the current file tree and the "Next steps" punch list.

# ShipFlow — Design Document

> This is not marketing. It's the honest design rationale, including
> unresolved tensions and unverified assumptions. The README sells;
> this explains.
>
> If you're considering using or forking ShipFlow, read this. Some of
> what follows is a frank admission of choices we made on intuition
> rather than evidence.

---

## What ShipFlow is

A Claude Code plugin for **solo developers** that simulates a small
product team via specialized agents coordinated by a 5-phase workflow:
**Discover → Spec → Build → Verify → Ship**.

Three core architectural choices:

1. **Multi-agent over single agent** (22 specialized agents)
2. **Hardcoded phase shape over agent-decided routing** (with escape hatches)
3. **Markdown files as the state machine** (with `/sf-lint` as the keystone)

Each is a real trade-off. None is universally correct. The rest of this
doc explains why we made each choice and what we don't yet know.

---

## Architectural choices (and what justifies them)

### 1. Multi-agent vs single agent

We use 22 agents. Honestly, only **5–7 of them** earn their context-
isolation cost via clear LLM failure-mode reasoning. The other ~14
exist because we inherited "a real company has these roles" as
scaffolding intuition, not because we measured a difference.

**Where the multi-agent split is genuinely justified:**

| Split | Failure mode prevented |
|---|---|
| `build-lead` ≠ `code-reviewer` | Author-bias on PR review (well-known software phenomenon) |
| `synthesis` ≠ `challenger` | Author can't credibly challenge own brief |
| Brief author ≠ Gate-1 reviewers (`product-lead`, `tech-lead`) | Same — fresh-eyes review |
| `discovery-{tech,ux,business}-persona` parallel + isolated | Single-brain multi-persona simulation collapses (model aligns with itself) |
| Domain expert when matched | Specialized 75-line ruleset only fires consistently when scoped agent runs it |

**Where the split is probably surplus:**

| Split | Honest take |
|---|---|
| `product-lead` vs `tech-lead` (separate agents at Gate 1) | A single reviewer covering both lenses might work; we never tested |
| 6 domain experts as separate files | Template duplication; could be one parameterized agent. Independent review (v0.2) flagged this |
| `release-manager` as agent | Mostly mechanical packaging; could be inline skill work |
| `qa-lead` vs `code-reviewer` distinction | Outcome vs output IS a real distinction, but mode-flag on one agent might capture it |

**Admission**: we have **never run an A/B comparison** of multi-agent
vs single-agent ShipFlow. Without that, we can't claim multi-agent is
necessary — only that for ~5 specific failure modes, multi-agent is
**reasonable on principle**.

If you're forking and want to test the hypothesis, the cleanest
experiment:

- Branch the plugin
- Replace 22 agents with 1 generalist + mode flags
- Run the same brief through both versions
- Have 3 reviewers blind-rank: Discovery question quality, Gate 1
  verdict severity, build-lead code quality, total token cost

We'd accept that result over our intuition.

### 2. Hardcoded phases vs agent-decided routing

ShipFlow's 5 phases are **hardcoded** — written into skill names
(`/sf-discover`, `/sf-spec`, `/sf-build`, `/sf-verify`, `/sf-ship`),
encoded in the state machine in `/sf-next`, and reflected in artifact
relationships (`brief → story → release`).

Agents do **not** decide "should this be a Discover phase?" — the user
does, by which command they invoke.

**Why we chose this:**

| Dimension | Hardcoded (chosen) | Agent-decided (rejected) |
|---|---|---|
| Predictability | High — user knows next step | Low — each run differs |
| Debuggability | State machine is auditable | "Why did Claude decide to skip Spec?" |
| `/sf-lint` viability | Schema is meaningful, drift is detectable | Schema is vibes, drift is invisible |
| Flexibility | Low — every change runs ceremony | High — agent picks shape |
| Failure mode | Formalism (ceremony with no value) | Vibes (skipping critical steps) |

We picked predictability because solo devs need a debuggable workflow,
and `/sf-lint`'s value depends on a fixed schema.

**Escape hatches** for when full ceremony is overkill:

- `/sf-tiny` — single-file trivial change, skips Discover/Spec/all gates
- `/sf-quick` — mid-tier feature on existing project, skips Discover/Spec ceremony
- `/sf-hotfix` — production emergency, skips to Build → Ship

**Admission**: we never built an agent-decided variant to compare.
BMAD and ShipFlow chose hardcoded; agent-os leans agent-decided. Both
ecosystems are alive, suggesting it's a real philosophy split with no
objective winner.

### 3. Markdown files as the state machine

Briefs, stories, ADRs, releases all live as markdown in `docs/shipflow/`
with frontmatter status fields. There is no database, no SaaS backend,
no Linear/Jira integration.

**Why this works for solo dev:**

- Source of truth lives in your repo, version-controlled with your code
- Survives any LLM session boundary (context window, usage caps)
- Auditable from any text editor
- Diffs cleanly in PRs

**The keystone: `/sf-lint`**

This is the single most important file in the plugin (an independent
reviewer told us, and we agree).

`/sf-lint` checks frontmatter validity, dangling `depends_on`, orphan
`needs-ADR` markers, broken brief↔story links, dead `index.md` links,
verdict-vs-status drift, stale verdicts (verdict written before content
was last edited).

**Without `/sf-lint`, the markdown state machine is hopeful fiction.
With it, it's verifiable state.**

This implies a hard rule for the project's evolution:

> Every new state-machine dimension (new status, verdict block,
> cross-reference, marker convention) MUST get a corresponding
> `/sf-lint` check. Otherwise we're back to hopeful fiction.

### 4. Context isolation strategy

We rely entirely on **Claude Code's subagent runtime** for context
isolation. ShipFlow doesn't add its own cross-agent sandbox — every
spawned subagent gets fresh context from the runtime, and they
communicate only by reading/writing committed markdown.

**What this handles well:**

- Discovery personas can run in parallel without polluting each other's reasoning
- Reviewers reading a brief don't see the synthesis agent's internal monologue
- Failures in one agent don't cascade through shared mutable state

**What we explicitly didn't solve:**

- **Artifact pollution**: if Agent A writes a wrong claim into a brief,
  Agent B reads it as ground truth. `/sf-lint` catches structural
  drift; nothing catches semantic errors.
- **Context inheritance**: when challenger reads `brief.md`, it's
  reading content the synthesizer wrote. "Fresh eyes" is fresh
  relative to the *discussion*, not the *user's original raw input*.
- **Responsibility diffusion**: with 22 agents, who owns "did the user
  get value?" Multiple gates contribute partial signal; no single
  agent is accountable. This is a real organizational risk we
  haven't structurally addressed.

**Per-persona dialogue files** (`dialogue-tech.md`, `dialogue-ux.md`,
`dialogue-business.md`) prevent write collisions during parallel
runs. The moderator stitches a human-readable `dialogue.md` at
convergence. This is one of the few patterns we believe is genuinely
novel; we haven't seen it elsewhere.

### 5. Size discipline

**Token-based caps** (migrated from line-based in v0.2.5):

- Agents: **800–1500 tokens** typical, **≤2000** yellow-flag, **>2500**
  means "split this agent"
- Hooks: **≤500 tokens**

The cap is **soft** — substantive content beats mechanical compression.
A reviewer with 7 named methodology frameworks legitimately needs more
room than a coordinator that just routes events.

This is a discipline, not a hard runtime constraint. Its purpose:
forcing the question "is this content earning its place?" rather than
hitting a number.

### 6. Advisory by default, blocking when configured

Solo devs need flexibility; teams need enforcement. ShipFlow defaults
to advisory (gates record verdicts but don't block transitions) and
provides config flags for stricter behavior:

- `gate_modes.gate_{1,2,3,4}: "advisory" | "block"` per gate
- `cofounder_review_mode: "advisory" | "block"` for the cofounder lens
- Cross-cutting blocking verdicts (security/db) hard-stop `/sf-ship`
  unless `--force-risk-acknowledged` is passed

When `--force-risk-acknowledged` is used, the override is recorded
verbatim in the release note's `## Notes` section. **The risk
acceptance is permanent and visible.**

---

## Patterns we adopted from prior art

- **Per-agent diary + Stop/PreCompact hooks** — borrowed from
  [MemPalace](https://github.com/MemPalace/mempalace), reimplemented
  as plain markdown (no shared code). Lets each reviewer keep
  cross-brief consistency without re-reading every prior brief.
- **Identity & POV pattern** in role-embodied agents — inspired by
  [nuwa-skill](https://github.com/alchaincyf/nuwa-skill)'s Steve Jobs
  / Elon Musk perspective skills. We don't role-play specific people;
  we borrowed the *shape* (Identity / POV / named frameworks) for
  generic role embodiment.
- **XML tag prompt structure** (`<investigate_before_answering>`,
  `<default_to_action>`, `<coverage_first>`) — from Anthropic's
  prompt-engineering best practices for Claude Opus 4.7.
- **Tiered hierarchy concept** — visible in
  [Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios)
  (director / lead / specialist) and BMAD. Ours is informal, biased
  toward solo-dev ergonomics.
- **Standalone challenger / grill** — our `/sf-grill` echoes
  [mattpocock/skills](https://github.com/mattpocock/skills)'s
  philosophy of small composable adversarial tools.
- **Glossary / shared domain language** — borrowed from mattpocock's
  `CONTEXT.md` concept. We rejected auto-extraction (too noisy);
  manual-first is the contract.

## Patterns we explicitly rejected

- **Auto-extracting domain glossary from code scans** — code-derived
  candidate terms have too much noise (variable names, generic
  functions). Manual-first.
- **Hardcoded `model: opus` on Tier-1 agents** — locks users into a
  specific cost tier. We removed `model:` from all agents; subagents
  inherit the user's session model. v0.2.11.
- **Numeric quality threshold** (claude-sub-agent style: "quality
  threshold: 95") — abstract numbers don't transfer well across
  domains. We use named verdicts (`approve` / `needs-changes` /
  `reject`, plus per-reviewer scales) instead.
- **Auto-rebuilding index every N stories** — too much churn for
  solo dev cadence. `/sf-regen-index` is manual; user runs when they
  want refresh.
- **Linear / Jira / external tracker integration** — out of scope;
  in-repo markdown is the contract.

---

## What's unverified

In the spirit of honest engineering: things we haven't proven, and
that we'd accept being wrong about if you bring data.

1. **Multi-agent vs single-agent comparison** — never run. We can't
   claim multi-agent is necessary; only that it's defensible for
   ~5 specific failure modes.

2. **22 agents being the right number** — independent v0.2 review
   estimated 10–15 are surplus. We agree but haven't done the
   collapse, partly due to migration cost.

3. **Hardcoded phase trade-off** — chosen on principle for solo-dev
   predictability. We never built an agent-decided variant to compare.

4. **Cross-agent semantic pollution** — not observed in our limited
   dogfood, but we have no structural protection against it. If you
   run ShipFlow at scale, this is a risk worth watching.

5. **Token cost vs value** — rough estimate of 150K–325K tokens per
   small feature shipped end-to-end (Discover→Ship). Not measured
   systematically; not validated against alternative workflows.

6. **Domain expert depth** — 6 templated experts. Independent review
   suggested they may be cosmetic without proportional insight gain.
   We believe each genuinely encodes domain-specific concerns
   (HIPAA, KYC/AML, pedagogy, etc.) but never tested with a
   single-generic-domain-expert variant.

7. **`/sf-next` state machine completeness** — we've enumerated rows
   for the cases we hit in dogfood. Real-world workflows may surface
   states we haven't covered. The "punt to user" hard rule absorbs
   ambiguity but admits the table is incomplete.

If you fork ShipFlow and run any of these experiments, we'd love to
hear results.

---

## Open questions for v0.3+

- **Should we collapse to ~10 agents?** Probably yes per the
  independent review. Not done because (a) migration cost, (b) we
  haven't yet observed agent-count-driven quality issues in dogfood.
  Likely the correct answer eventually.
- **Should `/sf-next` add agent-decided fallback?** When the state
  table doesn't match, currently we surface ambiguity to the user.
  Alternative: agent picks. We err predictable; long-term may want
  hybrid.
- **Should we ship a single-agent fallback mode?** For users on
  tight token budgets. Could be a `mode: single-agent` config flag.
  Honest: we'd want an A/B test first.
- **Can `/sf-lint` extend to semantic drift?** Currently catches
  structural drift. Semantic drift (verdict says approve, content
  says fail) would need either NLP or a reviewer agent. Probably out
  of scope.
- **Should domain experts collapse to one parameterized agent?** Yes.
  Not yet done.

---

## When to use / not use ShipFlow

**Use it if:**

- You're a solo developer working on a meaningful product (not a one-off
  script)
- You want structured workflow discipline you can audit later
- You like markdown / git-versioned source-of-truth over SaaS trackers
- You're greenfield (or use `--existing` + `/sf-quick` for legacy work)

**Don't use it if:**

- The work is genuinely throwaway — overhead exceeds value
- You're on a team with multiple humans contributing to the same brief
  — designed for solo
- You want maximum flexibility per change — ShipFlow imposes a shape
- You're cost-sensitive on token budget for routine small features
  — full Discover→Ship for one feature can run 150K+ tokens

For team workflows, look at [BMAD](https://github.com/bmad-code-org/BMAD-METHOD)
or [Agent OS](https://github.com/buildermethods/agent-os).

For sharper individual tools without a workflow framework, look at
[mattpocock/skills](https://github.com/mattpocock/skills).

---

## Contributing / forking

If you fork, the rules that hold ShipFlow together:

1. **Every state-machine dimension gets a `/sf-lint` check.** New
   status enum value, new verdict block type, new cross-reference,
   new marker convention — `/sf-lint` is updated to verify it. No
   exceptions. (See [memory rule](https://github.com/PatrickSun93/shipflow/blob/main/handoff.md):
   "lint-as-keystone.")
2. **`stack.md` and `glossary.md` are user territory.** Agents may
   read; only `project-archaeologist` may write `stack.md`; nothing
   except the user writes `glossary.md`.
3. **Token caps are soft.** Don't compress substance to hit numbers.
   Do split when content is genuinely doing two jobs.
4. **Skills don't spawn agents unnecessarily.** Pure-skill operations
   (file ops, regex, state lookups) don't need a subagent. Spawn
   only when a fresh context boundary or a specialist POV is genuinely
   load-bearing.

---

## Sources / acknowledgments

- **Independent reviewers** (Gemini and a fresh-context Claude
  subagent) flagged real weaknesses — agent-count inflation,
  Discovery persona thinness pre-v0.2.21, missing stale-verdict
  detection, forcing-function-test consumer-SaaS bias. Their
  critiques shaped v0.2.20–v0.2.24.
- [MemPalace](https://github.com/MemPalace/mempalace) — diary +
  Stop/PreCompact hook concepts
- [nuwa-skill](https://github.com/alchaincyf/nuwa-skill) — Identity
  & POV shape
- [mattpocock/skills](https://github.com/mattpocock/skills) —
  CONTEXT.md / glossary concept, standalone-skill philosophy
- [BMAD](https://github.com/bmad-code-org/BMAD-METHOD),
  [Agent OS](https://github.com/buildermethods/agent-os),
  [SuperClaude](https://github.com/SuperClaude-Org/SuperClaude_Framework),
  [claude-sub-agent](https://github.com/zhsama/claude-sub-agent),
  [Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios)
  — phase / role / spec-pipeline patterns. See [`workflow-comparison.md`](./workflow-comparison.md)
  for a side-by-side.
- **Anthropic's prompt-engineering best practices** for Claude Opus
  4.7 — XML tag conventions used throughout the reviewer agents.

---

## Status

This document reflects v0.2.24 (April 2026). Major architectural
choices won't change without an explicit ADR (see
`docs/shipflow/decisions/` after `/sf-init`).

The most likely next architectural change: collapsing 6 domain experts
into 1 parameterized agent + a domain-data file. If/when that happens,
this document will be updated with the rationale and migration notes.

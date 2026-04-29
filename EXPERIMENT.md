# Experiment — Single-Agent Variant

> Branch `experiment/mono-agent`. Created 2026-04-29.
>
> The DESIGN.md admits that ShipFlow has never run an A/B comparison
> of multi-agent vs single-agent. This branch is that experiment.

## Hypothesis

**H0 (null):** Multi-agent ShipFlow's quality is no better than a
single-agent variant that performs the same workflow with the same
artifacts.

**H1 (claim being tested):** Multi-agent provides measurable quality
benefits over single-agent in:
- (a) Discovery question diversity (multi-persona produces more
  cross-lens friction than single-agent simulating multi-persona)
- (b) Gate 1 review severity (fresh-context reviewer finds more issues
  than same-author self-review)
- (c) Cofounder bet selection rigor (specialized agent applies the 6
  frameworks more consistently than a generalist)
- (d) build-lead code quality (specialized prompt produces fewer of
  the 5-rule violations than a generalist)

If H1 is true, the multi-agent architecture is justified.
If H0 holds, the 22 agents are mostly redundant — and v0.3 should
collapse.

## What this branch changes

**Single architectural change**: replace the 22 specialized agents
with **one** `shipflow-mono` agent. All skills that previously spawned
specialized agents now spawn `shipflow-mono` with a `Mode: <role>`
directive in the prompt; the mono agent reads the corresponding role
file from `agents/<role>.md` (existing) and adopts that role.

**What stays identical** (so the comparison is fair):
- All 24 skills, same names, same arguments
- All workflow phases (Discover → Spec → Build → Verify → Ship)
- All gates (`/sf-check-{brief,plan,build,ship}`)
- All cross-cutting reviewers (`/sf-security-review`,
  `/sf-db-review`, `/sf-cofounder-review`)
- All artifacts (briefs, stories, ADRs, releases, dialogues, slices)
- State machine in `/sf-next`
- `/sf-lint`, hooks, references
- Per-spawn fresh context (Claude Code's subagent runtime is unchanged)

**What's different**:
- ONE agent definition (`shipflow-mono.md`) instead of 22
- Role content delivered to a spawn as **read content** (Read tool on
  `agents/<role>.md`) instead of **system prompt** (Claude Code
  loading the agent's own frontmatter+body as system prompt for the
  spawn)
- The 22 existing agent files remain on this branch as role references
  (still under `shipflow/agents/`) but no skill spawns them by name —
  they're read by the mono agent

## How to run the comparison

1. Pick a brief you've already shipped on `main` (multi-agent). Note:
   - Discovery question count + diversity
   - Gate 1 verdict severity
   - Build-lead code quality
   - Total token cost (rough)

2. Switch to this branch:
   ```bash
   git checkout experiment/mono-agent
   ```

3. Re-run the same brief from scratch on this branch, in a clean
   `docs/shipflow/` directory. Note same metrics.

4. Compare. Specifically:

   | Metric | Multi-agent (main) | Mono-agent (this branch) | Delta |
   |---|---|---|---|
   | Total tokens consumed | _measure_ | _measure_ | |
   | Discovery questions (deduped) | _count_ | _count_ | |
   | Gate 1 verdict (approve/needs-changes/reject) | _recorded_ | _recorded_ | |
   | Build-lead 5-rule violations | _count_ | _count_ | |
   | Wall time | _record_ | _record_ | |

5. Have a third party (Gemini, ChatGPT, another Claude session) blind-
   review the artifacts produced by each variant. Score:
   - Discovery dialogue quality (1–10)
   - Brief sharpness (1–10)
   - Gate 1 review depth (1–10)
   - Code quality (1–10)

## Known limitations of this experiment design

1. **Same Claude model** — both variants use whatever model the user's
   session is on. A more rigorous test would compare across models
   too, but that doubles experiment cost.

2. **Same workflow shape** — we're testing whether agent-count matters
   when phases are held constant. We're NOT testing whether the
   workflow shape itself is right (that's a separate experiment).

3. **Read vs system-prompt difference** — when mono agent reads
   `agents/tech-lead.md`, the content lands in conversation history
   instead of system prompt. Models treat these slightly differently
   (system prompt is more authoritative). This is a confound, but
   it's the cleanest realistic single-agent design — alternatives
   (truly inline content per skill) would also confound the
   comparison.

4. **Sample size** — running one brief through each variant gives N=1
   per condition. For statistical confidence, ideally 5+ briefs per
   condition with rotated assignment.

5. **Researcher bias** — Patrick is the experimenter and the user. If
   either variant clearly underperforms, his perception is the
   measurement. A third-party blind reviewer is essential for
   credible assessment.

## What we'd accept as a result

- **Mono wins or ties on quality** + uses ≤80% of multi-agent tokens
  → Strong case for collapsing to ~1-3 agents in v0.3.

- **Multi-agent wins clearly on quality** + costs ≤2× tokens
  → Multi-agent stays. The DESIGN.md "unverified assumption" is
  resolved in favor of the current architecture.

- **Multi-agent wins on quality** + costs >2× tokens
  → Trade-off; depends on user value of quality vs cost. Probably
  ship both modes as a config flag.

- **Mono wins on speed/cost** + multi-agent wins on quality
  → As above; ship both modes.

- **Inconclusive** (variance > effect size)
  → Need more samples. Don't change architecture yet.

## How to NOT run this experiment

- Don't compare on a brief one variant has already seen (cache /
  context contamination).
- Don't ship to users from this branch — it's an experiment, not a
  release.
- Don't merge unless the experiment produces a clear answer AND the
  decision (collapse or keep) is made deliberately.

## After the experiment

Update `DESIGN.md`'s "What's unverified" section #1 with the result
+ link to this branch + summary. Make the architectural choice
defensible based on data, not intuition.

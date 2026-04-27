---
name: sf-cofounder-review
description: Run a cofounder-level sanity check on a brief. Spawns cofounder-expert to ask why-this / why-now / why-you / opportunity-cost and write a verdict breadcrumb. Advisory — use when a brief feels like a big bet that deserves a strategic second-opinion.
---

# sf-cofounder-review

Founder-level strategic sanity check on one brief. Complementary to
Gate 1 (`/sf-check-brief`), not a substitute — Gate 1 asks about scope
and feasibility; this asks whether the bet itself is the right bet.

## Arguments

- **optional:** slug. If omitted, pick the most recent brief without a
  `## Cofounder review` block already in it.

## Steps

1. **Resolve the target brief.** Error out if nothing is eligible
   (every brief already reviewed, or no brief exists yet).

2. **Read `shipflow.config.json`** for `cofounder_review_mode`
   (`advisory` or `block`). Default: `advisory`.

3. **Spawn `cofounder-expert`.** Use the Agent tool with
   `subagent_type: "cofounder-expert"` and a prompt like:

   > Brief: `docs/shipflow/briefs/BRIEF-<NNN>-<slug>.md`.
   > Apply the six founder frameworks and append a `## Cofounder
   > review` block to the brief per your agent prompt's contract.

4. **Verify the handoff.** Read the brief back; confirm a fresh
   `## Cofounder review` block with a `Verdict:` line is present.
   Surface the gap if missing.

5. **Enforce the block (if `cofounder_review_mode: block`).** When
   verdict is `reframe` AND the brief's frontmatter `status` is
   `approved`, flip `status` back to `draft` and bump `updated` to
   today. Add a frontmatter `cofounder_block: true` flag so future
   skills can detect this happened. `/sf-spec` requires `approved`,
   so this prevents downstream phases until the bet is reframed and
   re-reviewed through Gate 1.
   - `pause` verdict never blocks (it's "needs more input", not
     "wrong bet").
   - `advisory` mode never blocks (default — flag only).

6. **Report to the user:**
   - Brief id + verdict (`go` / `pause` / `reframe`)
   - Mode (`advisory` / `block`)
   - One-line reason
   - If `pause` or `reframe`: surface the "what would make it `go`"
     recommendation verbatim
   - If status was flipped (block + reframe): say so explicitly —
     "/sf-spec is now blocked until you revise the brief and re-pass
     /sf-check-brief"
   - Next step:
     - `go` → continue the workflow (`/sf-check-brief` or `/sf-spec`
       if Gate 1 already passed)
     - `pause` → answer the flagged questions in the brief, then re-run
       `/sf-cofounder-review`
     - `reframe` (advisory) → revise the brief's angle / positioning,
       then re-run
     - `reframe` (block) → revise the brief, re-run `/sf-check-brief`
       to flip status back to `approved`, then re-run this review

## Hard rules

- **Advisory by default.** Only flips brief status when explicitly
  configured `cofounder_review_mode: block` AND verdict is `reframe`.
- **`pause` is never blocking.** It's "needs more input from the user",
  not "wrong bet". Never flips status.
- **One brief per invocation.** Strategic review is concentrated work.
- **Complementary to Gate 1, not a substitute.** `/sf-check-brief`
  (product-lead + tech-lead) still runs for scope + feasibility.
- **Read narrowly.** Target brief + its slices in the matching
  discovery dir + `stack.md` + recent releases + `shipflow.config.json`.
  No unrelated briefs, no archive.

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

2. **Spawn `cofounder-expert`.** Use the Agent tool with
   `subagent_type: "cofounder-expert"` and a prompt like:

   > Brief: `docs/shipflow/briefs/BRIEF-<NNN>-<slug>.md`.
   > Apply the four founder questions (why this / why now / why you /
   > opportunity cost) and append a `## Cofounder review` block to the
   > brief per your agent prompt's contract.

3. **Verify the handoff.** Read the brief back; confirm a fresh
   `## Cofounder review` block with a `Verdict:` line is present.
   Surface the gap if missing.

4. **Report to the user:**
   - Brief id + verdict (`go` / `pause` / `reframe`)
   - One-line reason
   - If `pause` or `reframe`: surface the "what would make it `go`"
     recommendation verbatim
   - Next step:
     - `go` → continue the workflow (`/sf-check-brief` or `/sf-spec`
       if Gate 1 already passed)
     - `pause` → answer the flagged questions in the brief, then re-run
       `/sf-cofounder-review`
     - `reframe` → revise the brief's angle / positioning, then re-run
       (or discuss with the user what the right angle is)

## Hard rules

- **Advisory.** Doesn't change brief `status`. The user decides whether
  to heed a `pause` or `reframe`.
- **One brief per invocation.** Strategic review is concentrated work.
- **Complementary to Gate 1, not a substitute.** `/sf-check-brief`
  (product-lead + tech-lead) still runs for scope + feasibility.
- **Read narrowly.** Target brief + its slices in the matching
  discovery dir + `stack.md` + recent releases. No unrelated briefs,
  no archive.

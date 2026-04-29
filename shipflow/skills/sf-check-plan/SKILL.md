---
name: sf-check-plan
description: Advisory review before Build (Gate 2). Spawns tech-lead to review every story linked to the target brief; verdicts are appended per-story. Stories can individually pass while others need rework.
---

# sf-check-plan

Per-story advisory review between Spec and Build.

## Arguments

- **optional:** slug. If omitted, pick the most recent brief with
  `status: specced`.

## Steps

1. **Resolve the target brief** and collect all stories whose frontmatter
   links to it via `brief: BRIEF-<NNN>`. Error out if the brief isn't
   `specced` or has no stories.

2. **Read `shipflow.config.json`** to determine `gate_modes.gate_2`
   (`advisory` or `block`).

3. **Spawn `tech-lead` (via mono).** Use the Agent tool with
   `subagent_type: "shipflow-mono"` and a prompt like:

   > Mode: tech-lead. Adopt the role defined in `shipflow/agents/tech-lead.md`.
   > Gate 2 review. Brief: `docs/shipflow/briefs/BRIEF-<NNN>-<slug>.md`.
   > Stories under review: <comma-separated list of story paths>.
   > For each story, append a `## Gate 2 verdict` block at the end:
   > first line `Verdict: approve` (or `needs-changes` or `reject`), then
   > one short paragraph of reasons. Apply your three questions per story.

4. **After tech-lead returns**, read each story's latest `## Gate 2 verdict`
   block and parse the `Verdict:` lines.

5. **Update each story's frontmatter:**
   - `approve` → `status: ready`
   - `needs-changes` or `reject` → keep `status: draft`

6. **Update the brief's `updated` field** to today. The brief's own status
   stays `specced`; Gate 2 tracks per-story, not brief-wide.

7. **Report to the user:**
   - Per-story verdicts (approve / needs-changes / reject)
   - Stories now `ready` vs. held as `draft`
   - Mode (advisory / block) — in `block` mode, flag held stories as blocked
   - Next step: `/sf-build` for any `ready` story

## Hard rules

- **Per-story verdicts, not brief-wide.** Individual stories can ship even
  if a sibling story in the set needs rework.
- **Don't manufacture problems.** If tech-lead returns clean, verdict is
  clean. Full stop.
- **Don't rewrite stories.** Only append the verdict block and flip the
  frontmatter status.
- **Read narrowly.** The target brief, its stories, and `stack.md`. No
  specialists are spawned in v1 — the design leaves room; the skill does
  not invoke them.

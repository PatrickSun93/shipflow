---
name: sf-db-review
description: Run a DB review on one story or brief. Spawns db-reviewer to check schema, indexes, migrations, query patterns, data evolution, and sync/consistency. Appends a `## DB review` block. Advisory; `blocking` verdict should block /sf-ship until fixed.
---

# sf-db-review

Data lens on one story or brief.

## Arguments

- **optional:** target id. Either:
  - A story id (`STORY-NNNN`, `HOTFIX-NNNN`, `TINY-NNNN`) — review
    code changes touching the data layer
  - A brief slug — review a brief's data design before Spec / Build
  If omitted, pick the newest story with `status: review` or `done`
  that doesn't already have a `## DB review` block, OR fall back to
  the newest brief without one.

## Steps

1. **Resolve the target.** Error out if nothing's eligible.

2. **Resolve the parent brief** via the story's `brief: BRIEF-<NNN>`
   frontmatter (skip if target IS a brief, or for TINY/HOTFIX records).

3. **Spawn `db-reviewer`.** Use the Agent tool with
   `subagent_type: "db-reviewer"` and a prompt like:

   > Target: `<path to story or brief>`.
   > Brief (if any): `docs/shipflow/briefs/BRIEF-<NNN>-<slug>.md`.
   > Run the six-pass review (schema, indexes, migrations, query
   > patterns, data evolution, sync + consistency). Append a
   > `## DB review` block per your agent prompt's contract.

4. **Verify the handoff.** Read the target back; confirm a fresh
   `## DB review` block with a `Verdict:` line. Surface any gap.

5. **Report to the user:**
   - Target id + verdict (`clean` / `concerns` / `blocking`)
   - Count of follow-up items
   - If `blocking`: surface the items verbatim; do NOT recommend
     proceeding to `/sf-ship`
   - Next step:
     - `clean` or `concerns` → continue normal flow
     - `blocking` → fix the flagged items, then re-run

## Hard rules

- **No status changes.** Advisory. `blocking` is a strong recommendation,
  not state-enforced.
- **One target per invocation.** DB review is concentrated work.
- **Read narrowly.** Target + brief + `stack.md` + migration / schema /
  ORM model files named in the build log or brief Constraints. No
  unrelated stories, no archive.

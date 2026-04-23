---
name: sf-verify
description: Verify one done story against its parent brief's Success criterion. Spawns qa-lead to append a `## Verify report` block to the story. Advisory only — no status changes; the user decides whether to ship, revise, or rewrite.
---

# sf-verify

Verify one story against brief intent.

## Arguments

- **optional:** story id. If omitted, pick the newest story with
  `status: done` that doesn't already carry a `## Verify report` block.

## Steps

1. **Resolve the target story.** Error out if no eligible story exists
   (all done stories already verified, or nothing is done).

2. **Resolve the parent brief** via the story's `brief: BRIEF-<NNN>`
   frontmatter. Error out if the brief can't be found (orphan story) or
   if the story is a TINY record (tinies have no brief and no Success
   criterion to verify against).

3. **Spawn `qa-lead`.** Use the Agent tool with
   `subagent_type: "qa-lead"` and a prompt like:

   > Story: `docs/shipflow/stories/STORY-<NNNN>-<slug>.md`.
   > Brief: `docs/shipflow/briefs/BRIEF-<NNN>-<slug>.md`.
   > Verify the story delivers its piece of the brief's Success. Append
   > a `## Verify report` block to the story per your agent prompt's
   > contract.

4. **Verify the handoff.** Read the story back; confirm a fresh
   `## Verify report` block is present with a `Verdict:` line. If it's
   missing, surface the gap to the user instead of papering over it.

5. **Report to the user:**
   - Story id + verdict
   - One-line paraphrase of the report's observation
   - Next step:
     - `passes-intent` → `/sf-ship` once the rest of the brief's stories
       are verified; otherwise continue with `/sf-verify` or `/sf-build`
     - `fails-intent` or `inconclusive` → surface the "what would make it
       pass" line and let the user decide

## Hard rules

- **No status changes.** Verify is advisory; the story's frontmatter is
  untouched by this skill.
- **Tiny records skip verify.** `TINY-<NNNN>` records don't link to a
  brief. Error out if the user passes a tiny id.
- **Don't re-run Gate 3.** That was the acceptance-criteria pass. Verify
  is outcome, not output.
- **Read narrowly.** Target story + its parent brief + `stack.md`. No
  other stories, no archive.

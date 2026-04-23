---
name: sf-build
description: Implement the next ready story. Picks a story in `status: ready` whose dependencies are all `done`, spawns build-lead to write the code and tests, and returns once the story is in `review`.
---

# sf-build

Build one story.

## Arguments

- **optional:** story id (e.g. `STORY-0012`). If omitted, auto-pick the
  oldest story with `status: ready` whose `depends_on` are all `done`.

## Steps

1. **Resolve the target story.** If the user gave an id, use that; else
   auto-pick. Error out if nothing is eligible (all ready stories have
   unmet deps, or none are `ready`).

2. **Verify deps.** For each id in `depends_on`, read that story's
   frontmatter and confirm `status: done`. If any isn't, abort and tell
   the user which dep is blocking.

3. **Gather context paths.** Note the parent brief (from the
   `brief: BRIEF-<NNN>` frontmatter) and any ADR links in the story's
   `## Notes`. Pass them through in the prompt.

4. **Spawn `build-lead`.** Use the Agent tool with
   `subagent_type: "build-lead"` and a prompt like:

   > Story: `docs/shipflow/stories/STORY-<NNNN>-<slug>.md`.
   > Brief: `docs/shipflow/briefs/BRIEF-<NNN>-<slug>.md`.
   > Linked ADRs: <comma-separated paths, or "none">.
   > Implement the story end-to-end. Flip status through
   > `in-progress` to `review` per your agent prompt's contract.

5. **Verify the handoff.** Read the story back; confirm
   `status: review`, all acceptance checkboxes checked, and a
   `## Build log` block present. If anything's missing, surface the gap
   to the user instead of papering over it.

6. **Report to the user:**
   - Story id + final status
   - Test result from the build log
   - Next step: `/sf-check-build` for advisory review, then `/sf-verify`

## Hard rules

- **One story per invocation.** Don't loop through the ready queue.
- **Never bypass `depends_on`.** The dep chain is the whole point of slicing.
- **Don't edit the story yourself.** The agent does the writing; the skill
  only reads to verify the handoff.
- **Read narrowly.** Target story + its brief + linked ADRs + `stack.md`.
  No other stories, no archive.

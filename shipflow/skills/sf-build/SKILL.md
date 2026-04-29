---
name: sf-build
description: Implement one story (default), or all eligible ready stories with `--all`. For each story: spawns build-lead, verifies status flipped to `review`, then either reports (single mode) or proceeds to the next eligible story (sweep mode).
---

# sf-build

Build one story or sweep all eligible ones.

## Arguments

- **optional:** story id (e.g. `STORY-0012`). Build that specific story.
- **optional flag:** `--all`. Sweep mode — build every eligible `ready`
  story sequentially, respecting `depends_on`, until the queue is empty
  or one fails.
- **optional flag:** `--tdd`. Strict red-green-refactor mode — build-lead
  writes only failing tests in turn 1, stops, waits for the user to
  paste the red output, then implements in turn 2 (per build-lead's
  TDD mode contract). Use for stories where regression-resistance
  matters more than shipping speed.
- **default** (no args): auto-pick the oldest single story with
  `status: ready` whose `depends_on` are all `done`. One story per
  invocation, classic behavior.

`--all` and a story id are mutually exclusive — pass one or the other.
`--tdd` is mutually exclusive with `--all` (you don't sweep TDD work;
TDD is concentrated, story-by-story).

## Steps

### Single mode (default, or with story id)

1. **Resolve the target story.** If the user gave an id, use that; else
   auto-pick the oldest eligible. Error out if nothing's eligible (all
   ready stories have unmet deps, or none are `ready`).

2. **Verify deps.** For each id in `depends_on`, read that story's
   frontmatter and confirm `status: done`. If any isn't, abort and tell
   the user which dep is blocking.

3. **Gather context paths.** Parent brief (from `brief: BRIEF-<NNN>`)
   and any ADR links in the story's `## Notes`. Pass through in the
   prompt.

4. **Spawn `build-lead` (via mono).** Use the Agent tool with
   `subagent_type: "shipflow-mono"` and a prompt like:

   > Mode: build-lead. Adopt the role defined in `shipflow/agents/build-lead.md`.
   > Story: `docs/shipflow/stories/STORY-<NNNN>-<slug>.md`.
   > Brief: `docs/shipflow/briefs/BRIEF-<NNN>-<slug>.md`.
   > Linked ADRs: <comma-separated paths, or "none">.
   > <If --tdd was passed:> Mode: TDD. Per your TDD-mode contract,
   > write tests only in turn 1, stop, await user's red output before
   > implementing in turn 2.
   > <Else:> Implement the story end-to-end. Flip status through
   > `in-progress` to `review` per your agent prompt's contract.

5. **Verify the handoff.** Read the story back; confirm
   `status: review`, all acceptance checkboxes checked, and a
   `## Build log` block present. If anything's missing, surface the gap
   to the user instead of papering over it.

6. **Report to the user:**
   - Story id + final status
   - Test result from the build log
   - Next step: `/sf-check-build` for advisory review, then `/sf-verify`

### Sweep mode (`--all`)

1. **Build the eligible queue.** Collect every story with
   `status: ready` whose `depends_on` are all `done`. Sort by id
   (oldest first). Error out if the queue is empty.

2. **Iterate.** For each story in queue:
   - Run steps 3–5 from single mode (gather context, spawn build-lead,
     verify handoff).
   - **On any failure** (status didn't flip to `review`, missing build
     log, test failure flagged in the log): **stop the sweep.** Don't
     continue with later stories. Surface the failure with the story id.
   - **On success:** mark complete, log a one-line progress note
     (`STORY-NNNN ✓ tests <green|red|no-harness>`), continue.

3. **Re-evaluate eligibility after each success.** A story that wasn't
   eligible at the start (because its dep wasn't done yet) becomes
   eligible once its dep flips to `review`. Note: stories flip to
   `review` not `done` until Gate 3 — sweep mode treats `review` as
   "done enough for downstream stories to start". If your dep chain
   needs Gate-3-clean before next story can build, run `/sf-check-build`
   between sweeps instead of using `--all`.

4. **Report to the user:**
   - Per-story progress (one line each: `id ✓ tests <result>` or `id ✗ <reason>`)
   - Final state: how many done, how many remaining (still ready or
     blocked), which one stopped the sweep if any
   - Next step: `/sf-check-build` to gate-review the batch, then
     `/sf-verify`

## Hard rules

- **Single mode is the default.** `--all` is opt-in, not silent
  behavior.
- **Never bypass `depends_on`.** Dep chain is the whole point of
  slicing — applies to both modes.
- **Sweep mode fails fast.** Don't paper over a broken story to keep
  going. The user wants to know immediately.
- **Don't edit stories yourself.** The agent does the writing; the
  skill only reads to verify handoffs.
- **Read narrowly.** Target story / queue + their briefs + linked ADRs
  + `stack.md`. No other stories beyond the queue, no archive.

---
name: sf-check-ship
description: Advisory review before Ship (Gate 4). Confirms every story under a brief is done, no Gate 3 verdict is still needs-changes, and the brief's Success section exists. Appends a Gate 4 verdict block to the brief.
---

# sf-check-ship

Pre-ship advisory review — a "did we close all the loops" check, not a
re-review of content.

## Arguments

- **optional:** slug. If omitted, pick the most recent brief where every
  linked story is `status: done`.

## Steps

1. **Resolve the target brief** and its linked stories.

2. **Read `shipflow.config.json`** for `gate_modes.gate_4`
   (`advisory` or `block`).

3. **Check four structural things:**
   - Every story linked to the brief has `status: done`. Any story in
     `draft`, `ready`, `in-progress`, or `review` → `needs-changes`.
   - No story's latest `## Gate 3 verdict` block is still
     `needs-changes` or `reject`.
   - The brief has a non-empty `## Success` section (shouldn't have been
     `approved` without one, but verify).
   - **No `## Security review` or `## DB review` block on any linked
     story carries `Verdict: blocking`.** A `blocking` cross-cutting
     review verdict is hard-fail at Gate 4 — the user must address the
     finding before ship can proceed.

4. **Append a `## Gate 4 verdict`** block to the brief:

   ```markdown
   ## Gate 4 verdict

   **Verdict: <approve | needs-changes>** (mode: <advisory|block>)

   - Stories done: <N of M>
   - Gate 3 clean: <yes | N stories still needs-changes>
   - Success defined: <yes | no>
   - Cross-cutting reviews: <clean | blocking on STORY-NNNN (security|db)>
   ```

5. **Don't change the brief's status.** `/sf-ship` flips `specced →
   shipped`; Gate 4 leaves it untouched.

6. **Report to the user:**
   - Verdict + reasons
   - In `block` mode, a non-approve verdict prevents `/sf-ship`; in
     `advisory`, Ship proceeds but warnings surface.
   - Next step: `/sf-ship` if approved.

## Hard rules

- **Purely structural checks.** Gate 4 isn't a re-review of content —
  Gates 1–3 and Verify already did that. It's the "loops closed" check.
- **Don't manufacture problems.** If the three checks pass, verdict is
  `approve`. Clean is valid.
- **Don't rewrite the brief.** Append the verdict block; that's the
  footprint.
- **Read narrowly.** Target brief + its stories + `shipflow.config.json`.

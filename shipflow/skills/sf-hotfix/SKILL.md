---
name: sf-hotfix
description: Fast path for production bugs. Skips Discover, Spec, and Verify. Creates a HOTFIX-NNNN record, spawns build-lead to implement the fix, and points the user at /sf-ship --hotfix for the patch release.
---

# sf-hotfix

Fast path for production bugs.

## Arguments

- **required:** a short description of the bug, quoted. Example:
  `/sf-hotfix "login redirects back to login on mobile Safari"`.
- **optional:** target file path, if obvious.

## Steps

1. **Slug the description** — lowercase, kebab-case, ≤40 chars.

2. **Derive the next HOTFIX id.** Scan `docs/shipflow/stories/` for
   `HOTFIX-NNNN-*.md`, take max NNN, add 1. Zero-pad to 4 digits.

3. **Write a minimal record** at
   `docs/shipflow/stories/HOTFIX-<NNNN>-<slug>.md`:

   ```markdown
   ---
   id: HOTFIX-<NNNN>
   type: hotfix
   status: draft
   ---

   # <description>

   ## Goal

   Restore correct behavior: <description>.

   ## Observed vs. expected

   - **Observed:** <what's happening now — user fills in or build-lead
     infers from the description>
   - **Expected:** <correct behavior>
   ```

4. **Spawn `build-lead`.** Use the Agent tool with
   `subagent_type: "build-lead"` and a prompt like:

   > Fast-path mode. Record:
   > `docs/shipflow/stories/HOTFIX-<NNNN>-<slug>.md`.
   > Description: "<description>". Target file (if given): <path>.
   > Diagnose, fix, run tests if a harness exists, append a one-line
   > `## Build log`, flip status to `done`.

5. **Report to the user:**
   - HOTFIX id + final status
   - Files touched (from the build log)
   - Test result
   - Next step: review the diff, then
     `/sf-ship --hotfix HOTFIX-<NNNN>` for a patch release.

## Hard rules

- **No Discover, no Spec, no Gate 2 or Gate 3.** Hotfix bypasses them on
  purpose. Review is manual — you eyeball the diff.
- **No Verify.** Hotfixes have no brief Success to check against; the user
  reviews the fix themselves before shipping.
- **Production-bug scope only.** If the issue isn't user-visible in prod,
  it isn't a hotfix — use `/sf-discover` or `/sf-tiny` instead.
- **One hotfix per invocation.**

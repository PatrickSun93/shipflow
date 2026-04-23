---
name: sf-security-review
description: Run a security review on one story. Spawns security-reviewer to check secrets, auth, injection, authorization, deps, data handling, and insecure defaults. Appends a `## Security review` block to the story. Advisory unless verdict is 'blocking' — which should block /sf-ship until fixed.
---

# sf-security-review

Security lens on one story.

## Arguments

- **optional:** story id (`STORY-NNNN`, `HOTFIX-NNNN`, or `TINY-NNNN`).
  If omitted, pick the newest story with `status: review` or `done`
  that doesn't already carry a `## Security review` block.

## Steps

1. **Resolve the target story.** Error out if no eligible story exists.
   All types are allowed — even trivial changes can leak secrets; a
   story in any post-build status (`review`, `done`) works.

2. **Resolve the parent brief** via the story's `brief:` frontmatter, if
   present. TINY / HOTFIX records skip this step.

3. **Spawn `security-reviewer`.** Use the Agent tool with
   `subagent_type: "security-reviewer"` and a prompt like:

   > Story: `docs/shipflow/stories/STORY-<NNNN>-<slug>.md`.
   > Brief (if any): `docs/shipflow/briefs/BRIEF-<NNN>-<slug>.md`.
   > Run the seven-pass review. Append a `## Security review` block to
   > the story per your agent prompt's contract.

4. **Verify the handoff.** Read the story back; confirm a fresh
   `## Security review` block is present with a `Verdict:` line. If
   missing, surface the gap — don't paper over.

5. **Report to the user:**
   - Story id + verdict (clean / concerns / blocking)
   - Count of follow-up items, if any
   - If `blocking`: surface the blocking items verbatim and do **not**
     recommend proceeding to `/sf-ship`
   - Next step:
     - `clean` or `concerns` — continue normal flow (`/sf-verify`,
       `/sf-ship`)
     - `blocking` — fix the flagged items, then re-run
       `/sf-security-review` on the same story

## Hard rules

- **Doesn't change story status.** Security review is advisory by
  default. `blocking` is a strong recommendation, not enforced by the
  state machine — the user decides.
- **One story per invocation.** Security review is concentrated work;
  batching dilutes focus.
- **Read narrowly.** Target story + its brief (if any) + `stack.md` +
  the source files named in the story's build log. No other briefs.

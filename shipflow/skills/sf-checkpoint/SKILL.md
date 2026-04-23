---
name: sf-checkpoint
description: Write a rich snapshot of the current session's in-flight work to docs/shipflow/sessions/checkpoint-<ts>.md. Use when Claude Code usage feels close to its cap and you want the next session to pick up cleanly.
---

# sf-checkpoint

Rich session snapshot for pause-resistant resume. Complements the
per-turn log written automatically by the `UserPromptSubmit` hook —
this skill captures **session intent** that the hook can't infer from
prompts alone.

## Arguments

None. Reads repo state + current conversation to compose.

## Steps

1. **Check for init.** If `docs/shipflow/` doesn't exist, tell the user
   to run `/sf-init` first and stop.

2. **Scan recent work.** Identify what's active — by mtime and status
   (frontmatter-only reads, no bodies):
   - Most recently touched discovery dir under `docs/shipflow/discovery/`
   - Briefs with non-final status (`draft` / `approved` / `specced`)
   - Stories in `draft` / `ready` / `in-progress` / `review`
   - Any open Gate verdicts flagged `needs-changes`

3. **Capture git state.** Run `git status --short` and
   `git diff --stat` against the working tree. Keep outputs small.

4. **Summarize session intent.** From this conversation's context
   (**you, the main Claude, have it — don't spawn a subagent that
   loses it**), compose 1–2 paragraphs covering:
   - What the user is trying to do right now (this session, not this
     phase in the abstract)
   - Decisions made so far in this session
   - Decisions still pending
   - The next step if work resumed tomorrow

5. **Write the checkpoint** at
   `docs/shipflow/sessions/checkpoint-<yyyy-mm-ddThh-mm>.md`:

   ```markdown
   ---
   ts: <iso-timestamp>
   ---

   # Checkpoint — <human-time>

   ## In flight

   - Active brief: <id + status, or "none">
   - Active story: <id + status, or "none">
   - Recent discovery dir: <slug, or "none">

   ## Session intent

   <1–2 paragraphs of what we're trying to do right now>

   ## Decisions pending

   - <bullet for each open judgment call the user hasn't answered yet>

   ## Next step if resumed

   <one sentence — which skill to run, what to focus on>

   ## Git state

   ```
   <git status --short output>
   ```
   ```

6. **Report to the user:**
   - Checkpoint path
   - One-line summary of what was captured
   - Note that the next session's SessionStart hook will surface this
     checkpoint automatically

## Hard rules

- **Don't spawn a subagent.** You (the main Claude) are the only one
  holding this session's intent. A subagent would re-read the repo and
  produce a generic summary.
- **Frontmatter-only scans** of existing briefs/stories. Don't read
  full bodies.
- **No workflow state changes.** Checkpoint is read-only apart from the
  new checkpoint file.
- **One checkpoint per invocation.** Point-in-time snapshot, not a log.

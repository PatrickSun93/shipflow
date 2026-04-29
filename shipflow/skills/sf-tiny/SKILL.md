---
name: sf-tiny
description: Fast path for trivial changes (typos, copy fixes, one-file tweaks). Skips Discover, Spec, Gate 2, and Gate 3. Creates a minimal TINY-NNNN record, spawns build-lead in tiny mode, and transitions straight to done.
---

# sf-tiny

Fire-and-forget fast path for changes too small to warrant a full brief.

## Arguments

- **required:** a short description of the fix, quoted. Example:
  `/sf-tiny "fix typo in settings page header"`.
- **optional:** target file path, if obvious. Otherwise build-lead figures
  it out.

## Steps

1. **Slug the description** — lowercase, kebab-case, ≤40 chars.

2. **Derive the next TINY id.** Scan `docs/shipflow/stories/` for
   `TINY-NNNN-*.md`, take the max NNN, add 1. Zero-pad to 4 digits.

3. **Write a minimal record** at
   `docs/shipflow/stories/TINY-<NNNN>-<slug>.md`:

   ```markdown
   ---
   id: TINY-<NNNN>
   type: tiny
   status: draft
   ---

   # <description>

   ## Goal

   <description, one line>
   ```

4. **Spawn `build-lead` (via mono).** Use the Agent tool with
   `subagent_type: "shipflow-mono"` and a prompt like:

   > Mode: build-lead. Adopt the role defined in `shipflow/agents/build-lead.md`.
   > Tiny mode. Record: `docs/shipflow/stories/TINY-<NNNN>-<slug>.md`.
   > Description: "<description>". Target file (if given): <path>.
   > Make the change. If `stack.md` names a test command, run it.
   > Append a one-line `## Build log` and flip status to `done`.

5. **Update `docs/shipflow/index.md`** — add the TINY to the Stories
   section (same section; filter is the frontmatter `type: tiny`).

6. **Report to the user:**
   - TINY id + final status
   - Files touched (from the build log)
   - Test result, if run

## Hard rules

- **No brief, no ADR, no Gate 2 or Gate 3.** This path bypasses them on
  purpose. If the change has any review-worthy surface area, use
  `/sf-discover` instead.
- **Genuinely trivial only.** Typo fixes, copy tweaks, one-file cleanups.
  If it touches more than a couple of files or has non-obvious test
  implications, it isn't tiny.
- **Tiny records still ship.** They land in the same `stories/` dir so
  the index sees them and archiving works the same way at `/sf-ship`.

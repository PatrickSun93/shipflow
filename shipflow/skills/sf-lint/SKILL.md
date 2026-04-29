---
name: sf-lint
description: Strict linter for the project-management layer. Checks frontmatter validity, dangling depends_on, orphan needs-ADR markers, broken brief↔story links, and dead links in index.md. Read-only — flags problems with file:line, doesn't fix.
---

# sf-lint

Compiler-strict pass over the workflow artifacts. Catches the kinds of
manual-edit mistakes (typos, dangling refs, status drift) that make the
state machine behave unpredictably.

## Arguments

None. Lints the entire `docs/shipflow/` tree (warm layer only — never
descends into `archive/`).

## Steps

1. **Check init.** Error out if `docs/shipflow/` doesn't exist.

2. **Run all checks below**, collecting findings as `(severity, path,
   issue)` tuples. Don't stop on first failure — collect everything,
   report once at the end.

3. **Frontmatter validity** — for every brief and story, parse the
   YAML frontmatter. Verify:
   - **Brief** `status` is one of: `draft`, `approved`, `specced`,
     `shipped`. Anything else → `error`.
   - **Story** `status` is one of: `draft`, `ready`, `in-progress`,
     `review`, `done`. (TINY/HOTFIX use the simpler `draft`/`done`.)
   - Required fields present: brief needs `id`, `slug`, `status`,
     `created`. Story needs `id`, `status` (and `brief` unless type
     is `tiny` or `hotfix`).
   - `id` matches the filename pattern (`BRIEF-<NNN>-<slug>.md`,
     `STORY-<NNNN>-<slug>.md`, etc.).

4. **Dangling `depends_on`** — for every story with a `depends_on`
   list, check each referenced id resolves to a real story file in
   `docs/shipflow/stories/`. Missing → `error`. Self-reference → `error`.
   Circular dependency (A → B → A) → `error`.

5. **Orphan `needs-ADR` markers** — find any story with a
   `<!-- needs-ADR: ... -->` comment in its `## Notes`. If the story's
   `status` is `ready`, `in-progress`, `review`, or `done` AND no
   ADR-NNN link replacement was made → `error`. (The marker should
   have been replaced by `/sf-adr` before the story could move past
   `draft`.)

6. **Brief↔story link integrity** — every story's `brief: BRIEF-NNN`
   frontmatter must resolve to an actual brief file. Missing → `error`.
   Brief frontmatter doesn't carry story refs (briefs don't list
   their stories), so this is a one-way check.

7. **`index.md` dead links** — parse `docs/shipflow/index.md`. For
   every markdown link target, verify the file exists in the warm
   layer. Links pointing to archive paths → `warning` (intentional
   archive reference is unusual but allowed). Truly missing → `error`.

8. **Verdict consistency** — sanity check verdict blocks against
   frontmatter status:
   - Brief with `## Gate 1 verdict` `approve` but `status: draft` →
     `warning` (Gate 1 should have flipped it to `approved`).
   - Story with `## Gate 3 verdict` `approve` but `status: review` →
     `warning` (Gate 3 should have flipped it to `done`).
   - Brief with `cofounder_block: true` in frontmatter and
     `status: approved` → `error` (block flag should have flipped to
     `draft`).

9. **Stale verdict / content-vs-verdict drift** — detect cases where
   the user manually edited an artifact after a verdict was written
   (the verdict no longer reflects the current content):
   - For each brief with a `## Gate 1 verdict` block: compare the
     brief's `updated` frontmatter date against the verdict block's
     mtime / date. If `updated` > verdict date → `warning: stale
     verdict — re-run /sf-check-brief`.
   - For each story with `## Gate 2 verdict`, `## Gate 3 verdict`,
     `## Verify report`, `## Security review`, `## DB review`, or
     `## Code review`: same comparison against the story's `updated`
     frontmatter or file mtime.
   - If file mtime exceeds the most recent verdict's recorded
     timestamp by > 1 hour, flag the verdict as potentially stale.
     The 1-hour buffer absorbs same-session edits to formatting.
   - Stale verdicts don't auto-block but they should be visible to
     `/sf-next` (which can pair this with the existing
     "verdict was needs-changes AND mtime > verdict mtime" rule).

10. **Report:**

   ```markdown
   # /sf-lint report — <yyyy-mm-dd hh:mm>

   ## Errors (N)
   - <path>:<line> — <issue>
   - ...

   ## Warnings (M)
   - <path>:<line> — <issue>
   - ...

   ## Summary
   - Briefs scanned: <N>
   - Stories scanned: <N>
   - ADRs scanned: <N>
   - Errors: <N>  ← non-zero blocks /sf-ship if you want strictness
   - Warnings: <M>
   ```

   If clean: `✓ No issues found.`

## Hard rules

- **Read-only.** Never write to artifacts; never auto-fix. Surface
  the issue with file:line; user fixes.
- **Warm layer only.** Don't descend into `docs/shipflow/archive/`.
- **Errors vs. warnings:** errors break the state machine (dangling
  ref, invalid status); warnings indicate drift (verdict said approve
  but status didn't update).
- **No agent spawn.** Pure file-scan + YAML-parse work. Skill does it
  directly.

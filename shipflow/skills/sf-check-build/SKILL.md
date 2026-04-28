---
name: sf-check-build
description: Advisory review after Build (Gate 3). Verifies acceptance checkboxes, runs the project test command, optionally invokes engineering:code-review, and flips approved stories from 'review' to 'done'.
---

# sf-check-build

Post-build advisory review.

## Arguments

- **optional:** story id. If omitted, review every story currently in
  `status: review`.

## Steps

1. **Collect target stories.** Either the one given, or every story with
   `status: review`. Error out if the set is empty.

2. **Read `shipflow.config.json`** to determine `gate_modes.gate_3`
   (`advisory` or `block`).

3. **For each story, check three things:**

   - **Acceptance checkboxes.** Every box in `## Acceptance criteria` must
     be checked. Any unchecked → `needs-changes`.
   - **Tests.** Run the project test command (named in `stack.md`, or
     inferred from `package.json` scripts / `Makefile`). Any failure →
     `needs-changes`. No test harness → record `no-harness` (not a fail).
   - **Code review.** If the `engineering:code-review` skill is available,
     invoke it against the story's diff. Skip silently if it isn't
     installed. Findings don't auto-fail — they inform the verdict.

4. **Scan the build log for cross-cutting review signals** (don't run
   the reviews yourself — just flag whether they're recommended):
   - **Data signals**: build log mentions files under `migrations/`,
     `prisma/`, `schema.`, `*.sql`, `models/`, `db/`, `database/`, or
     ORM model files → recommend `/sf-db-review`
   - **Security signals**: build log mentions `auth/`, `*auth*`,
     `*login*`, `*password*`, `*token*`, `*session*`, `middleware/`,
     or any user-input-facing route handler → recommend
     `/sf-security-review`
   - These are recommendations only — not blocking. Solo dev decides.

5. **Append a `## Gate 3 verdict`** block to each story:

   ```markdown
   ## Gate 3 verdict

   **Verdict: <approve | needs-changes>** (mode: <advisory|block>)

   - Acceptance: <pass | N unchecked>
   - Tests: <green | red | no-harness>
   - Code review: <clean | N findings | not run>
   - Cross-cutting reviews recommended: <`/sf-db-review` | `/sf-security-review` | both | none>
   ```

5. **Update each story's frontmatter status:**
   - `approve` → `status: done`
   - `needs-changes` → keep `status: review`; in `block` mode also warn
     the user this blocks `/sf-ship`

6. **Report to the user:**
   - Per-story verdict summary
   - Stories now `done` vs. still `review`
   - Next step: `/sf-verify` for any `done` story with user-facing intent;
     otherwise continue building via `/sf-build`

## Hard rules

- **Acceptance criteria are the bar.** If a box is unchecked, that's a
  `needs-changes` — don't guess intent.
- **Don't rewrite stories.** Append the verdict block, flip status. That's
  the entire footprint.
- **Don't manufacture findings.** Clean is valid.
- **Read narrowly.** Target stories + `stack.md` + the working tree (for
  tests). No other briefs, no archive.

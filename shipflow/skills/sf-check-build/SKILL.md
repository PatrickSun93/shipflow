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
   - **Code review.** Spawn `code-reviewer` (via mono) using
     `subagent_type: "shipflow-mono"` with prompt prefix
     `Mode: code-reviewer. Adopt the role defined in shipflow/agents/code-reviewer.md.`
     Findings inform the verdict but don't auto-fail unless the agent
     returns `Verdict: blocking`.

4. **Scan the build log for cross-cutting review signals** (don't run
   the reviews yourself — just flag whether they're recommended). Use
   **strong signals only** to avoid noise on stories where the review
   would be low-value:

   - **Data signals (strong)**: build log mentions any of
     `migrations/**`, `**/migrations/**`, `schema.prisma`, `schema.sql`,
     `*.schema.{prisma,sql}`, raw `*.sql` files at repo root → recommend
     `/sf-db-review`
   - **Security signals (strong)**: build log mentions any of `auth/**`,
     `lib/auth/**`, `src/auth/**`, files literally named `*password*` or
     `*credential*`, `**/middleware/auth*`, `**/middleware/*csrf*`,
     `**/middleware/*cors*`, or new login/signup route handlers →
     recommend `/sf-security-review`
   - **Skip weak signals** — generic `models/`, `db/`, `*token*`,
     `*session*`, `middleware/` without an auth/csrf/cors qualifier
     produce too many false positives. The user can still run reviews
     manually if their judgment says so.

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

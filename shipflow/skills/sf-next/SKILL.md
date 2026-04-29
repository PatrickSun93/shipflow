---
name: sf-next
description: Detect the current ShipFlow state from the repo (brief/story statuses, discovery artifacts, gate verdicts) and run the next appropriate phase skill automatically. Use instead of tracking which command comes next manually.
---

# sf-next

Figure out where the workflow is and run what comes next.

## Arguments

None. State comes from the repo itself.

## Steps

1. **Check for init.** If `docs/shipflow/` doesn't exist, tell the user
   to run `/sf-init` first and stop.

2. **Scan state** (all frontmatter-only — don't read bodies):
   - Discovery dirs under `docs/shipflow/discovery/` — note which have
     `questions.md` but no `answers.md` (user-blocked), vs. have
     `answers.md` but no matching brief (ready for synthesis).
   - Briefs under `docs/shipflow/briefs/` — collect by `status:`
     (`draft`, `approved`, `specced`, `shipped`).
   - Stories under `docs/shipflow/stories/` — collect by `status:` and
     by `brief:` parent. Note any `## Verify report`, `## Security
     review`, or `## DB review` blocks present.
   - Latest gate verdicts on the most recent live brief.
   - For stories in `review` or `done` status, scan their `## Build log`
     for **strong path signals** that suggest cross-cutting reviews
     (weak signals like generic `models/` produce false positives —
     skip them):
     - Data signals: `migrations/**`, `**/migrations/**`, `schema.prisma`,
       `schema.sql`, `*.schema.{prisma,sql}`, raw `*.sql` at repo root
     - Security signals: `auth/**`, `lib/auth/**`, `src/auth/**`,
       `*password*`, `*credential*`, `**/middleware/auth*`,
       `**/middleware/*csrf*`, `**/middleware/*cors*`, new login /
       signup route handlers

3. **Pre-step: pick the live brief.** A "live brief" is one with
   `status` in `{draft, approved, specced}` (not `shipped`). Sort
   live briefs by `updated` descending. Cases:
   - **0 live briefs**: skip brief-related rows, jump to TINY/HOTFIX
     or idle.
   - **1 live brief**: that's the target.
   - **2+ live briefs**: surface them all to the user with one-line
     status summaries, ask which to advance. Don't auto-pick. (Hard
     rule: don't guess at scope.)

4. **Decide the next step** using this priority (stop at first match).
   Rows are evaluated against the live brief from step 3 (when it
   exists) plus any TINY/HOTFIX records (which are brief-less):

   | State | Next step | Auto-run? |
   |---|---|---|
   | Discovery dir with `questions.md` but no `answers.md` | Remind user to answer, then `/sf-brief` | **No** — user input needed |
   | Discovery dir with `answers.md` but no matching brief | `/sf-brief` | Yes |
   | Brief `status: draft`, no `## Gate 1 verdict` | `/sf-check-brief` | Yes |
   | Brief `status: draft`, last Gate 1 verdict was `needs-changes` / `reject` AND brief mtime > verdict mtime (user revised) | `/sf-check-brief` (re-run on revised brief) | Yes |
   | Brief `status: draft`, last Gate 1 verdict was `needs-changes` / `reject` AND brief unchanged | Surface the verdict, ask user to revise | **No** |
   | Brief `status: approved`, no stories link to it | `/sf-spec` | Yes |
   | Stories `status: draft`, brief `status: specced`, no Gate 2 verdicts on them | `/sf-check-plan` | Yes |
   | Story `status: draft`, last Gate 2 verdict was `needs-changes` / `reject` AND story mtime > verdict mtime (user revised) | `/sf-check-plan` (re-run on that story) | Yes |
   | Any story has `<!-- needs-ADR: ... -->` marker and no ADR link yet | `/sf-adr <STORY-id>` (pick the earliest) | **No** — user picks which to tackle first |
   | Story `status: ready`, all `depends_on` `done` | `/sf-build` | Yes |
   | Story `status: review`, no Gate 3 verdict | `/sf-check-build` | Yes |
   | Story `status: done`, build log shows **data signals**, no `## DB review` | Suggest `/sf-db-review` before `/sf-verify` | **No** — user decides whether DB risk merits the review |
   | Story `status: done`, build log shows **security signals**, no `## Security review` | Suggest `/sf-security-review` before `/sf-verify` | **No** — same |
   | Story `status: done`, no `## Verify report` | `/sf-verify` | Yes |
   | **TINY** record (`type: tiny`) `status: draft` | Remind user this is a fast-path; recommend `/sf-tiny` if the description came from them, or `/sf-build` to implement directly | **No** — user-context-dependent |
   | **HOTFIX** record (`type: hotfix`) `status: draft` | Same as TINY, but biased toward `/sf-build` (hotfix is emergency) | **No** |
   | TINY or HOTFIX `status: done`, no release | Recommend `/sf-ship --hotfix <id>` if hotfix; else continue (TINY rides next regular ship) | **No** |
   | Live brief has stories in **mixed** statuses (e.g. some `done`, some `ready`, some `draft`), brief `status: specced` | Continue building the next eligible `ready` story (highest-priority match in this same table); after each `/sf-build`, re-run `/sf-next` | Yes |
   | All stories under live brief `done`, no Gate 4 verdict | `/sf-check-ship` | Yes |
   | All stories `done`, Gate 4 `approve`, brief not `shipped` | `/sf-ship` | **No** — shipping is user-driven |
   | Brief `shipped` but `index.md` mtime older than any story/brief/ADR | `/sf-regen-index` | Yes |
   | None of the above | Report "workflow idle" with a one-line state summary; suggest `/sf-discover "<idea>"` for new work | — |

5. **When auto-run is Yes**, invoke the resolved skill via the Skill
   tool with any defaults the skill itself supports. Pass through the
   target slug / story id the scan surfaced.

6. **When auto-run is No**, report to the user:
   - Current state (one line)
   - The recommended next command
   - Why it's not auto-running (user input needed / judgment call / etc.)

## Hard rules

- **Never skip a phase.** If Gate 1 was never run and the brief is
  `draft`, don't jump to `/sf-spec` even if the user asks.
- **Never auto-run `/sf-ship`.** Shipping touches git and release notes;
  the user makes that call explicitly.
- **Never auto-run `/sf-adr`.** The user picks which flagged story to
  unblock first.
- **Don't guess at scope.** If the state table doesn't cover a situation
  (e.g. multiple live briefs), surface the ambiguity and let the user
  pick.
- **Read narrowly.** Frontmatter scans only — no body reads. No
  archive access.

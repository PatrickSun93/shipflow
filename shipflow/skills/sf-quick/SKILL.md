---
name: sf-quick
description: Mid-tier fast path for existing projects. Skips Discover and Spec ceremony — generates a minimal brief + 1-3 ready-to-build stories inline (no subagent fanout) from a one-line description. Use when you already know the scope and don't need 18 persona questions.
---

# sf-quick

Mid-tier fast path: between `/sf-tiny` (one-file trivial change) and the
full `/sf-discover → /sf-brief → /sf-spec` flow. **For existing
projects** where you already understand the codebase, the user, and
the constraints — and just want to ship a feature or fix.

## When to use which size

| Path | When | Skips |
|---|---|---|
| `/sf-tiny "<fix>"` | One-file trivial (typo, copy fix) | Discover, Spec, all gates |
| `/sf-hotfix "<bug>"` | Production bug, emergency | Discover, Spec |
| **`/sf-quick "<feature or fix>"`** | **Mid-tier feature on existing project; you know the scope** | **Discover, Spec ceremony** |
| `/sf-discover "<idea>"` → ... | Greenfield product, big bet, unclear scope | nothing — full flow |

## Arguments

- **required:** description of the feature / fix / refactor in quotes.
  Example: `/sf-quick "fix sortorder=9 wrongly assigned to LB variants in autoscoreai.js:1159"`.
- **optional:** `--type [bug|feature|refactor]`. Default: `feature`.
  Affects brief framing — `bug` adds a regression-test acceptance box,
  `refactor` flags "no behavior change" in Success.

## Steps

1. **Check init.** If `docs/shipflow/` doesn't exist, error out.

2. **Slug the description.** kebab-case, ≤40 chars.

3. **Derive next BRIEF id.** Scan `docs/shipflow/briefs/` for the max
   `BRIEF-NNN`, add 1, zero-pad.

4. **Read context inline** (no subagent spawn — `/sf-quick` is pure
   skill work for token efficiency):
   - `docs/shipflow/stack.md` — tech stack + conventions
   - `docs/shipflow/index.md` — recent shipping cadence
   - 1–2 most recent release notes for trajectory
   - For `bug` or `refactor` types referencing specific files:
     read those files to ground the brief in actual code

5. **Write a minimal brief** at `docs/shipflow/briefs/BRIEF-<NNN>-<slug>.md`:

   ```markdown
   ---
   id: BRIEF-<NNN>
   slug: <slug>
   status: approved
   type: quick
   created: <yyyy-mm-dd>
   updated: <yyyy-mm-dd>
   ---

   # <Title>

   ## Goal
   <2–3 sentences. State the actual change. For bugs, name the failure
   mode + the file:line if known. For features, state the user-visible
   delta. Don't pad.>

   ## Constraints
   <Pulled from stack.md + obvious from the description. 2–4 bullets max.>

   ## Success
   <Observable outcome. For bugs: "X no longer happens; regression test
   covers it." For features: "Y works for users; tests cover happy + 1
   edge case." For refactors: "Behavior unchanged; tests still green;
   <metric> improved.">

   ## Notes
   _Generated via `/sf-quick` — bypassed full Discover / Spec ceremony.
   If the change turns out to be bigger than expected, escalate to a
   full brief via `/sf-discover` and link back here._
   ```

   Set `status: approved` directly so `/sf-build` (or `/sf-spec`) can
   run without first passing Gate 1.

6. **Generate 1–3 stories** inline, each at
   `docs/shipflow/stories/STORY-<NNNN>-<short-slug>.md`:

   - frontmatter: `id`, `brief: BRIEF-<NNN>`, `status: ready`, `size`,
     `depends_on` (chain across the 1–3 stories if multi-story)
   - `## Goal` — one sentence
   - `## Acceptance criteria` — 2–4 boxes, every box testable
   - For `--type bug`: include an explicit "regression test added that
     reproduces the failure when reverted" acceptance box
   - For `--type refactor`: include "behavior unchanged; existing tests
     still pass" acceptance box
   - `## Notes` — implementation hints + file:line references when known

7. **Update `docs/shipflow/index.md`** — add the brief + stories.

8. **Report to the user:**
   - Brief id + path
   - Story ids in dependency order
   - One-line: "Skipped: Discover, Brief synthesis (no challenger),
     Gate 1, Spec phase, Gate 2."
   - Next step: `/sf-build` to start the first story, or
     `/sf-build --all` to sweep all eligible stories
   - Optional: "Run `/sf-cofounder-review` if you want a strategic
     sanity check on the bet — `/sf-quick` skipped it by design."

## Hard rules

- **Existing project only.** `/sf-quick` assumes you already have
  context — codebase familiarity, user understanding, stack
  conventions in `stack.md`. Don't use for greenfield products; they
  need Discover.
- **One brief per invocation.** Don't batch multiple unrelated changes.
- **Don't elaborate the brief.** If the description is one sentence,
  the brief is one paragraph per section. No padding.
- **Don't auto-skip downstream gates.** `/sf-quick` only skips Discover
  + Spec ceremony. Build → Gate 3 → Verify → Gate 4 → Ship still apply
  (you can configure them as advisory, but don't bypass them by default).
- **No subagent fanout.** Skill does the brief + story generation
  inline. Spawning 4 personas for a `/sf-quick` would defeat the
  purpose.
- **Read narrowly.** `stack.md` + recent index/releases + source files
  named in the description. No archive, no unrelated briefs.
- **If scope balloons, escalate.** When generating, if you find
  yourself wanting to write more than 3 stories or constraints exceed
  4 bullets, stop and tell the user "this is bigger than `/sf-quick`
  — consider `/sf-discover` for a real brief instead."

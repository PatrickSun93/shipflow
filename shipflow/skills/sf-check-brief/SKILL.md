---
name: sf-check-brief
description: Advisory review before Spec phase (Gate 1). Spawns product-lead + tech-lead in parallel, each writes a gate-1-review-<role>.md breadcrumb, then classifies a single verdict and appends it to the brief.
---

# sf-check-brief

Advisory review between Discover and Spec.

## Arguments

- **optional:** slug. If omitted, pick the most recent brief with
  `status: draft` in its frontmatter.

## Steps

1. **Resolve the target brief** at `docs/shipflow/briefs/BRIEF-<NNN>-<slug>.md`.
   Error out if no draft brief exists.

2. **Read `shipflow.config.json`** to determine `gate_modes.gate_1`
   (`advisory` or `block`).

3. **Spawn both reviewers in parallel (single message, two Agent calls):**

   - `product-lead` — prompt:
     > Gate 1 review. Brief: `docs/shipflow/briefs/BRIEF-<NNN>-<slug>.md`.
     > Write verdict to `docs/shipflow/discovery/<slug>/gate-1-review-product-lead.md`.
     > First line: `Verdict: approve` (or `needs-changes` or `reject`). Then reasons.

   - `tech-lead` — prompt:
     > Gate 1 review. Brief: `docs/shipflow/briefs/BRIEF-<NNN>-<slug>.md`.
     > Write verdict to `docs/shipflow/discovery/<slug>/gate-1-review-tech-lead.md`.
     > First line: `Verdict: approve` (or `needs-changes` or `reject`). Then reasons.

4. **After both return**, read both review files. Parse the `Verdict:` line from each.

5. **Classify the overall verdict:**
   - Both `approve` → `approve`
   - Any `reject` → `reject`
   - Otherwise → `needs-changes`

6. **Append a verdict block** to the brief (at the very end):
   ```markdown

   ## Gate 1 verdict

   **Overall: <verdict>** (mode: <advisory|block>)

   - product-lead: <their verdict> — <first reason, one line>
   - tech-lead: <their verdict> — <first reason, one line>

   Full reviews: `docs/shipflow/discovery/<slug>/gate-1-review-*.md`.
   ```

7. **Update the brief's frontmatter** `status` field:
   - If overall `approve` → `approved` regardless of mode.
   - If overall `needs-changes`:
     - advisory → remain `draft`, warn the user
     - block → remain `draft`, block progression
   - If overall `reject`:
     - advisory → remain `draft`, strong warning
     - block → remain `draft`, block progression

   Update the `updated` field to today.

8. **Report to the user** with verdict, mode, and next step (`/sf-spec` if approved).

## Hard rules

- **Don't manufacture problems.** If both reviewers return `approve`, the verdict is `approve`. Full stop.
- **Don't rewrite the brief.** The skill appends a verdict; the brief body is the author's (or their next revision's).
- **Review files stay put.** They're breadcrumbs. They travel with the brief through archiving.
- **Read narrowly.** Only the target brief, the two fresh review files, and `shipflow.config.json`.

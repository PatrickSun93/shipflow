---
name: sf-brief
description: Synthesize a ShipFlow brief from the user's discovery answers after /sf-discover. Assembles BRIEF-NNN-<slug>.md from per-persona slices and runs the challenger on the result.
---

# sf-brief

Turn a completed discovery dialogue into a brief.

## Arguments

- **optional:** slug. If omitted, pick the most recent discovery dir under
  `docs/shipflow/discovery/` that has `questions.md` but no `answers.md`.

## Steps

1. **Resolve the target discovery dir.** Error out if none is found.

2. **Write `answers.md` verbatim.** The user's previous message contained the
   answers. Save that message's text exactly, in an `answers.md` under the
   discovery dir. Don't summarize, rephrase, or reorder.

3. **Detect whether a domain expert was active.** Look in the discovery
   dir for any `dialogue-<domain>.md` file beyond the 3 base personas
   (education / fintech / healthcare / ecommerce / devtools / social).
   If one exists, include its expert in the synthesis spawn — its slug
   is the one written to `dialogue.md`'s `_Domain: <name>_` line.

4. **Spawn 3 or 4 personas in parallel (single message).** Each uses the
   persona's `subagent_type` with a synthesis-mode prompt:

   - `discovery-tech-persona` — prompt:
     > Synthesis mode. Working dir: `docs/shipflow/discovery/<slug>/`.
     > Read `seed.md`, `dialogue-tech.md`, `answers.md`.
     > Write `slice-tech.md` with `## Constraints` and `## Risks`.

   - `discovery-ux-persona` — prompt:
     > Synthesis mode. Working dir: `docs/shipflow/discovery/<slug>/`.
     > Read `seed.md`, `dialogue-ux.md`, `answers.md`.
     > Write `slice-ux.md` with `## Who` and `## Open questions`.

   - `discovery-business-persona` — prompt:
     > Synthesis mode. Working dir: `docs/shipflow/discovery/<slug>/`.
     > Read `seed.md`, `dialogue-business.md`, `answers.md`.
     > Write `slice-business.md` with `## Why now`, `## Success`, `## Non-goals`.

   - (optional, only if domain expert is active) `<domain>-expert`:
     > Synthesis mode. Working dir: `docs/shipflow/discovery/<slug>/`.
     > Read `seed.md`, `dialogue-<domain>.md`, `answers.md`.
     > Write `slice-<domain>.md` per your agent prompt's contract.

5. **Derive the next brief id.** Scan `docs/shipflow/briefs/` for existing
   `BRIEF-NNN-*.md` filenames, take the max NNN, add 1. Zero-pad to 3 digits.

6. **Assemble the brief** at `docs/shipflow/briefs/BRIEF-<NNN>-<slug>.md` using
   `references/brief-template.md`:
   - Fill frontmatter: `id`, `slug`, `status: draft`, `created`, `updated`.
   - Derive a title from the slug (title-case with spaces).
   - **Problem** section: write a 2–5 sentence distillation of `seed.md` and
     `answers.md`. Stay close to the user's words.
   - **Who**, **Open questions** ← `slice-ux.md`
   - **Why now**, **Success**, **Non-goals** ← `slice-business.md`
   - **Constraints**, **Risks** ← `slice-tech.md`
   - **Domain section** (only if a domain expert was active) — copy the
     `## Pedagogy` / `## Compliance & regulation` / `## Clinical & compliance`
     / `## Checkout & conversion` / `## DX` / `## Trust & safety` section from
     `slice-<domain>.md` verbatim, placed after Risks and before Unresolved.
   - **Unresolved** section: if any slice contained a `## Unresolved` block,
     collect all (3 or 4) into a single `## Unresolved` block in the brief.
     If none, omit the section.

7. **Update `docs/shipflow/index.md`** by adding the new brief to the Briefs section.

8. **Spawn the challenger.** Use the Agent tool with `subagent_type: "challenger"`
   and a prompt like:

   > Working directory: `docs/shipflow/discovery/<slug>/`.
   > Brief path: `docs/shipflow/briefs/BRIEF-<NNN>-<slug>.md`.
   > Read seed, answers, and the brief. Run your challenge loop (soft cap —
   > stop when further pressing would be theater). Write `open-questions.md`
   > in the discovery dir. Report back with the count of unresolved questions.

9. **Report to the user:**
   - Brief path
   - Number of unresolved flags (if any)
   - Number of open challenges from the challenger + path to `open-questions.md`
     (skip this line if challenger found none)
   - Next step: review `open-questions.md` if present, then `/sf-check-brief`

## Hard rules

- **Read narrowly.** Only the target discovery dir and `docs/shipflow/briefs/`
  (to compute the next id). Never read other briefs' contents.
- **Don't second-guess the slices.** If a persona synthesized something surprising,
  preserve it. Contradictions go to `## Unresolved`, not to rewrites.
- **Don't run Gate 1.** That's a separate skill.

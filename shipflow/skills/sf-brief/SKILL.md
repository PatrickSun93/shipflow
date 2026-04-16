---
name: sf-brief
description: Synthesize a ShipFlow brief from the user's discovery answers. Writes answers.md verbatim, spawns the three personas in synthesis mode in parallel, and stitches their slices into docs/shipflow/briefs/BRIEF-NNN-<slug>.md.
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

3. **Spawn the three personas in parallel (single message, three Agent calls).**
   Each call uses the persona's `subagent_type` with a synthesis-mode prompt:

   - `discovery-tech-persona` — prompt:
     > Synthesis mode. Working dir: `docs/shipflow/discovery/<slug>/`.
     > Read `seed.md`, `dialogue-tech.md`, `answers.md`.
     > Write `slice-tech.md` with the `## Constraints` and `## Risks` sections.

   - `discovery-ux-persona` — prompt:
     > Synthesis mode. Working dir: `docs/shipflow/discovery/<slug>/`.
     > Read `seed.md`, `dialogue-ux.md`, `answers.md`.
     > Write `slice-ux.md` with the `## Who` and `## Open questions` sections.

   - `discovery-business-persona` — prompt:
     > Synthesis mode. Working dir: `docs/shipflow/discovery/<slug>/`.
     > Read `seed.md`, `dialogue-business.md`, `answers.md`.
     > Write `slice-business.md` with the `## Why now`, `## Success`, and `## Non-goals` sections.

4. **Derive the next brief id.** Scan `docs/shipflow/briefs/` for existing
   `BRIEF-NNN-*.md` filenames, take the max NNN, add 1. Zero-pad to 3 digits.

5. **Assemble the brief** at `docs/shipflow/briefs/BRIEF-<NNN>-<slug>.md` using
   `references/brief-template.md`:
   - Fill frontmatter: `id`, `slug`, `status: draft`, `created`, `updated`.
   - Derive a title from the slug (title-case with spaces).
   - **Problem** section: write a 2–5 sentence distillation of `seed.md` and
     `answers.md`. Stay close to the user's words.
   - **Who**, **Open questions** ← `slice-ux.md`
   - **Why now**, **Success**, **Non-goals** ← `slice-business.md`
   - **Constraints**, **Risks** ← `slice-tech.md`
   - **Unresolved** section: if any slice contained a `## Unresolved` block,
     collect all three into a single `## Unresolved` block in the brief.
     If none, omit the section.

6. **Update `docs/shipflow/index.md`** by adding the new brief to the Briefs section.

7. **Report to the user:**
   - Brief path
   - Number of unresolved flags (if any)
   - Next step: `/sf-gate-1`

## Hard rules

- **Read narrowly.** Only the target discovery dir and `docs/shipflow/briefs/`
  (to compute the next id). Never read other briefs' contents.
- **Don't second-guess the slices.** If a persona synthesized something surprising,
  preserve it. Contradictions go to `## Unresolved`, not to rewrites.
- **Don't run Gate 1.** That's a separate skill.

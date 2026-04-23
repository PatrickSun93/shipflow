---
name: sf-adr
description: Author one ADR for a story that spec-author flagged needs-ADR. Spawns tech-lead to draft docs/shipflow/decisions/ADR-NNN-<slug>.md using the ADR template. Replaces the needs-ADR marker in the story with a link to the new ADR.
---

# sf-adr

Draft one ADR to unblock a flagged story.

## Arguments

- **required:** story id (e.g. `STORY-0012`). The story must carry a
  `<!-- needs-ADR: reason -->` marker in its `## Notes`.

## Steps

1. **Resolve the story** at `docs/shipflow/stories/STORY-<NNNN>-<slug>.md`.
   Error out if not found or if it lacks the `needs-ADR` marker.

2. **Derive the next ADR id.** Scan `docs/shipflow/decisions/` for existing
   `ADR-NNN-*.md` filenames, take the max NNN, add 1. Zero-pad to 3 digits.

3. **Derive a slug for the ADR** from the needs-ADR reason text (kebab-case,
   ≤40 chars, trimmed at word boundary).

4. **Spawn `tech-lead`.** Use the Agent tool with
   `subagent_type: "tech-lead"` and a prompt like:

   > ADR draft. Story: `docs/shipflow/stories/STORY-<NNNN>-<slug>.md`.
   > Parent brief: `docs/shipflow/briefs/BRIEF-<NNN>-<slug>.md`.
   > Reason flagged: "<reason from the marker>".
   > Write `docs/shipflow/decisions/ADR-<NNN>-<adr-slug>.md` using
   > `references/adr-template.md`. Real alternatives only. Keep it tight.

5. **Update the story's `## Notes`:** remove the
   `<!-- needs-ADR: ... -->` marker and add a bullet
   `- ADR: ADR-<NNN> (<adr-slug>)` in its place.

6. **Update `docs/shipflow/index.md`** — add the new ADR to the ADRs section.

7. **Report to the user:**
   - ADR path written
   - Story unblocked
   - Next step: if more stories carry `needs-ADR`, run `/sf-adr <next-id>`;
     otherwise `/sf-check-plan` or `/sf-build`.

## Hard rules

- **One ADR per invocation.** Batching ADRs muddles decisions.
- **Don't rewrite the story.** Only replace the `needs-ADR` marker with the
  ADR link bullet.
- **Read narrowly.** Target story + its parent brief + `stack.md` + ADR
  filenames (to compute next id). No other stories, no archive.

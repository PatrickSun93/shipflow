---
name: sf-spec
description: Translate an approved brief into 5–10 stories under docs/shipflow/stories/. Spawns spec-author, which slices the brief by dependency, then updates the index. Flags which stories need /sf-adr before /sf-build.
---

# sf-spec

Turn an approved brief into a working set of stories.

## Arguments

- **optional:** slug. If omitted, pick the most recent brief with
  `status: approved` in its frontmatter.

## Steps

1. **Resolve the target brief.** Default: the newest `approved` brief under
   `docs/shipflow/briefs/`. Error out if none exists — Spec needs an approved
   brief.

2. **Spawn `spec-author`.** Use the Agent tool with
   `subagent_type: "spec-author"` and a prompt like:

   > Brief: `docs/shipflow/briefs/BRIEF-<NNN>-<slug>.md`.
   > Slice it into 5–10 stories under `docs/shipflow/stories/` using
   > `references/story-template.md`. Link each back with
   > `brief: BRIEF-<NNN>` in frontmatter. Flag any story that needs an ADR
   > before Build with `<!-- needs-ADR: reason -->` in `## Notes`. Report
   > the story ids in dependency order and any ADR flags.

3. **Collect the result.** Parse the agent's response for STORY ids and
   needs-ADR flags. If incomplete, scan the written files to fill in.

4. **Update `docs/shipflow/index.md`** — add the new stories to the Stories
   section. Preserve the `<!-- Auto-regenerated -->` comment.

5. **Update the brief's frontmatter:** set `status: specced` and bump
   `updated` to today.

6. **Report to the user:**
   - Count of stories written + their ids in dependency order
   - Any stories flagged needs-ADR + the reasons
   - Next step:
     - If any needs-ADR → run `/sf-adr <STORY-id>` for each
     - Else → `/sf-check-plan` for advisory review, then `/sf-build`

## Hard rules

- **One `approved` brief per invocation.** Don't batch briefs.
- **Don't write stories yourself.** The agent writes them; the skill
  coordinates and reports.
- **Don't run Gate 2 or Build.** Those are separate skills.
- **Read narrowly.** Only the target brief, story filenames (to compute the
  next id), `stack.md`, and `index.md`.

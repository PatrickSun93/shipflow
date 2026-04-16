---
name: sf-init
description: Initialize ShipFlow in the current repo. Creates docs/shipflow/ directory tree, writes shipflow.config.json, and seeds CLAUDE.md using the plugin's template. Run once per project. Supports --overwrite and --append flags.
---

# sf-init

One-time repo setup for ShipFlow.

## Flags

- `--overwrite` — if `CLAUDE.md` exists, back it up to `CLAUDE.md.pre-shipflow` and overwrite with the template. Safe: the backup is kept.
- `--append` — force append mode even if `CLAUDE.md` is empty or a placeholder.

Default behavior: smart. Empty or placeholder `CLAUDE.md` → overwrite in place.
Real content → append a delimited ShipFlow section.

## Steps

1. **Check for prior init.** If `docs/shipflow/` exists, tell the user ShipFlow
   is already initialized and stop. Don't re-initialize silently.

2. **Create the directory tree:**
   ```
   docs/shipflow/
     briefs/           .gitkeep
     stories/          .gitkeep
     decisions/        .gitkeep
     releases/         .gitkeep
     retros/           .gitkeep
     discovery/        .gitkeep
     diaries/          .gitkeep   (agent-only memory, see §"Diaries" below)
     sessions/         .gitkeep   (written by Stop + PreCompact hooks)
     archive/
       briefs/         .gitkeep
       stories/        .gitkeep
       decisions/      .gitkeep
   ```

3. **Write `docs/shipflow/index.md`** with empty sections: Briefs, Stories, ADRs, Releases.
   Include the comment `<!-- Auto-regenerated. Edit shipflow.config.json to change cadence. -->`.

4. **Write `docs/shipflow/stack.md`** as a stub (one paragraph: "Describe your stack here").

5. **Write `shipflow.config.json`:**
   ```json
   {
     "gate_modes": {
       "gate_1": "advisory",
       "gate_2": "advisory",
       "gate_3": "advisory",
       "gate_4": "advisory"
     },
     "index_regen_every_n_stories": 5,
     "archive_on_ship": true
   }
   ```

6. **Handle `CLAUDE.md`:**
   - Read the template from `${CLAUDE_PLUGIN_ROOT}/references/claude-md-template.md`.
   - Substitute `{{project_name}}` with the basename of the current directory.
   - Decide mode:
     - `--overwrite` flag → back up existing `CLAUDE.md` to `CLAUDE.md.pre-shipflow`, then write template. If no existing `CLAUDE.md`, just write.
     - `--append` flag → append template body (between `SHIPFLOW:BEGIN`/`SHIPFLOW:END` markers) to existing `CLAUDE.md`.
     - Default:
       - File missing, empty, or only contains placeholders like `# TODO` / `# Project` (≤5 lines, no headings below H1) → write template.
       - Otherwise → append template body under the markers. Preserve existing content.
   - If markers already exist in the file, update the content between them rather than appending a second copy.

7. **Confirm to the user** with:
   - Files created (list)
   - Whether `CLAUDE.md` was overwritten, appended, or created
   - Backup path if `--overwrite` was used
   - Next step: `/sf-discover "<your first idea>"`

## Hard rules

- Never silently clobber `CLAUDE.md` without a backup. `--overwrite` writes `.pre-shipflow` first.
- Never create files outside `docs/shipflow/`, `CLAUDE.md`, and `shipflow.config.json`.
- If the repo has a productivity-plugin CLAUDE.md marker, preserve that section (see open question #1 in handoff).

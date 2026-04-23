---
name: sf-ship
description: Cut a release for a brief whose stories are all done, or for a HOTFIX record as a patch. Spawns release-manager to write the release note and archive the brief + stories. Run after /sf-gate-4 on the normal flow.
---

# sf-ship

Ship a brief's completed work as a release.

## Arguments

- **optional:** slug. If omitted, pick the newest brief where every linked
  story is `status: done`.
- **optional:** `--version X.Y.Z`. If omitted, bump the minor from the
  last release in `docs/shipflow/releases/` (or `v0.1.0` on first ship).
- **optional:** `--hotfix <HOTFIX-id>`. Ships a single hotfix record as a
  patch release instead of a full brief.

## Steps

1. **Resolve the target.**
   - Normal mode: find the target brief; confirm every story linked to it
     has `status: done`. Error out if any story is still in flight.
   - Hotfix mode: resolve the `HOTFIX-NNNN` record; confirm `status: done`.

2. **Read `shipflow.config.json`** for `archive_on_ship`. Pass the value
   through to release-manager.

3. **Derive the version:**
   - Normal mode: if `--version` is given, use it; else bump the minor
     from the newest release in `releases/` (e.g. `v0.3.0 → v0.4.0`).
   - Hotfix mode: bump the patch (`v0.3.0 → v0.3.1`), unless `--version`
     overrides.

4. **Spawn `release-manager`.** Use the Agent tool with
   `subagent_type: "release-manager"` and a prompt like:

   > Brief: `docs/shipflow/briefs/BRIEF-<NNN>-<slug>.md` (or hotfix record
   > path in hotfix mode). Version: `<version>`.
   > `archive_on_ship: <true|false>`.
   > Write the release note, archive per config, report back.

5. **Report to the user:**
   - Version shipped + release note path
   - Stories archived (or skipped archive if config disabled)
   - Next step: run `/sf-regen-index` to refresh the warm index (a brief
     just left), then tag / push in git if appropriate.

## Hard rules

- **One release per invocation.**
- **All stories must be `done`.** No ship with stories in `review` or
  `ready`. If Gate 4 is configured `block`, re-run it first.
- **Never tag, push, or publish.** The skill writes markdown and moves
  files; git and deploy operations stay in the user's hands.
- **Read narrowly.** Target brief + its stories + `stack.md` + release
  filenames (for version derivation). No unrelated briefs.

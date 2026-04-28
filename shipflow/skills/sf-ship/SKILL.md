---
name: sf-ship
description: Cut a release for a brief whose stories are all done, or for a HOTFIX record as a patch. Spawns release-manager to write the release note and archive the brief + stories. Run after /sf-check-ship on the normal flow.
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
- **optional:** `--force-risk-acknowledged`. Override hard-fail when a
  cross-cutting review (security or DB) returned `Verdict: blocking`.
  User explicitly accepts the risk in writing.

## Steps

1. **Resolve the target.**
   - Normal mode: find the target brief; confirm every story linked to it
     has `status: done`. Error out if any story is still in flight.
   - Hotfix mode: resolve the `HOTFIX-NNNN` record; confirm `status: done`.

2. **Hard-fail on blocking cross-cutting reviews.** Scan every linked
   story for `## Security review` or `## DB review` blocks. If any
   carries `Verdict: blocking`:
   - Without `--force-risk-acknowledged`: abort. Surface the blocking
     finding(s) verbatim and tell the user to either fix or pass the
     override flag.
   - With `--force-risk-acknowledged`: proceed but record the override
     in the release note's `## Notes` section ("Shipped with overridden
     blocking review on STORY-NNNN: <one-line summary>").
   - Hotfix mode is exempt from this check (hotfixes are emergency by
     definition; blocking concerns get fixed in the next regular brief).

3. **Read `shipflow.config.json`** for `archive_on_ship`. Pass the value
   through to release-manager.

4. **Derive the version:**
   - Normal mode: if `--version` is given, use it; else bump the minor
     from the newest release in `releases/` (e.g. `v0.3.0 → v0.4.0`).
   - Hotfix mode: bump the patch (`v0.3.0 → v0.3.1`), unless `--version`
     overrides.

5. **Spawn `release-manager`.** Use the Agent tool with
   `subagent_type: "release-manager"` and a prompt like:

   > Brief: `docs/shipflow/briefs/BRIEF-<NNN>-<slug>.md` (or hotfix record
   > path in hotfix mode). Version: `<version>`.
   > `archive_on_ship: <true|false>`.
   > Write the release note, archive per config, report back.

6. **Auto-refresh the index.** Invoke `/sf-regen-index` via the Skill
   tool. The brief just left the warm layer; index is now stale.
   Don't make the user remember.

7. **Report to the user:**
   - Version shipped + release note path
   - Stories archived (or skipped archive if config disabled)
   - Index refreshed
   - If `--force-risk-acknowledged` was used: surface the override
     verbatim so it's visible in the report
   - Next step: tag / push in git if appropriate.

## Hard rules

- **One release per invocation.**
- **All stories must be `done`.** No ship with stories in `review` or
  `ready`. If Gate 4 is configured `block`, re-run it first.
- **Never tag, push, or publish.** The skill writes markdown and moves
  files; git and deploy operations stay in the user's hands.
- **Read narrowly.** Target brief + its stories + `stack.md` + release
  filenames (for version derivation). No unrelated briefs.

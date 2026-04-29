---
name: sf-resurvey
description: Re-run project-archaeologist on the current repo to refresh `docs/shipflow/stack.md` with rich, evidence-cited context. Use when /sf-init was run without --existing, when stack.md feels stale, or after a major refactor.
---

# sf-resurvey

Refresh `stack.md` by re-running the project archaeologist. Useful when:

- `/sf-init` was run **without** `--existing` (so `stack.md` is just a stub)
- The codebase has evolved meaningfully and `stack.md` no longer
  reflects current reality
- You inherited a ShipFlow project from someone else and want a real
  survey of where it's at
- Major refactor happened — naming / framework / structure changed

This is the "I want a real `stack.md` now" button.

## Arguments

None. Operates on the current repo.

## Steps

1. **Check init.** If `docs/shipflow/` doesn't exist, error out — run
   `/sf-init` first.

2. **Spawn `project-archaeologist` (via mono)** via the Agent tool with
   `subagent_type: "shipflow-mono"` and a prompt starting with
   `Mode: project-archaeologist. Adopt the role defined in shipflow/agents/project-archaeologist.md.`
   The archaeologist (in mono mode) will:
   - Survey the codebase broadly (manifests, configs, sample source
     files, recent git activity)
   - Verify every claim against actual code
   - **Preserve any user-authored content** in the existing `stack.md`
     by moving it under a `## User notes` section at the bottom
   - Overwrite the rest with a rich, evidence-cited survey

3. **Verify the handoff.** Read the new `stack.md`; confirm it has the
   "At a glance" section + "Project pulse" section + "Known unknowns"
   block. If anything's missing, surface the gap.

4. **Report to the user:**
   - Path written
   - One-line summary of what was found (languages, primary
     framework, key directories count, recent activity theme)
   - **Surface the "Known unknowns" section verbatim** — these are
     things the code couldn't tell the archaeologist; user should
     answer them inline so a future re-survey or downstream agent has
     the answers in `## User notes`

## Hard rules

- **Don't run any other phase.** This is a survey; not a Discover, not
  a brief. Read-only against the codebase, write-only against
  `stack.md`.
- **Preserve user notes.** The archaeologist already does this — but
  re-verify after it returns; warn if the user's original content
  appears to be missing.
- **One re-survey per invocation.** Don't loop or re-spawn.

---
name: sf-discover
description: Start a ShipFlow discovery dialogue. Takes a raw idea, slugs it, seeds docs/shipflow/discovery/<slug>/, and spawns the discovery moderator to run a 3-persona 2-round question loop. Presents the deduped questions to the user.
---

# sf-discover

Kick off a Discover-phase dialogue for a new idea.

## Arguments

- **required:** the idea, as a quoted string. Example: `/sf-discover "dark mode toggle"`.

## Steps

1. **Slug the idea.** Transform the quoted string into a URL-safe slug:
   - lowercase
   - replace runs of non-alphanumeric characters with a single `-`
   - trim leading/trailing `-`
   - cap length at 40 characters (cut on word boundary if possible)
   - if a directory with that slug already exists under `docs/shipflow/discovery/`, append `-2`, `-3`, etc.

2. **Create the discovery directory:** `docs/shipflow/discovery/<slug>/`.

3. **Write `seed.md`:**
   ```markdown
   ---
   slug: <slug>
   created: <yyyy-mm-dd>
   ---

   # Seed idea

   <the raw idea string, verbatim>
   ```

4. **Spawn the discovery-moderator (via mono).** Use the Agent tool with
   `subagent_type: "shipflow-mono"` and a prompt like:

   > Mode: discovery-moderator. Adopt the role defined in `shipflow/agents/discovery-moderator.md`.
   > Working directory: `docs/shipflow/discovery/<slug>/`.
   > Run the full 2-round dialogue with the three personas (tech, ux, business).
   > Converge to `questions.md` and a stitched `dialogue.md`.
   > Report back with the number of questions produced.

5. **When the moderator returns**, read `docs/shipflow/discovery/<slug>/questions.md`
   and display its contents to the user.

6. **Tell the user what to do next:**
   > Answer the questions above in your next message (free-form is fine —
   > the answers get written verbatim). When ready, run `/sf-brief`.

## Hard rules

- **Don't answer the questions yourself.** That's the user's job.
- **Don't read the archive** or any other discovery slug's files. Stay in `<slug>/`.
- **One moderator invocation, period.** If it fails, surface the error; don't retry with modifications.

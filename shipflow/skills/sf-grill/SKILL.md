---
name: sf-grill
description: Adversarial grill on any markdown file (brief, ADR, stack.md, retro draft, design doc, READMEs). Switchable persona lens (generic / security / product / architect / cofounder). Auto-injects git diff + status as silent context. Read-only — doesn't modify the target unless --save passed.
---

# sf-grill

Independent grill skill for any markdown artifact. Generalizes the
"smart-but-skeptical" challenger style beyond `/sf-brief`'s tail.
Use it whenever you've written something and want adversarial review
before committing — your stack.md, an ADR draft, a design doc, a retro
note, a release note.

## Arguments

- **required:** target file path. Relative to repo root or absolute.
  Examples:
  - `/sf-grill docs/shipflow/stack.md`
  - `/sf-grill docs/shipflow/decisions/ADR-001-foo.md`
  - `/sf-grill docs/shipflow/briefs/BRIEF-003-bar.md`
  - `/sf-grill ARCHITECTURE.md`
- **optional:** `--persona <type>`. Default: `generic`. Available:
  - `generic` — load-bearing claims without evidence
  - `security` — attack surface, trust boundaries, secrets, authz gaps
  - `product` — user specificity, outcome vs output, scope creep
  - `architect` — coupling, lock-in, migration path, hidden complexity
  - `cofounder` — wedge vs spreading, opportunity cost, why-now-why-you
- **optional:** `--save`. If passed, append a `## Grill notes
  (<persona>, <yyyy-mm-dd>)` section to the target file with the
  findings. Default: print to chat only, target file untouched.

## Steps

1. **Resolve and read the target file.** Error out cleanly if it
   doesn't exist, isn't readable, or isn't a markdown file (`.md` or
   `.markdown`).

2. **Capture git context silently** (don't display raw output to the
   user — fold into the grill as needed):
   - Run `git status --short` to see what's dirty repo-wide
   - Run `git diff --stat` for a high-level picture of uncommitted scope
   - If the **target file itself** has uncommitted changes, run
     `git diff -- <target>` and include that diff as context (you're
     grilling what the user **just wrote**, not yesterday's version)
   - If not inside a git repo: skip silently and continue with
     file-only grill

3. **Apply the persona lens.** Switch on `--persona`:

   - **generic**: Read for load-bearing claims that lack evidence.
     What's stated as fact but actually a guess? What sounds
     reasonable but isn't supported by the document itself or
     anything else verifiable? Voice drift, hand-waved risks.

   - **security**: Read as if you'll be on-call when this breaches.
     Where could secrets leak? What user input crosses a trust
     boundary unchecked? What's missing: rate limiting, authorization,
     audit logging, input validation? What logs PII or credentials?
     What assumes "internal only" without enforcing it? IDOR risks?

   - **product**: Read as a senior PM. Are users specific (named
     persona, trigger, frequency) or vague? Is success outcome-shaped
     (user behavior changes) or output-shaped (we shipped X)? What's
     the hidden scope creep? What's the wedge — and is it actually
     narrow enough to validate?

   - **architect**: Read as Staff Engineer. What does this couple to
     6 months from now? What's reversible vs locked-in? What's the
     migration path back if this fails? What hidden complexity does
     this assume (cache, sync, schema, distributed-systems gotchas)?
     What's the tech-debt accumulation path?

   - **cofounder**: Read as cofounder with skin in the game. Is this
     our wedge or are we spreading? Whose four weeks does this eat?
     What's the operating cost beyond launch (support, content
     refresh, on-call)? What does winning unlock vs distract from?
     What's the opportunity cost?

4. **Run the grill.** Generate 3–7 challenges matching the persona's
   lens. For each challenge:
   - **Quote** the line you're pushing back on. Include `file:line` if
     the target uses line numbers naturally; otherwise just quote.
   - State the **gap**: what's not supported, missing, ambiguous, or
     contradictory.
   - Suggest **1–2 specific paths forward** (concrete evidence to
     gather, named alternative, concrete rephrasing).
   - Stop when remaining doubts are matters of user judgment, not
     material gaps. Pressing past that is theater.

5. **Output the grill report.** Default destination is the chat
   (don't modify the file). Format:

   ```markdown
   # Grill: <target> (persona: <type>)

   _Git context: <one-line summary — "clean working tree" / "target
   has 12 uncommitted lines" / "not a git repo">_

   ## Q1. <one-line challenge>
   **From:** "<quoted line>"
   **Gap:** <what's missing or not supported>
   **Path forward:** <1–2 specific suggestions>

   ## Q2. ...

   ## Verdict
   <one of: "needs revision before commit" / "minor concerns, ship
   anyway" / "looks solid">
   ```

   If no material gaps land: write `_No material gaps from <persona>
   lens. Document looks solid._` and stop.

6. **If `--save` was passed**, append the report to the target file
   under a `## Grill notes (<persona>, <yyyy-mm-dd hh:mm>)` heading,
   preserving the rest of the file verbatim.

## Hard rules

- **Don't manufacture findings.** A clean document is a valid clean
  result. Quota grills are theater and burn user trust.
- **Cite the file.** Quote the actual line you're pushing back on. No
  vague "feels off" without evidence anchored in the text.
- **Don't fix.** Surface the gap and suggest a path forward; do not
  rewrite the user's document.
- **Read narrowly.** Target file + git context only. If the target
  references another file (a brief mentions a slice, an ADR mentions
  a story), flag the question rather than chasing the reference.
- **No subagent spawn.** Pure skill work — apply the lens, write the
  report. Spawning challenger or any other agent is overkill.
- **Persona is lens, not policy.** Grill style stays consistent across
  personas (concrete, quote-grounded, evidence-cited); only the
  **focus areas** change. A `security` grill on a brief still cites
  brief lines, doesn't pivot to scanning the codebase.

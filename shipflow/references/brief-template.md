---
id: BRIEF-{{nnn}}
slug: {{slug}}
status: draft
created: {{yyyy-mm-dd}}
updated: {{yyyy-mm-dd}}
---

# {{Title}}

## Problem

What's broken, missing, or painful today? State it from the user's perspective,
not the team's. Keep it to 2–5 sentences.

## Who

Who specifically feels this problem? Name the persona, their role, and the
frequency of the pain. Avoid "our users" — be concrete.

## Why now

What changed to make this worth doing in *this* cycle? External forcing function
(market, compliance, competitor), internal leverage (unlocks something bigger),
or accumulated cost of inaction. If "why now" is weak, reconsider scope.

## Constraints

Technical, time, stack, team, or policy constraints that bound the solution
space. Include path hints (e.g. `src/ui/**`, `prisma/**`) when relevant — they
drive specialist selection in Spec phase.

## Non-goals

What this brief deliberately does **not** cover. Be specific. "Mobile support"
is a non-goal if desktop is the whole target.

## Success

How will we know this worked? Prefer observable outcomes (metric moved,
workflow reduced from N steps to M) over outputs shipped.

## Risks

What could go wrong? Technical risks, adoption risks, dependencies on external
parties. One sentence each.

## Open questions

Questions the Discover dialogue couldn't resolve. Spec phase may still have
enough to proceed — these become flags, not blockers.

## Unresolved

_(Auto-populated by `/sf-brief` if the three persona slices contradict each other.)_

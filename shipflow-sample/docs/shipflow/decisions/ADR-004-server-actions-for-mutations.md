---
id: ADR-004
slug: server-actions-for-mutations
status: accepted
created: 2025-11-20
supersedes: null
tags: [server-actions, mutations]
---

# ADR-004: Server Actions for all mutations

## Status

accepted

## Context

Every mutation (log a habit, create a board, send an invite) needs a
write path. A separate `/api/*` REST layer would duplicate validation
that Server Actions can colocate with the form.

## Decision

All mutations go through Server Actions colocated with their feature
(e.g. `app/boards/actions.ts`). No hand-rolled REST endpoints except
the cron routes (ADR-006), which need a stable URL for Vercel Cron.

## Alternatives considered

- **REST API routes** — more portable if a mobile client shows up
  later, but not a v1 requirement.
- **tRPC** — nice DX, but another dependency for a solo project already
  using Server Actions successfully.

## Consequences

**Positive:** one less layer between form and DB write; validation
lives in one place.

**Negative:** harder to reuse a mutation from a future non-Next.js
client without wrapping it in a real endpoint.

**Neutral / follow-up:** revisit if/when a mobile app needs the same
mutations.

---
id: ADR-003
slug: lucia-auth
status: accepted
created: 2026-01-18
supersedes: null
tags: [lucia, auth, session]
---

# ADR-003: Session-based auth via Lucia

## Status

accepted

## Context

Need auth before any per-user data ships. Solo team; wants something
that doesn't fight App Router's server components.

## Decision

Use Lucia for session-based auth, email+password only for v1. Sessions
stored in Postgres via Prisma; cookie validated in middleware.

## Alternatives considered

- **NextAuth.js** — heavier config for one provider than needed now.
- **Roll our own** — session security isn't where solo time should go.

## Consequences

**Positive:** small dependency surface, works well with Server Actions.

**Negative:** no social login until a provider is added later.

**Neutral / follow-up:** add OAuth later if requested.

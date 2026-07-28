---
id: ADR-002
slug: prisma-orm
status: accepted
created: 2025-11-05
supersedes: null
tags: [prisma, orm, schema]
---

# ADR-002: Prisma as the ORM

## Status

accepted

## Context

Need type-safe DB access for `User`, `Habit`, `Log`, `Board`, and
`BoardMember` without hand-writing SQL per query, while keeping
migrations reviewable in git.

## Decision

Use Prisma with `prisma/schema.prisma` as the single source of truth.
Migrations committed to the repo; `prisma migrate deploy` on release.

## Alternatives considered

- **Drizzle** — lighter weight, closer to raw SQL; Prisma's migration
  workflow wins for solo velocity right now.
- **Raw SQL + query builder** — more control, more boilerplate than a
  solo project needs at this stage.

## Consequences

**Positive:** generated types catch schema/query mismatches at compile
time.

**Negative:** query engine adds cold-start latency on serverless;
acceptable at current traffic.

**Neutral / follow-up:** revisit if serverless cold-start becomes a
measured problem.

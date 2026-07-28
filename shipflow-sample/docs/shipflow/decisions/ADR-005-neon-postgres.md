---
id: ADR-005
slug: neon-postgres
status: accepted
created: 2025-11-02
supersedes: null
tags: [neon, postgres, database]
---

# ADR-005: Neon for Postgres hosting

## Status

accepted

## Context

Need a Postgres instance reachable from Vercel's serverless functions,
with low ops overhead for a solo maintainer and a real free/cheap tier
for a pre-revenue product.

## Decision

Use Neon (serverless Postgres). Connection via Prisma's Neon adapter to
handle serverless connection pooling correctly.

## Alternatives considered

- **Supabase** — comparable, but Neon's per-preview-deploy DB branching
  fits the solo workflow better.
- **Self-hosted Postgres (Fly.io / Railway)** — more control, more ops
  burden than a solo project should take on for v1.

## Consequences

**Positive:** DB branch per preview deploy; cheap at current scale.

**Negative:** connection pooling for serverless needs the adapter, not
just a raw Postgres URL.

**Neutral / follow-up:** revisit hosting if usage outgrows Neon's
pricing tiers.

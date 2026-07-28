---
id: ADR-006
slug: vercel-cron-scheduled-jobs
status: accepted
created: 2026-03-05
supersedes: null
tags: [cron, scheduled-jobs, vercel-cron]
---

# ADR-006: Vercel Cron for scheduled jobs

## Status

accepted

## Context

Reminders and digests need a scheduled trigger. Solo dev, already on
Vercel — a separate queue/worker is a new service for two cron jobs.

## Decision

Use Vercel Cron hitting `app/api/cron/*` routes, guarded by a shared
secret header. One route per job.

## Alternatives considered

- **BullMQ + Redis** — right tool at higher volume; overkill for two jobs.
- **GitHub Actions cron** — couples deploy infra to a second platform.

## Consequences

**Positive:** zero extra infra; config lives in `vercel.json`.

**Negative:** Vercel Cron's granularity/timeout caps how this scales.

**Neutral / follow-up:** revisit if job volume outgrows the limits.

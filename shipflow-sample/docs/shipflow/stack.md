# Stack — Loopline

_Habit tracker: logging, streaks, reminders, shared boards._

## Core

- **Next.js 14 (App Router)** — `app/`. ADR-001.
- **Prisma + Neon** — schema in `prisma/schema.prisma`. ADR-002, ADR-005.
- **Lucia** — session auth. ADR-003.
- **Server Actions** — all mutations. ADR-004.
- **Vercel Cron** — scheduled jobs. ADR-006.

## Conventions

- Logging: structured `key=value` at boundaries. No secrets.
- Tests: Vitest, colocated as `*.test.ts`. Errors propagate with stack
  trace; validate at the edge only.

## Paths

`app/` routes/UI · `lib/` actions, Prisma, Lucia, mail · `prisma/` schema

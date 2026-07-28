---
id: BRIEF-003
slug: streak-reminders-weekly-digest
status: specced
created: 2026-03-02
updated: 2026-03-14
---

# Streak reminders & weekly digest

## Problem

Users who miss a day silently lose their streak and don't notice until
days later. No nudge to log, no recap of progress.

## Who

Casual loggers (3-5 entries/week) who say they "forget to open the
app." Power users want a weekly summary, not per-day noise.

## Why now

Week-1 retention dropped after the v0.2 streak launch: users see a
streak break and don't come back. Cheapest lever available.

## Constraints

- Must run on Vercel Cron (no separate worker/queue infra).
- Email only for v1. Respect per-user timezone on the `User` model.

## Non-goals

- Push notifications. Configurable digest cadence (weekly only).

## Success

Day-7 retention improves measurably over the v0.2 baseline; reminder
reads as "helpful, not spammy."

## Risks

- Deliverability (spam filters). Wrong-timezone sends erode trust fast.

## Open questions

- Snooze for N days? Deferred to a follow-up brief if requested.

## Unresolved

_None._

# Retro — v0.2.0

_Streak counters & basic notifications_

## What went well

- Streak calculation shipped without a schema migration surprise —
  ADR-002's Prisma schema anticipated the `currentStreak` field.
- Missed-day banner was the cheapest-possible version of "don't let the
  streak break silently," and users noticed it in feedback.

## What didn't

- The single daily reminder email ignored timezone entirely — several
  users got it at 3am local. Directly caused BRIEF-003.
- No duplicate-send guard: a cron retry once double-sent the reminder
  to a subset of users.

## Carried into next brief

- Timezone-aware send time (BRIEF-003)
- Duplicate-send guard as a hard acceptance criterion, not an
  afterthought (STORY-0010)

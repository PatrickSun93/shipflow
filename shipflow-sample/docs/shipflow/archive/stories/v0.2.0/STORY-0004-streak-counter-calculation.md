---
id: STORY-0004
brief: BRIEF-002
status: done
size: M
depends_on: []
---

# Streak counter calculation

## Goal

A user sees their current consecutive-day streak per habit, not just a
raw log count.

## Acceptance criteria

- [x] `currentStreak` computed from consecutive Log rows ending today
      or yesterday (grace for "haven't logged yet today")
- [x] Streak resets to 0 the first day fully missed
- [x] List view shows the streak number next to each habit

## Notes

Migrated auth to Lucia (ADR-003) in the same release; unrelated to
this story but noted here since it's the same deploy.

## Build log

`lib/streaks.ts`, `prisma/schema.prisma` (added `currentStreak`). Tests
green (9/9).

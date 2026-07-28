---
id: STORY-0005
brief: BRIEF-002
status: done
size: S
depends_on: [STORY-0004]
---

# Missed-day warning banner

## Goal

A user who hasn't logged a habit yet today, with a streak on the line,
sees a banner before the day ends.

## Acceptance criteria

- [x] Banner shows when a habit's streak is 2+ and today isn't logged
- [x] Banner links directly to that habit's log action
- [x] Dismissing the banner doesn't suppress it again tomorrow

## Notes

Client-side only (checks current local time vs. server-provided
"logged today" state).

## Build log

`app/habits/StreakBanner.tsx`. Tests green (4/4).

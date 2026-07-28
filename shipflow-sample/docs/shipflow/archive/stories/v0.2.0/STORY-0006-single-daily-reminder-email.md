---
id: STORY-0006
brief: BRIEF-002
status: done
size: S
depends_on: []
---

# Single daily reminder email

## Goal

Users get one daily email if they haven't logged anything that day.

## Acceptance criteria

- [x] Cron route runs once daily at a fixed UTC hour
- [x] Sends to any user with zero Log rows for the current UTC date
- [x] Email links straight to the habit list

## Notes

Fixed UTC hour caused the timezone complaints that motivated BRIEF-003
(see retro-v0.2.md). No duplicate-send guard either — a cron retry
once double-sent this to a subset of users.

## Build log

`app/api/cron/reminder/route.ts`. Tests green (3/3).

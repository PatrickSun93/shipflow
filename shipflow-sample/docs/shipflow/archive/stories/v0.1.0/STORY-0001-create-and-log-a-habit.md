---
id: STORY-0001
brief: BRIEF-001
status: done
size: M
depends_on: []
---

# Create and log a habit

## Goal

A user can create a habit and mark it done for today.

## Acceptance criteria

- [x] Create-habit form writes a Habit row scoped to the user
- [x] "Mark done today" writes a Log row for today's date
- [x] Marking done twice in a day doesn't create duplicate Log rows

## Notes

First write path in the app — sets the pattern later stories reuse.

## Build log

`app/habits/actions.ts`, `prisma/schema.prisma`. Tests green (8/8).

---
id: STORY-0002
brief: BRIEF-001
status: done
size: S
depends_on: [STORY-0001]
---

# Daily habit list view

## Goal

A user sees today's habits in one list with a done/not-done state per
habit.

## Acceptance criteria

- [x] List page queries the user's habits + today's Log rows
- [x] Each row shows a checkbox reflecting today's done state
- [x] Empty state (no habits yet) links to create-habit

## Notes

Server component; the checkbox is the only client-interactive piece.

## Build log

`app/habits/page.tsx`. Tests green (5/5).

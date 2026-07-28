---
id: STORY-0013
brief: BRIEF-004
status: review
size: M
depends_on: []
---

# Board create and invite

## Goal

A user can create a board and invite up to 7 others by email.

## Acceptance criteria

- [x] Create-board form writes a Board + creator BoardMember row
- [x] Invite email has a one-time accept link (login required)
- [x] 9th invite is rejected (8-member cap)

## Notes

Auth via Lucia session (ADR-003); no separate invite tokens.

## Build log

`app/boards/actions.ts`, `lib/invites.ts`. Tests green.

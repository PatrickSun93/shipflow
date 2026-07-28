---
id: STORY-0015
brief: BRIEF-004
status: ready
size: S
depends_on: [STORY-0013]
---

# Board activity feed

## Goal

A lightweight feed ("Sam logged a habit — 2h ago") so members feel
activity without a chat app.

## Acceptance criteria

- [ ] Feed shows the last 20 log events across board members
- [ ] Entries show name + time only, no habit detail
- [ ] Feed updates on next page load (no realtime for v1)

## Notes

Same privacy bound as STORY-0014 — presence-only, not content.

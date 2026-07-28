---
id: STORY-0012
brief: BRIEF-003
status: ready
size: S
depends_on: [STORY-0010]
---

# Reminder time preference

## Goal

A user can pick what "evening" means for them (a simple hour picker)
instead of a hardcoded 8pm local default.

## Acceptance criteria

- [ ] Settings page exposes an hour dropdown, defaults to 20:00 local
- [ ] Cron sweep reads the stored preference, not a hardcoded hour
- [ ] Changing the preference takes effect on the next sweep, no restart

## Notes

Depends on STORY-0010's timezone-aware sweep landing first — this story
only adds the per-user hour on top of it.

## Gate verdicts

_(not yet built)_

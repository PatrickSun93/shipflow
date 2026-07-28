---
id: STORY-0010
brief: BRIEF-003
status: in-progress
size: M
depends_on: []
---

# Daily reminder email job

## Goal

A user who hasn't logged a habit by their local evening gets one
reminder email — not zero, not several.

## Acceptance criteria

- [x] Cron route runs once daily, queries users with no log entry today
- [x] Send respects each user's stored timezone before computing "today"
- [ ] Duplicate-send guard: a user never gets two reminder emails same day
- [ ] Unsubscribe link in every email updates `User.remindersEnabled`

## Notes

See ADR-006 for the cron-route approach. Email send goes through the
existing transactional mail helper in `lib/mail.ts`; no new provider.

## Build log

_(in progress — duplicate-send guard and unsubscribe link remaining)_

## Gate verdicts

_(pending /sf-check-build)_

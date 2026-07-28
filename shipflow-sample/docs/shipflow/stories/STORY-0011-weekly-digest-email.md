---
id: STORY-0011
brief: BRIEF-003
status: in-progress
size: M
depends_on: []
---

# Weekly digest email

## Goal

Every user with at least one log this week gets a Sunday-evening email
summarizing days logged and current streak.

## Acceptance criteria

- [x] Cron route aggregates the past 7 days per user
- [ ] Email renders streak delta ("+2 this week"), not just a raw count
- [ ] Users with zero logs this week are skipped, not sent an empty digest

## Notes

Shares the cron-guard pattern from STORY-0010 (see ADR-006). Digest
template lives alongside the reminder template in `lib/email-templates/`.

## Build log

_(in progress — streak-delta rendering remaining)_

## Gate verdicts

_(pending /sf-check-build)_

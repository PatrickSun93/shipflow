---
id: STORY-0003
brief: BRIEF-001
status: done
size: M
depends_on: []
---

# Basic email/password signup + auth

## Goal

A new user can sign up with email/password and stay logged in across
visits.

## Acceptance criteria

- [x] Signup form creates a User + hashed password
- [x] Session cookie set on signup and on login
- [x] Protected routes redirect to `/login` when session is missing

## Notes

Predates ADR-003 (Lucia landed in v0.2); this used a hand-rolled
session cookie, later replaced.

## Build log

`app/login/actions.ts`, `app/signup/actions.ts`. Tests green (6/6).

---
id: ADR-001
slug: nextjs-app-router
status: accepted
created: 2025-11-02
supersedes: null
tags: [app-router, routing, nextjs]
---

# ADR-001: Next.js App Router for all routes

## Status

accepted

## Context

Starting a new Next.js project from scratch; Pages Router is legacy at
this point and App Router's server components fit a mostly server-
rendered habit tracker.

## Decision

All routes live under `app/` using the App Router. Server components by
default; `"use client"` only where local interactivity requires it (the
habit-logging checkbox, the streak-view toggle).

## Alternatives considered

- **Pages Router** — well-understood but legacy; no reason to start a
  new project on it.
- **Remix** — solid alternative, but App Router keeps the stack inside
  one framework's docs and conventions.

## Consequences

**Positive:** server components cut client JS for mostly-static pages.

**Negative:** newer patterns (streaming, `loading.tsx`) have a learning
curve solo.

**Neutral / follow-up:** none anticipated.

# ShipFlow

> **Other languages:** [中文](./README.zh.md)

A Claude Code plugin for solo developers: a multi-agent product-dev workflow
**Discover → Spec → Build → Verify → Ship**, with four advisory gates and
cross-cutting reviewers.

All artifacts (briefs, stories, ADRs, releases) live in-repo as markdown.
No external services required.

## Status

**v0.2.5** — all five phases scaffolded and usable.

- **19 agents** — 2 Tier-1 reviewers (product-lead, tech-lead), 4 Discover
  personas, 1 challenger, 6 domain experts (education / fintech / healthcare /
  ecommerce / devtools / social), 5 phase leads (spec-author, build-lead,
  qa-lead, release-manager, security-reviewer, cofounder-expert).
- **18 skills** — init, discover, brief, spec, adr, build, tiny, hotfix,
  verify, ship, regen-index, next, checkpoint, plus the four gates
  (`/sf-check-brief` / `-plan` / `-build` / `-ship`) and two cross-cutting
  reviews (`/sf-security-review`, `/sf-cofounder-review`).
- **4 hooks** — SessionStart, Stop, PreCompact, UserPromptSubmit.

## Install (local / dev)

Start Claude Code with the plugin dir mounted:

```bash
claude --plugin-dir ./shipflow
```

Or add a shell alias:

```bash
alias claude-sf='claude --plugin-dir /path/to/shipflow'
```

After editing plugin source, hot-reload in-session:

```
/reload-plugins
```

## Quick start

```bash
/sf-init                          # one-time repo setup
/sf-discover "your idea"          # 3–4 personas research + ask questions
# ...answer the questions...
/sf-brief                         # assemble brief; challenger stress-tests
/sf-check-brief                   # Gate 1: product-lead + tech-lead
/sf-spec                          # slice brief into 5–10 stories
/sf-check-plan                    # Gate 2: per-story tech review
/sf-build                         # implement one story
/sf-check-build                   # Gate 3: tests + acceptance + code review
/sf-verify                        # qa-lead checks against brief's Success
/sf-check-ship                    # Gate 4: structural pre-ship check
/sf-ship                          # cut release, archive brief + stories
```

Or just `/sf-next` — reads repo state and auto-runs whatever comes next.

## What makes it different

**Multi-lens Discovery with auto-research.** Tech / UX / Business personas
run in parallel, plus an optional domain expert auto-matched from the seed
(education / fintech / healthcare / ecommerce / devtools / social). Each
persona runs 1–3 WebSearch queries first — users only answer judgment
questions, not facts the agent could look up.

**Advisory gates by default.** Four review checkpoints (brief / plan /
build / ship) surface verdicts without blocking; flip individual gates to
`block` in `shipflow.config.json` for stricter enforcement.

**Cross-cutting reviewers on demand.** `/sf-security-review` runs a 7-pass
audit (secrets, auth, injection, authz, deps, data, defaults).
`/sf-cofounder-review` asks founder-level bet questions (three-person test,
forcing function, unfair advantage stack, counterfactual cost).

**Pause-resistant session resume.** `UserPromptSubmit` hook logs each turn
to `docs/shipflow/sessions/log-<date>.md`. `/sf-checkpoint` captures rich
intent before suspected usage exhaustion. SessionStart surfaces both on the
next session — so work isn't lost when Claude Code hits a usage cap.

**Fast paths.** `/sf-tiny` for trivial one-file changes (skip Discover /
Spec). `/sf-hotfix` for prod bugs (skip to Build → Ship).

## Conventions

- **Size caps.** Agents ≤2000 tokens (typical 800–1500; reviewer roles
  with Identity sections may use the full range), hooks ≤500 tokens.
  Tokens, not lines — that's what the model actually budgets against.
- **Gates advisory by default.** Flip in `shipflow.config.json` when ready.
- **Read narrowly.** No archive access from phase skills unless explicitly
  asked.
- **Personas never propose solutions during Discover.** That's Spec's job.
- **Clear and simple over clever abstraction.** Applies to agent prompts,
  hook scripts, skill instructions, and the code `/sf-build` produces.

## Directory layout (after `/sf-init`)

```
your-repo/
├── CLAUDE.md                    # hot layer (auto-read every session)
├── shipflow.config.json         # gate modes, archive-on-ship, etc.
└── docs/shipflow/
    ├── index.md                 # warm-layer index (via /sf-regen-index)
    ├── stack.md                 # tech stack reference
    ├── briefs/                  # approved product briefs
    ├── stories/                 # active (STORY / TINY / HOTFIX records)
    ├── decisions/               # ADRs
    ├── releases/                # shipped release notes
    ├── retros/                  # post-ship retros
    ├── diaries/                 # per-agent review log
    ├── discovery/<slug>/        # per-idea dialogue + synthesis
    ├── sessions/                # per-turn logs + checkpoints
    └── archive/                 # cold layer — shipped work moves here
```

## Acknowledgements

- **Diary + Stop/PreCompact hooks** — ideas borrowed from
  [MemPalace](https://github.com/MemPalace/mempalace), reimplemented as
  file-based markdown (no shared code).
- **Named mental models + research-first protocol** in `cofounder-expert`
  are inspired by [nuwa-skill](https://github.com/alchaincyf/nuwa-skill)'s
  person-based perspective skills.
- **Phased multi-persona structure** draws on prior art documented in
  `../workflow-comparison.md` (BMAD, Agent OS, SuperClaude,
  Claude-Code-Game-Studios, claude-sub-agent).

No code shared across projects — ShipFlow stays dependency-free.

## License

MIT.

# ShipFlow

> **Other languages:** [中文](./README.zh.md)

A Claude Code plugin that gives solo developers a multi-agent product-dev workflow:
**Discover → Spec → Build → Verify → Ship**, with four advisory gates between phases.

Stories, ADRs, briefs, and releases live in-repo as markdown. No external integrations required.

## Status

- **Discover phase**: scaffolded and usable.
- **Spec / Build / Verify / Ship**: designed, not yet scaffolded.

## Install (local / dev)

```bash
/plugin add ./shipflow
```

Or copy this folder to your Claude Code plugins directory and `/plugin reload`.

## Quick start

```bash
/sf-init                        # one-time repo setup
/sf-discover "dark mode toggle" # start a discovery dialogue
# ...answer the questions the moderator produces...
/sf-brief                       # synthesize answers into a brief
/sf-gate-1                      # advisory review before Spec
```

## How it works

`/sf-discover` spawns a **discovery moderator** that orchestrates three parallel
personas — **Tech**, **UX**, **Business** — over two rounds (initial + cross-talk).
Each persona writes its own `dialogue-<persona>.md` file to avoid write collisions.
The moderator converges the three into a deduped `questions.md` for you to answer.

`/sf-brief` re-spawns the three personas in parallel to each synthesize a slice of
the final brief (tech: constraints+risks; ux: who+open-qs; business: why-now+success+non-goals),
then stitches them into `docs/shipflow/briefs/BRIEF-NNN-<slug>.md`.

`/sf-gate-1` spawns `product-lead` + `tech-lead` reviewers in parallel; they each
write a `gate-1-review-<role>.md` breadcrumb. The skill classifies a single verdict
(approve | needs-changes | reject) and appends it to the brief.

## Conventions

- **Gates are advisory by default** (warnings, not blocks). Flip to blocking in
  `shipflow.config.json` when you want stricter enforcement.
- **All phase skills read narrowly** — no archive access, no unrelated briefs.
- **Personas never propose solutions during Discover.** That's Spec's job.
- **Code style: clear and simple over clever abstraction.** Applies to agent prompts,
  hook scripts, and skill instructions.

## Directory layout (after `/sf-init`)

```
your-repo/
├── CLAUDE.md                    # hot layer (auto-read every session)
├── shipflow.config.json         # gate modes, index-regen cadence, etc.
└── docs/shipflow/
    ├── index.md                 # warm-layer index (auto-regenerated)
    ├── stack.md                 # tech stack reference
    ├── briefs/                  # approved product briefs
    ├── stories/                 # active stories
    ├── decisions/               # ADRs
    ├── releases/                # shipped release notes
    ├── retros/                  # optional post-ship retros
    ├── discovery/<slug>/        # per-idea dialogue + synthesis breadcrumbs
    └── archive/                 # cold layer — shipped work moves here
```

## Acknowledgements

- **Per-agent diary** (`docs/shipflow/diaries/<agent>.md`) and **Stop +
  PreCompact hooks** are file-based reimaginings of ideas from
  [MemPalace](https://github.com/MemPalace/mempalace). No code shared —
  ShipFlow stays dependency-free.
- **Phased multi-persona workflow structure** draws on prior art documented
  in `workflow-comparison.md` in the parent directory (rows pending
  firsthand review).

## License

MIT.

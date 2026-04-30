# ShipFlow — `experiment/mono-agent` branch

> **Other languages:** [中文](./README.zh.md)
>
> ⚠️ **This is the single-agent experimental variant.** For the
> production multi-agent plugin, switch to `main` or install via
> marketplace (see "Don't install this branch" below).

## What this branch is

The `experiment/mono-agent` variant of ShipFlow. **Same workflow,
same artifacts, same skills — but ONE agent instead of 22.**

It exists to A/B test the question: *"Are 22 specialized agents
genuinely needed, or could one parameterized agent do the same work?"*
That question was admitted as unverified in
[`DESIGN.md`](../DESIGN.md). This branch is the experiment.

See [`EXPERIMENT.md`](../EXPERIMENT.md) at the repo root for the full
hypothesis, comparison protocol, and acceptance criteria.

## Architecture difference (the only variable changed)

| | `main` (multi-agent) | `experiment/mono-agent` (this branch) |
|---|---|---|
| Agent count | 22 specialized agents | **1 `shipflow-mono` agent** |
| Spawn pathway | `subagent_type: "<role>"` direct | `subagent_type: "shipflow-mono"` + `Mode: <role>` directive |
| Role content delivery | System prompt of specialized agent | Read-tool result of `shipflow/agents/<role>.md` |
| Workflow / artifacts / skills | identical | identical |
| Per-spawn fresh context | identical (Claude Code runtime) | identical (Claude Code runtime) |

The 22 specialized agent files **are still in this branch** under
`shipflow/agents/<role>.md` — they serve as **role references** the
mono agent reads on first turn. Their content is unchanged.

## Don't install this branch via marketplace

The marketplace (`/plugin marketplace add ...`) points at `main`.
This branch is **never** auto-installed; users on `main` are
unaffected.

To run this variant for the experiment, install **locally**:

```bash
git clone https://github.com/PatrickSun93/shipflow.git shipflow-mono
cd shipflow-mono
git checkout experiment/mono-agent
claude --plugin-dir ./shipflow
```

Or with the plugin dir flag:

```bash
claude --plugin-dir /path/to/shipflow-mono/shipflow --dangerously-skip-permissions
```

## Don't merge this branch

Per the contract in [`EXPERIMENT.md`](../EXPERIMENT.md):

> Don't merge unless the experiment produces a clear answer AND the
> decision (collapse or keep) is made deliberately.

If the experiment shows mono ≥ multi on quality + cost, the path
forward is a deliberate v0.3 collapse, not a fast-merge of this
branch.

## Version on this branch

`shipflow/.claude-plugin/plugin.json` shows `"version":
"0.2.24-mono.0"`. The `-mono.0` suffix marks the experimental status
and is your visual confirmation you're running the mono variant.

`marketplace.json` is **deliberately unchanged** on this branch
(stays at `0.2.24` pointing at the multi-agent main version) so users
doing `/plugin update` from the marketplace catalog stay clean on
main.

---

# Below is the multi-agent README (preserved verbatim for reference)

## What ShipFlow is

**A multi-agent product team in a folder.**

ShipFlow gives solo developers what a startup with 8 people gets: a Tech
Lead, Product Lead, Cofounder, QA, Security Reviewer, DB Reviewer, plus
six domain experts (education / fintech / healthcare / ecommerce /
devtools / social) — all coordinated through a 5-phase workflow:
**Discover → Spec → Build → Verify → Ship**.

Each agent has a real **point of view**, named methodologies (JTBD /
RICE / OWASP / CAP / Three-Person Test / Rollback Test...), and the
patience to push back when something's off. Briefs, stories, ADRs, and
releases all live in your repo as markdown. No SaaS, no Jira, no
external services.

## Status

**v0.2.21** — all five phases scaffolded and dogfood-validated.

**Honest agent count: 22 total, structured as:**
- **8 role-embodied reviewers with Identity & POV** — `tech-lead`,
  `product-lead`, `cofounder-expert`, `qa-lead`, `security-reviewer`,
  `db-reviewer`, `code-reviewer`, `build-lead`, `challenger`
- **3 Discovery personas with Identity & POV** — `discovery-tech-persona`,
  `discovery-ux-persona`, `discovery-business-persona` (added v0.2.21
  — previously thin task-spec prompts)
- **6 domain experts** (auto-spawned by domain match in Discovery) —
  education, fintech, healthcare, ecommerce, devtools, social. Focused
  on domain-specific concerns; lighter on Identity than the 8+3 above.
- **5 specialty / coordinator agents** — `discovery-moderator`,
  `spec-author`, `release-manager`, `project-archaeologist`, plus
  challenger (also counted above as a reviewer)

**24 skills** — init, discover, brief, spec, adr, build (with `--tdd`
hard red-green-refactor mode and `--all` sweep mode), tiny, quick,
hotfix, verify, ship, regen-index, resurvey, next, checkpoint, lint,
grill, diagnose, plus four gates (`/sf-check-{brief,plan,build,ship}`)
and three cross-cutting reviews (`/sf-security-review`,
`/sf-db-review`, `/sf-cofounder-review`).

**4 hooks** — SessionStart, Stop, PreCompact, UserPromptSubmit.

## Install

### Recommended — via Claude Code marketplace

In any Claude Code session, **run these two commands one at a time**
(wait for each to return before sending the next):

```
/plugin marketplace add https://github.com/PatrickSun93/shipflow
```

```
/plugin install shipflow@shipflow-marketplace
```

> Slash-command parsers can concatenate multiple lines into one if you
> paste them together — leading to a malformed URL. Send each on its
> own turn.
>
> The `PatrickSun93/shipflow` shorthand defaults to SSH and may fail on
> machines without `github.com` in `~/.ssh/known_hosts`. The full HTTPS
> URL above works everywhere for public repos.

Verify:

```
/help
```

You should see `/sf-init`, `/sf-discover`, `/sf-next`, `/sf-build`, etc.

To update later:

```
/plugin update shipflow@shipflow-marketplace
```

### Alternative — local / dev

For working on the plugin source itself:

```bash
git clone https://github.com/PatrickSun93/shipflow.git
claude --plugin-dir ./shipflow/shipflow
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
/sf-build                         # implement one story (or --all to sweep)
/sf-check-build                   # Gate 3: tests + acceptance + code review
/sf-verify                        # qa-lead checks against brief's Success
/sf-check-ship                    # Gate 4: structural + blocking-review check
/sf-ship                          # cut release, archive, auto-regen index
```

Or just `/sf-next` — reads repo state and runs (or recommends) the
appropriate next step.

## What makes it different

**Multi-lens Discovery with auto-research.** Tech / UX / Business personas
run in parallel, plus an optional domain expert auto-matched from the seed
(education / fintech / healthcare / ecommerce / devtools / social). Each
persona runs 1–3 WebSearch queries first — users only answer judgment
questions, not facts the agent could look up.

**Reviewers think like roles, not checklists.** Every Tier-1 reviewer
(tech-lead, product-lead, cofounder-expert, qa-lead, security-reviewer,
db-reviewer, build-lead, challenger) carries an Identity & POV section
plus named methodology toolkits — JTBD / RICE / Kano for product, CAP /
OWASP / 12-factor / Rollback Test for tech, three-person test / forcing
function / pre-mortem / Deletion Test for cofounder, etc. Reviewers have
opinions and instincts, not just a 5-bullet checklist.

**Advisory gates by default, blocking when configured.** Four review
checkpoints (brief / plan / build / ship) surface verdicts; flip individual
gates to `block` in `shipflow.config.json` for stricter enforcement.
Cross-cutting `Verdict: blocking` from security / DB / cofounder reviews
hard-stops `/sf-ship` — override only with `--force-risk-acknowledged`,
which gets recorded in the release note.

**Cross-cutting reviewers on demand.** `/sf-security-review` (7-pass:
secrets, auth, injection, authz, deps, data, defaults). `/sf-db-review`
(6-pass: schema, indexes, migrations, query patterns, data evolution,
sync/consistency). `/sf-cofounder-review` (six founder frameworks +
domain overlay + Founder gut check).

**Auto-suggest at the right moment.** `/sf-next` and `/sf-check-build`
scan the build log for path signals (migrations / auth / token / etc.)
and recommend the relevant cross-cutting review — solo dev decides
whether the path signal is real risk.

**Pause-resistant session resume.** `UserPromptSubmit` hook logs each turn
to `docs/shipflow/sessions/log-<date>.md`. `/sf-checkpoint` captures rich
intent before suspected usage exhaustion. SessionStart surfaces both on the
next session — work isn't lost when Claude Code hits a usage cap.

**Workflow integrity check.** `/sf-lint` strict-checks frontmatter,
dangling `depends_on`, orphan `needs-ADR` markers, broken brief↔story
links, dead `index.md` links, and verdict-vs-status drift.

**Three sizes — pick the right entry point.** Solo dev work isn't
all the same shape; ShipFlow has three explicit paths so you don't run
the full 5-phase flow for a typo fix:

| Size | Path | When |
|---|---|---|
| 🪶 **Tiny** | `/sf-tiny "<fix>"` | One-file trivial: typo, copy fix, comment update |
| 🚀 **Quick** | `/sf-quick "<feature or fix>"` | **Existing project, mid-tier feature/bug — you already know the scope.** Skips Discover + Spec ceremony, generates a minimal brief + 1-3 ready-to-build stories inline. |
| 🛠️ **Full** | `/sf-discover "<idea>"` → ... | Greenfield product, significant bet, scope is unclear |
| 🚨 **Hotfix** | `/sf-hotfix "<bug>"` | Production emergency, skip to Build → Ship |

For an existing app where you've already shipped something, `/sf-quick`
is usually the right answer. The full flow is overkill when you don't
need 18 persona questions for a 2-line bug fix.

## Conventions

- **Size caps.** Agents ≤2000 tokens (typical 800–1500; reviewer roles
  with Identity sections may use the full range), hooks ≤500 tokens.
  Caps are guidance, not red lines — substantive content wins over
  mechanical compression.
- **Model is user-controlled.** No `model:` in agent frontmatter; subagents
  inherit the user's session model (Opus / Sonnet / Haiku).
- **Read narrowly.** No archive access from phase skills unless explicitly
  asked.
- **Personas never propose solutions during Discover.** That's Spec's job.
- **Clear and simple over clever abstraction.** Applies to agent prompts,
  hook scripts, skill instructions, and the code `/sf-build` produces
  (KISS/YAGNI, trust internal boundaries + log them, Rule of Three, no
  half-finished code, match neighbor style).

## Directory layout (after `/sf-init`)

```
your-repo/
├── CLAUDE.md                    # hot layer (auto-read every session)
├── shipflow.config.json         # gate modes, cofounder review mode, archive
└── docs/shipflow/
    ├── index.md                 # warm-layer index (via /sf-regen-index)
    ├── stack.md                 # tech stack + conventions
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
  inspired by [nuwa-skill](https://github.com/alchaincyf/nuwa-skill)'s
  person-based perspective skills.
- **Anthropic's prompt engineering best practices** for Claude Opus 4.7
  shaped the XML-tag structure (`<investigate_before_answering>`,
  `<default_to_action>`, `<coverage_first>`) used in build-lead,
  cofounder-expert, security-reviewer, and db-reviewer.
- **Phased multi-persona structure** draws on prior art documented in
  `../workflow-comparison.md` (BMAD, Agent OS, SuperClaude,
  Claude-Code-Game-Studios, claude-sub-agent).

No code shared across projects — ShipFlow stays dependency-free.

## License

MIT.

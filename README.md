# claude-code-project

This repo houses **ShipFlow** — a Claude Code plugin that gives solo developers
a multi-agent product-dev workflow (Discover → Spec → Build → Verify → Ship),
plus the design docs and handoff notes that produced it.

## What's here

| Path | What it is |
|------|------------|
| [`shipflow/`](./shipflow/) | The plugin itself. Installable in Claude Code. |
| [`handoff.md`](./handoff.md) | Running log of locked design decisions and the punch list of next steps. The authoritative record of *why* things are the way they are. |
| [`shipflow-plan.md`](./shipflow-plan.md) | Detailed per-phase design — agents, skills, gates, trade-offs, cross-cutting concerns. |
| [`shipflow-memory-measurement.md`](./shipflow-memory-measurement.md) | The 3-layer memory model and how to verify budgets hold. |
| [`workflow-comparison.md`](./workflow-comparison.md) | Prior-art comparison (BMAD, Agent OS, SuperClaude, Claude-Code-Game-Studios, claude-sub-agent). |

## Status

- **Discover phase** of the plugin: scaffolded, validated, ready to try.
- **Spec / Build / Verify / Ship:** designed (see [`shipflow-plan.md`](./shipflow-plan.md)),
  not yet scaffolded.
- **Sample fixture + measurement script:** designed, not yet rebuilt after the
  Cowork → Claude Code transition.

See the "Next steps" section in [`handoff.md`](./handoff.md) for the current
punch list.

## Installing the plugin

From Claude Code, with this repo cloned:

```bash
/plugin add ./shipflow
```

Then in a fresh repo where you want to use ShipFlow:

```bash
/sf-init                        # one-time setup
/sf-discover "your first idea"  # start a discovery dialogue
```

See [`shipflow/README.md`](./shipflow/README.md) for the full quick-start.

## Conventions

- **Clear and simple over clever abstraction.** Agent prompts, hook scripts, and
  skill instructions all follow this rule.
- **Agent prompts ≤80 lines.** Hook scripts ≤40 lines of bash. Not arbitrary —
  it keeps each component readable by a human, not just by the model.
- **Read narrowly.** No archive access from phase skills unless explicitly
  asked. Enforced by agent prompts; audit hook designed but not yet written.

## License

MIT — see [`LICENSE`](./LICENSE).

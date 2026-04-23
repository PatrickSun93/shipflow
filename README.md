# claude-code-project

> **Other languages:** [中文](./README.zh.md)

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
- **Agent prompts 800–1500 tokens.** Hook scripts ≤500 tokens. Tokens, not
  lines, because that's what the model actually budgets against. Keeps each
  component readable by a human, not just by the model.
- **Read narrowly.** No archive access from phase skills unless explicitly
  asked. Enforced by agent prompts; audit hook designed but not yet written.

## Acknowledgements

Ideas borrowed (not code — everything here is ShipFlow-native, no external deps):

- **[MemPalace](https://github.com/MemPalace/mempalace)** — The per-agent diary
  concept in `docs/shipflow/diaries/<agent>.md` is a file-based reimagining of
  MemPalace's `diary_write` / `diary_read` MCP tools. The Stop + PreCompact
  hooks also borrow from MemPalace's hook design, but as minimal markdown
  markers rather than verbatim transcript storage.
- **The Claude Code / agentic-dev workflow prior art** — overall phased
  structure (Discover → Spec → Build → Verify → Ship) and multi-persona
  discovery draws on patterns from projects including BMAD, Agent OS,
  SuperClaude, Claude-Code-Game-Studios, and claude-sub-agent. See
  [`workflow-comparison.md`](./workflow-comparison.md) — the comparison table's
  rows for those projects are still marked `_TODO_` pending firsthand review.

## License

MIT — see [`LICENSE`](./LICENSE).

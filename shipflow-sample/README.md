# shipflow-sample

A realistic ShipFlow repo fixture, used to measure whether each phase's
"narrow read set" actually fits its memory budget. See
[`../shipflow-memory-measurement.md`](../shipflow-memory-measurement.md)
for the full methodology (the 3-layer memory model, per-phase budgets,
and what "narrow read set" means per phase).

This is a **memory-budget measurement harness** — it checks bytes read
and archive leakage. It is not a quality/rubric scorer and not a
cost/latency evaluator.

## What's in here

- `CLAUDE.md`, `shipflow.config.json` — Hot layer + config, as `sf-init`
  would create them.
- `docs/shipflow/` — Warm layer: `stack.md`, `index.md`, 2 briefs
  (BRIEF-003, BRIEF-004), 6 active stories (3 in-flight, 3 ready), 6
  ADRs, 2 releases, 1 retro, and a `discovery/habit-templates/` dialogue
  in progress.
- `docs/shipflow/archive/` — Cold layer: 6 stories shipped in two
  historical releases (v0.1.0, v0.2.0). No phase should ever read this.
- `measure.py` — the measurement script itself.

## Running it

From the repo root:

```
python3 shipflow-sample/measure.py
```

Prints a table of bytes read / file count / budget / PASS-FAIL for
each of the five phases (Discover, Spec, Build, Verify, Ship), then
exits `0` if all five pass, `1` otherwise.

For machine-readable output (includes each phase's full resolved read
set, so the byte count and "no archive" claim are independently
checkable):

```
python3 shipflow-sample/measure.py --json
```

No dependencies beyond the Python 3 standard library.

# ShipFlow — Memory Budget Measurement

> This document describes the 3-layer memory model, defines per-phase read
> budgets, and lays out the methodology for verifying that ShipFlow's
> phase-skill reads actually fit the budget.
>
> **Status:** rebuilt and passing. The fixture (`shipflow-sample/`) and the
> measurement script (`measure.py`) that produced the original numbers in
> `handoff.md` did not transfer from Cowork, so both were rebuilt from this
> doc's methodology (not copied from the original — that fixture is gone).
> `python3 shipflow-sample/measure.py` now runs green: all five phases PASS
> within budget with zero archive leakage. See "Re-measured" below for the
> actual numbers from the rebuilt fixture.

---

## The model

ShipFlow organizes project knowledge into three layers with different read
cadences:

| Layer | Where | When read | Target size | Purpose |
|-------|-------|-----------|-------------|---------|
| **Hot**  | `CLAUDE.md` | Every session (auto) | < 2 KB | Pointer to Warm + conventions. |
| **Warm** | `docs/shipflow/{briefs,stories,decisions,releases}/` + `index.md` + `stack.md` | On demand, per phase | No hard cap; managed by archiving | Active product knowledge. |
| **Cold** | `docs/shipflow/archive/` | Only when explicitly asked | Unbounded | Shipped work. Kept out of default reads. |

The goal isn't to shrink files — it's to make sure each phase reads only the
subset of Warm that matters for the task at hand. Archiving is the mechanism
that keeps Warm from growing unbounded.

---

## Per-phase read budgets

These are the maximum bytes a phase's agents should read under normal
operation (i.e. one brief / one story in progress, not a bulk migration).

| Phase    | Budget | Reads typically include |
|----------|--------|-------------------------|
| Discover | ≤ 3 KB | `seed.md` (× round 1), `dialogue-<other>.md` × 2 (round 2), `answers.md` at synthesis. |
| Spec     | ≤ 6 KB | Brief under spec, `stack.md`, relevant ADRs (greps only), `brief-template.md`, `story-template.md`. |
| Build    | ≤ 5 KB | Story + linked brief + linked ADRs, `stack.md`. Source files read as needed but not counted here — they're the work. |
| Verify   | ≤ 3 KB | Story + linked brief (for success criteria). |
| Ship     | ≤ 3 KB | All stories under the release's brief (status check), brief itself, `stack.md`. |

**Rule of thumb:** if a phase is reading more than its budget, it's reading
something it shouldn't — almost always unrelated briefs or the archive.

---

## Baseline (from handoff)

These numbers were measured in Cowork against the original 26-file fixture,
per `handoff.md`. That fixture and script did not transfer, so these are
kept only as the historical reference point — not something the rebuilt
fixture reproduces byte-for-byte (the file contents are new; the file
*shape* — counts, section structure, budgets — follows the same
methodology below):

| Phase    | Measured | Budget | Status |
|----------|----------|--------|--------|
| Discover | 1.98 KB  | 3 KB   | PASS |
| Spec     | 4.48 KB  | 6 KB   | PASS |
| Build    | 3.52 KB  | 5 KB   | PASS |
| Verify   | 1.55 KB  | 3 KB   | PASS |
| Ship     | 2.29 KB  | 3 KB   | PASS |

Additional baseline facts from `handoff.md`:

- Zero archive leakage — no read against `docs/shipflow/archive/` during
  normal phase work.
- Hot layer (`CLAUDE.md`) stays under 2 KB in all sessions.

## Re-measured (rebuilt fixture, `<date>`)

Numbers below are from actually running `python3 shipflow-sample/measure.py`
against the rebuilt fixture (new content, same methodology and file shape
as the list in "Methodology" below) — not restated from handoff, not
hand-computed. Re-run the command yourself to reproduce:

| Phase    | Measured | Budget | # Files | Status |
|----------|----------|--------|---------|--------|
| Discover | 1.79 KB  | 3 KB   | 5       | PASS |
| Spec     | 4.61 KB  | 6 KB   | 5       | PASS |
| Build    | 3.35 KB  | 5 KB   | 4       | PASS |
| Verify   | 1.88 KB  | 3 KB   | 2       | PASS |
| Ship     | 2.78 KB  | 3 KB   | 5       | PASS |

`measure.py` exits `0`. Zero archive leakage confirmed programmatically
(the script asserts no `archive/` path appears in any phase's resolved
read set — see `--json` output for each phase's full read set). All
numbers use 1 KB = 1024 bytes.

These land close to but not identical to the Cowork baseline above, which
is expected — the rebuilt fixture's briefs/stories/ADRs are newly written
prose (a habit-tracker product, "Loopline"), not a recovery of the
original text. What the re-measurement actually confirms is the thing
that matters: realistic per-phase content of mature-project shape stays
within budget with no archive leakage, across all five phases.

---

## Methodology

Reproducing these numbers requires:

1. **A realistic fixture** — a simulated ShipFlow repo containing representative
   content at mature-project size. The original fixture had:
   - 1 `CLAUDE.md` (~1 KB)
   - 1 `stack.md`
   - 1 `index.md`
   - 2 briefs
   - 6 active stories (3 in flight, 3 ready)
   - 6 ADRs
   - 2 releases
   - 1 retro
   - 6 archived stories across two historical releases

2. **A measurement script** that, for each phase, simulates the narrow-read
   rule: determines which files that phase's agents *should* read, sums their
   bytes, and reports pass/fail against the budget.

3. **A verification of the "no archive leakage" property** — the script also
   confirms no path under `archive/` appears in any phase's read set.

### What the measurement script does (pseudocode)

```
for each phase in [Discover, Spec, Build, Verify, Ship]:
    inputs = resolve_narrow_read_set(phase, fixture)
    total_bytes = sum of file sizes in inputs
    archive_hits = [p for p in inputs if 'archive/' in p]

    assert total_bytes <= budget[phase]
    assert archive_hits == []
    report(phase, total_bytes, len(inputs), pass/fail)
```

### What "narrow read set" means per phase

- **Discover:** the current `discovery/<slug>/` directory only.
- **Spec:** the target brief, `stack.md`, ADRs matching grep hints from the
  brief's Constraints section, and the two template references.
- **Build:** one story, its linked brief, its linked ADRs, `stack.md`.
- **Verify:** one story and its linked brief.
- **Ship:** all stories matching `brief: BRIEF-NNN` frontmatter for the
  release, the brief itself, `stack.md`.

Any read outside that set is a budget violation — not because the bytes are
prohibitive but because it signals the agent didn't follow the narrow-read
contract.

---

## Next actions

1. ~~**Rebuild the fixture** at `shipflow-sample/`. Keep it realistic but not
   excessive — ~26 files is enough to test all five phases.~~ **Done.**
   26 core files (1 `CLAUDE.md`, `stack.md`, `index.md`, 2 briefs, 6 active
   stories, 6 ADRs, 2 releases, 1 retro, 6 archived stories) plus a
   `discovery/habit-templates/` dialogue dir, `shipflow.config.json`,
   `measure.py`, and a short `README.md`.
2. ~~**Port the measurement script** (`measure.py` or equivalent). Node would
   also work if Python isn't preferred on this machine.~~ **Done.**
   `shipflow-sample/measure.py`, stdlib-only Python 3, `--json` flag.
3. ~~**Re-run the table above** and check that the numbers still pass.~~
   **Done.** See "Re-measured (rebuilt fixture, `<date>`)" above — all
   five phases PASS, zero archive leakage, exit code 0.
4. **Add a stress test** — a fixture with 100 ADRs and 500 stories — to
   verify the model holds at mature-project scale. This is an open question
   in `handoff.md` and has **not** been tested (still open — out of scope
   for this rebuild, which targeted parity with the original ~26-file
   fixture, not the stress case).

#!/usr/bin/env python3
"""ShipFlow memory-budget measurement harness.

What this is
-------------
This script measures whether ShipFlow's five phases (Discover, Spec,
Build, Verify, Ship) read only their "narrow read set" of Warm-layer
files, and whether that read set stays under the phase's byte budget.
Both the budgets and the narrow-read-set rules are defined in
`shipflow-memory-measurement.md` (see "Per-phase read budgets" and
"What narrow read set means per phase"); this script is the
implementation of the pseudocode in that doc's "What the measurement
script does" section, run against the fixture in this directory.

What this is NOT
-----------------
- Not a quality/rubric scorer. It never judges whether a brief, story,
  or ADR is well written.
- Not a cost/latency evaluator. It counts bytes on disk, not tokens,
  API cost, or wall-clock time.
It is a memory-budget + narrow-read-set verifier, nothing more.

For each phase, in order:
    1. Resolve the narrow read set (which files that phase's agents
       should read for one unit of work — one brief, one story, etc.)
    2. Sum the bytes of those files.
    3. Check the sum against the phase's budget.
    4. Check that no path in the read set falls under `archive/`
       (the Cold layer must never leak into a normal phase read).

Mirrors this pseudocode from shipflow-memory-measurement.md:

    for each phase in [Discover, Spec, Build, Verify, Ship]:
        inputs = resolve_narrow_read_set(phase, fixture)
        total_bytes = sum of file sizes in inputs
        archive_hits = [p for p in inputs if 'archive/' in p]

        assert total_bytes <= budget[phase]
        assert archive_hits == []
        report(phase, total_bytes, len(inputs), pass/fail)

(Implemented below as boolean checks rather than raised `assert`s, so
the full report prints for all five phases before the script exits —
one violation shouldn't hide the other four results.)

Usage
-----
    python3 measure.py            # human-readable report table
    python3 measure.py --json     # machine-readable JSON

Exit code is 0 if all five phases pass, 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# Fixture layout
# --------------------------------------------------------------------------

SAMPLE_ROOT = Path(__file__).resolve().parent
DOCS = SAMPLE_ROOT / "docs" / "shipflow"

# Spec's narrow read set includes "the two template references"
# (brief-template.md, story-template.md). Those live in the real
# plugin, one directory up from this fixture — not duplicated here,
# so there's exactly one copy to keep in sync.
TEMPLATES_DIR = SAMPLE_ROOT.parent / "shipflow" / "references"

# 1 KB = 1024 bytes (KiB) throughout this script and in the
# measurement doc's tables — matches typical dev-tool file-size
# reporting, not the SI decimal kilobyte.
KB = 1024

BUDGETS = {
    "Discover": 3 * KB,
    "Spec": 6 * KB,
    "Build": 5 * KB,
    "Verify": 3 * KB,
    "Ship": 3 * KB,
}

PHASE_ORDER = ["Discover", "Spec", "Build", "Verify", "Ship"]

# Which brief/story each phase measures against in this fixture. A real
# invocation of a phase skill resolves its own target (newest approved
# brief, oldest ready story, etc.) — this script targets one concrete,
# realistic unit of work per phase so the same fixture always produces
# the same numbers.
DISCOVERY_DIR_FALLBACK = "habit-templates"  # used only if none found by date
SPEC_BRIEF_ID = "BRIEF-004"   # "Team habit boards" — currently moving through Spec
BUILD_STORY_ID = "STORY-0010"  # "Daily reminder email job" — currently in Build
SHIP_BRIEF_ID = "BRIEF-004"   # same brief's stories, about to ship as a release


# --------------------------------------------------------------------------
# Tiny stdlib-only markdown/frontmatter helpers
# --------------------------------------------------------------------------

def read_frontmatter(path: Path) -> tuple[dict, str]:
    """Parse a minimal `---\\nkey: value\\n---` frontmatter block.

    Returns (frontmatter_dict, body_text). No YAML dependency — every
    value in this fixture is a plain scalar or a `[a, b, c]` list
    written on one line, so a line-based split on the first `:` is
    enough.
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end].strip("\n")
    body = text[end + 4:]
    fm = {}
    for line in fm_text.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()
    return fm, body


def section(body: str, heading: str) -> str:
    """Return the text under a `## <heading>` section, up to the next
    `## ` heading or end of file."""
    pattern = rf"##\s+{re.escape(heading)}\s*\n(.*?)(?=\n##\s|\Z)"
    m = re.search(pattern, body, re.DOTALL | re.IGNORECASE)
    return m.group(1) if m else ""


def tag_list(raw: str) -> list[str]:
    """Parse a frontmatter `tags: [a, b, c]` value into lowercase tags."""
    raw = raw.strip().lstrip("[").rstrip("]")
    return [t.strip().lower() for t in raw.split(",") if t.strip()]


# --------------------------------------------------------------------------
# Fixture lookups
# --------------------------------------------------------------------------

def all_briefs() -> list[Path]:
    return sorted((DOCS / "briefs").glob("*.md"))


def all_stories() -> list[Path]:
    return sorted((DOCS / "stories").glob("*.md"))


def all_adrs() -> list[Path]:
    return sorted((DOCS / "decisions").glob("*.md"))


def find_brief(brief_id: str) -> Path:
    for p in all_briefs():
        fm, _ = read_frontmatter(p)
        if fm.get("id") == brief_id:
            return p
    raise FileNotFoundError(f"no brief with id {brief_id!r} under {DOCS / 'briefs'}")


def find_story(story_id: str) -> Path:
    for p in all_stories():
        fm, _ = read_frontmatter(p)
        if fm.get("id") == story_id:
            return p
    raise FileNotFoundError(f"no story with id {story_id!r} under {DOCS / 'stories'}")


def stories_for_brief(brief_id: str) -> list[Path]:
    out = []
    for p in all_stories():
        fm, _ = read_frontmatter(p)
        if fm.get("brief") == brief_id:
            out.append(p)
    return out


def adrs_matching_constraints(constraints_text: str) -> list[Path]:
    """Spec's grep-hint rule: an ADR is in-scope if any of its tags
    appears (case-insensitively) in the brief's Constraints text."""
    haystack = constraints_text.lower()
    hits = []
    for p in all_adrs():
        fm, _ = read_frontmatter(p)
        for tag in tag_list(fm.get("tags", "")):
            if tag in haystack or tag.replace("-", " ") in haystack:
                hits.append(p)
                break
    return hits


def adrs_linked_in_story(story_body: str) -> list[Path]:
    """Build's ADR-link rule: an explicit `ADR-NNN` citation in the
    story body (conventionally in `## Notes`)."""
    ids = sorted(set(re.findall(r"ADR-\d{3}", story_body)))
    paths = []
    for adr_id in ids:
        for p in all_adrs():
            fm, _ = read_frontmatter(p)
            if fm.get("id") == adr_id:
                paths.append(p)
    return paths


def current_discovery_dir() -> Path:
    """Discover's target: 'the current discovery/<slug>/ directory'.
    Picks the slug whose seed.md has the most recent `created` date;
    falls back to the fixture's only slug if dates are missing/tied.
    """
    discovery_root = DOCS / "discovery"
    candidates = [d for d in discovery_root.iterdir() if d.is_dir()]
    if not candidates:
        raise FileNotFoundError(f"no discovery/<slug>/ directories under {discovery_root}")

    def created_date(d: Path) -> str:
        seed = d / "seed.md"
        if seed.exists():
            fm, _ = read_frontmatter(seed)
            return fm.get("created", "")
        return ""

    candidates.sort(key=created_date)
    return candidates[-1] if created_date(candidates[-1]) else (
        discovery_root / DISCOVERY_DIR_FALLBACK
    )


# --------------------------------------------------------------------------
# Per-phase narrow-read-set resolvers
# --------------------------------------------------------------------------
# Each function returns the list of file paths that phase's agents
# should read for one unit of work, per shipflow-memory-measurement.md
# "What narrow read set means per phase".

def resolve_discover() -> list[Path]:
    # "The current discovery/<slug>/ directory only."
    return sorted(current_discovery_dir().glob("*.md"))


def resolve_spec() -> list[Path]:
    # "The target brief, stack.md, ADRs matching grep hints from the
    # brief's Constraints section, and the two template references."
    brief_path = find_brief(SPEC_BRIEF_ID)
    _, body = read_frontmatter(brief_path)
    constraints = section(body, "Constraints")
    inputs = [brief_path, DOCS / "stack.md"]
    inputs += adrs_matching_constraints(constraints)
    inputs += [
        TEMPLATES_DIR / "brief-template.md",
        TEMPLATES_DIR / "story-template.md",
    ]
    return inputs


def resolve_build() -> list[Path]:
    # "One story, its linked brief, its linked ADRs, stack.md."
    story_path = find_story(BUILD_STORY_ID)
    fm, body = read_frontmatter(story_path)
    brief_path = find_brief(fm["brief"])
    inputs = [story_path, brief_path]
    inputs += adrs_linked_in_story(body)
    inputs += [DOCS / "stack.md"]
    return inputs


def resolve_verify() -> list[Path]:
    # "One story and its linked brief."
    story_path = find_story(BUILD_STORY_ID)
    fm, _ = read_frontmatter(story_path)
    brief_path = find_brief(fm["brief"])
    return [story_path, brief_path]


def resolve_ship() -> list[Path]:
    # "All stories matching brief: BRIEF-NNN frontmatter for the
    # release, the brief itself, stack.md."
    brief_path = find_brief(SHIP_BRIEF_ID)
    inputs = stories_for_brief(SHIP_BRIEF_ID) + [brief_path, DOCS / "stack.md"]
    return inputs


_RESOLVERS = {
    "Discover": resolve_discover,
    "Spec": resolve_spec,
    "Build": resolve_build,
    "Verify": resolve_verify,
    "Ship": resolve_ship,
}


def resolve_narrow_read_set(phase: str) -> list[Path]:
    return _RESOLVERS[phase]()


# --------------------------------------------------------------------------
# Measurement + reporting
# --------------------------------------------------------------------------

def is_archive_path(p: Path) -> bool:
    return "archive" in p.parts


def measure_phase(phase: str) -> dict:
    inputs = resolve_narrow_read_set(phase)
    total_bytes = sum(p.stat().st_size for p in inputs)
    archive_hits = [p for p in inputs if is_archive_path(p)]
    budget = BUDGETS[phase]

    within_budget = total_bytes <= budget
    no_archive_leak = archive_hits == []
    passed = within_budget and no_archive_leak

    return {
        "phase": phase,
        "bytes": total_bytes,
        "kb": round(total_bytes / KB, 2),
        "files": len(inputs),
        "budget_bytes": budget,
        "budget_kb": round(budget / KB, 2),
        "within_budget": within_budget,
        "archive_hits": [str(p.relative_to(SAMPLE_ROOT.parent)) for p in archive_hits],
        "no_archive_leak": no_archive_leak,
        "pass": passed,
        "read_set": [str(p.relative_to(SAMPLE_ROOT.parent)) for p in inputs],
    }


def print_report(results: list[dict]) -> None:
    header = f"{'Phase':<10} {'Bytes':>8} {'KB':>7} {'#Files':>7} {'Budget':>9} {'Status':>8}"
    print(header)
    print("-" * len(header))
    for r in results:
        status = "PASS" if r["pass"] else "FAIL"
        budget_str = f"{r['budget_kb']:.2f}KB"
        print(
            f"{r['phase']:<10} {r['bytes']:>8} {r['kb']:>6.2f}K {r['files']:>7} "
            f"{budget_str:>9} {status:>8}"
        )
        if not r["within_budget"]:
            print(f"    over budget by {r['bytes'] - r['budget_bytes']} bytes")
        if not r["no_archive_leak"]:
            print(f"    archive leakage: {', '.join(r['archive_hits'])}")
    print("-" * len(header))
    all_pass = all(r["pass"] for r in results)
    print("ALL PHASES PASS" if all_pass else "AT LEAST ONE PHASE FAILED")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="ShipFlow memory-budget measurement harness (not a quality scorer).",
    )
    parser.add_argument(
        "--json", action="store_true", help="emit machine-readable JSON instead of the report table"
    )
    args = parser.parse_args()

    results = [measure_phase(phase) for phase in PHASE_ORDER]
    all_pass = all(r["pass"] for r in results)

    if args.json:
        # Includes each phase's full read_set so the archive-leakage
        # and narrow-read-set claims are independently auditable, not
        # just asserted.
        payload = {"phases": results, "all_pass": all_pass}
        print(json.dumps(payload, indent=2))
    else:
        print_report(results)

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())

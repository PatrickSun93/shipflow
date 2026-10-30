#!/usr/bin/env python3
"""ShipFlow plugin structure lint.

What this is
------------
A compiler-strict pass over the plugin's own definition files under
`shipflow/` — the same idea `/sf-lint` applies to a user project's
`docs/shipflow/` tree, pointed at the plugin itself. It catches the
manual-edit mistakes that make a plugin load wrong or spawn a ghost:
a SKILL.md whose frontmatter got clipped, an agent file renamed without
its `name:` following, a skill that spawns an agent that doesn't exist,
a hook pointing at a script that was moved.

What this is NOT
----------------
- Not a prompt-quality check. It never judges whether an agent prompt
  is well written or whether a skill's steps make sense.
- Not a token-budget check. The README's "agent prompts <=2000 tokens"
  convention is enforced by review, not here — a bytes/4 estimate would
  flag the two largest agents every run and teach people to ignore it.
- Not a substitute for loading the plugin in Claude Code
  (`claude --plugin-dir ./shipflow`). It only checks structure.

Checks
------
  1. plugin.json and marketplace.json parse, carry the required fields,
     and agree on the plugin version (they are bumped together so
     `/plugin update` sees new releases).
  2. Every `agents/*.md` opens with frontmatter whose lines are all
     `key: value`, with non-empty `name` and `description`; `name`
     matches the filename; `tools:` (if present) is a non-empty list.
  3. Every `skills/<dir>/SKILL.md` exists and has the same frontmatter
     shape; `name` matches the directory.
  4. Every agent reference in a skill or agent prompt
     (`subagent_type: "<name>"`, "Spawn `<name>`", "spawns <name>")
     resolves to a real agent file. Agents nothing references are
     reported as warnings.
  5. Every `/sf-<name>` mention inside the plugin and the top-level
     READMEs resolves to a real skill directory — the plugin's
     equivalent of `/sf-lint`'s dead-link check on index.md.
  6. hooks.json parses; every script it runs exists under the plugin
     and passes `bash -n`; scripts nothing runs are reported as
     warnings.

Usage
-----
    python3 scripts/lint_plugin.py
    python3 scripts/lint_plugin.py --plugin-dir path/to/shipflow

Findings are collected across all checks and reported once at the end
(don't stop on first failure — same rule as /sf-lint). Exit code is 0
if there are no errors (warnings alone don't fail), 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PLUGIN_DIR = REPO_ROOT / "shipflow"
MARKETPLACE_JSON = REPO_ROOT / ".claude-plugin" / "marketplace.json"

# Top-level docs that are kept current and so must not point at skills
# that no longer exist. handoff.md / shipflow-plan.md are historical logs
# and deliberately excluded — a rename shouldn't force edits to history.
ROOT_DOCS = ["README.md", "README.zh.md", "DESIGN.md"]

# Frontmatter keys Claude Code understands for each file type. Anything
# else is a warning, not an error: a new key in a newer Claude Code
# release shouldn't break CI, but a typo (`tool:` for `tools:`) should
# be visible.
AGENT_KEYS = {
    "name", "description", "tools", "disallowedTools", "model",
    "permissionMode", "skills", "hooks", "memory", "background",
    "isolation", "color", "maxTurns", "mcpServers", "effort",
}
SKILL_KEYS = {
    "name", "description", "allowed-tools", "argument-hint",
    "disable-model-invocation", "user-invocable", "model", "context",
    "agent", "hooks", "effort", "paths",
}
HOOK_EVENTS = {
    "SessionStart", "SessionEnd", "UserPromptSubmit", "PreToolUse",
    "PostToolUse", "PostToolUseFailure", "PermissionRequest",
    "Notification", "Stop", "SubagentStart", "SubagentStop", "PreCompact",
    "PostCompact", "Setup", "ConfigChange", "WorktreeCreate",
    "WorktreeRemove", "TaskCreated", "TaskCompleted", "Elicitation",
    "ElicitationResult", "InstructionsLoaded", "CwdChanged", "FileChanged",
    "TeammateIdle",
}

# A frontmatter line. `key:` with nothing after it is allowed (empty
# value, caught separately when the key is required); `key:value` with
# no space is not a YAML mapping and is flagged.
FM_LINE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s+(.*))?$")

# How skills and agents name the agent they spawn. All four forms occur
# in the repo; the first is the one Claude Code actually acts on.
AGENT_REF_PATTERNS = [
    re.compile(r'subagent_type:\s*["\']?(?:shipflow:)?([a-z0-9][a-z0-9-]*)'),
    re.compile(r"[Ss]pawn(?:s|ed)?\s+(?:the\s+)?(?:\*\*)?`([a-z0-9][a-z0-9-]*)`"),
    re.compile(r"[Ss]pawn(?:s|ed)?\s+the\s+([a-z0-9]+(?:-[a-z0-9]+)+)\s+agent\b"),
    re.compile(r"[Ss]pawns?\s+([a-z]+-[a-z-]+)"),
]
BACKTICK_TOKEN = re.compile(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`")

# `/sf-check-{brief,plan,build,ship}` is brace shorthand, not a skill name;
# the optional trailing `{` group lets us skip it.
SKILL_REF = re.compile(r"/sf-([a-z0-9-]+)(\{)?")

PLUGIN_ROOT_VAR = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}/(\S+)")


# --------------------------------------------------------------------------
# Findings
# --------------------------------------------------------------------------

@dataclass
class Finding:
    severity: str  # "error" | "warning"
    path: Path
    line: int | None
    issue: str

    def render(self) -> str:
        try:
            rel = self.path.relative_to(REPO_ROOT)
        except ValueError:
            rel = self.path
        loc = f"{rel}:{self.line}" if self.line else str(rel)
        return f"- {loc} — {self.issue}"


class Report:
    def __init__(self) -> None:
        self.findings: list[Finding] = []
        self.counts: dict[str, int] = {}

    def error(self, path: Path, line: int | None, issue: str) -> None:
        self.findings.append(Finding("error", path, line, issue))

    def warning(self, path: Path, line: int | None, issue: str) -> None:
        self.findings.append(Finding("warning", path, line, issue))

    def count(self, key: str, n: int = 1) -> None:
        self.counts[key] = self.counts.get(key, 0) + n

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "error"]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "warning"]


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def read_text(path: Path) -> str:
    # Checkouts on Windows-configured machines carry CRLF; normalise so
    # line-based checks behave the same everywhere.
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def parse_frontmatter(path: Path, report: Report) -> dict[str, tuple[str, int]]:
    """Return {key: (value, line_number)} for the `---` block at the top
    of `path`, recording an error for anything that isn't `key: value`."""
    lines = read_text(path).split("\n")
    if not lines or lines[0].strip() != "---":
        report.error(path, 1, "missing frontmatter (file must start with `---`)")
        return {}
    fm: dict[str, tuple[str, int]] = {}
    closed = False
    for lineno, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            closed = True
            break
        if not line.strip():
            continue
        m = FM_LINE.match(line)
        if not m:
            report.error(
                path, lineno,
                f"frontmatter line is not `key: value`: {line.strip()[:60]!r}",
            )
            continue
        key, value = m.group(1), (m.group(2) or "").strip()
        if key in fm:
            report.error(path, lineno, f"duplicate frontmatter key `{key}`")
        fm[key] = (value, lineno)
    if not closed:
        report.error(path, 1, "frontmatter never closed (no second `---`)")
    return fm


def require(fm: dict, path: Path, key: str, report: Report) -> str | None:
    if key not in fm:
        report.error(path, 1, f"frontmatter missing required `{key}`")
        return None
    value, lineno = fm[key]
    if not value:
        report.error(path, lineno, f"frontmatter `{key}` is empty")
        return None
    return value


def warn_unknown_keys(fm: dict, known: set[str], path: Path, report: Report) -> None:
    for key, (_, lineno) in fm.items():
        if key not in known:
            report.warning(path, lineno, f"unrecognised frontmatter key `{key}`")


def parse_list(raw: str) -> list[str]:
    """`Read, Write, Edit` or `[Read, Write]` -> ['Read', 'Write', ...]"""
    raw = raw.strip().lstrip("[").rstrip("]")
    return [t.strip() for t in raw.split(",") if t.strip()]


def line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def check_manifests(plugin_dir: Path, report: Report) -> None:
    plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
    if not plugin_json.exists():
        report.error(plugin_json, None, "missing plugin.json")
        return
    try:
        plugin = json.loads(read_text(plugin_json))
    except json.JSONDecodeError as e:
        report.error(plugin_json, e.lineno, f"invalid JSON: {e.msg}")
        return
    for key in ("name", "version", "description"):
        if not plugin.get(key):
            report.error(plugin_json, None, f"plugin.json missing `{key}`")

    if not MARKETPLACE_JSON.exists():
        report.warning(MARKETPLACE_JSON, None, "no marketplace.json (skipping version cross-check)")
        return
    try:
        marketplace = json.loads(read_text(MARKETPLACE_JSON))
    except json.JSONDecodeError as e:
        report.error(MARKETPLACE_JSON, e.lineno, f"invalid JSON: {e.msg}")
        return
    entries = [p for p in marketplace.get("plugins", []) if p.get("name") == plugin.get("name")]
    if not entries:
        report.error(MARKETPLACE_JSON, None, f"no plugins[] entry named `{plugin.get('name')}`")
        return
    entry = entries[0]
    source = MARKETPLACE_JSON.parent.parent / entry.get("source", "")
    if not source.is_dir():
        report.error(MARKETPLACE_JSON, None, f"plugins[].source `{entry.get('source')}` is not a directory")
    if entry.get("version") != plugin.get("version"):
        report.error(
            MARKETPLACE_JSON, None,
            f"version {entry.get('version')!r} != plugin.json {plugin.get('version')!r} "
            "(bump both — /plugin update keys off marketplace.json)",
        )


def check_agents(plugin_dir: Path, report: Report) -> set[str]:
    agents_dir = plugin_dir / "agents"
    files = sorted(agents_dir.glob("*.md"))
    if not files:
        report.error(agents_dir, None, "no agent files found")
    names: set[str] = set()
    for path in files:
        names.add(path.stem)
        report.count("agents")
        fm = parse_frontmatter(path, report)
        if not fm:
            continue
        name = require(fm, path, "name", report)
        require(fm, path, "description", report)
        if name and name != path.stem:
            report.error(path, fm["name"][1], f"name `{name}` does not match filename `{path.name}`")
        if "tools" in fm and not parse_list(fm["tools"][0]):
            report.error(path, fm["tools"][1], "`tools` is present but empty")
        warn_unknown_keys(fm, AGENT_KEYS, path, report)
    return names


def check_skills(plugin_dir: Path, report: Report) -> set[str]:
    skills_dir = plugin_dir / "skills"
    dirs = sorted(d for d in skills_dir.iterdir() if d.is_dir())
    if not dirs:
        report.error(skills_dir, None, "no skill directories found")
    names: set[str] = set()
    for d in dirs:
        names.add(d.name)
        report.count("skills")
        path = d / "SKILL.md"
        if not path.exists():
            report.error(path, None, "skill directory has no SKILL.md")
            continue
        fm = parse_frontmatter(path, report)
        if not fm:
            continue
        name = require(fm, path, "name", report)
        require(fm, path, "description", report)
        if name and name != d.name:
            report.error(path, fm["name"][1], f"name `{name}` does not match directory `{d.name}/`")
        warn_unknown_keys(fm, SKILL_KEYS, path, report)
    return names


def check_agent_refs(plugin_dir: Path, agents: set[str], report: Report) -> None:
    files = sorted(plugin_dir.glob("skills/**/*.md")) + sorted(plugin_dir.glob("agents/*.md"))
    referenced: set[str] = set()
    for path in files:
        text = read_text(path)
        for pattern in AGENT_REF_PATTERNS:
            for m in pattern.finditer(text):
                report.count("agent_refs")
                name = m.group(1)
                if name in agents:
                    referenced.add(name)
                else:
                    report.error(
                        path, line_of(text, m.start()),
                        f"spawns agent `{name}` but there is no agents/{name}.md",
                    )
        # A bare `name` in backticks (persona tables, reviewer lists) counts
        # as a reference for the orphan check, but a non-agent token in
        # backticks is not an error — it's usually a status or a flag.
        for m in BACKTICK_TOKEN.finditer(text):
            if m.group(1) in agents and m.group(1) != path.stem:
                referenced.add(m.group(1))
    for name in sorted(agents - referenced):
        report.warning(
            plugin_dir / "agents" / f"{name}.md", None,
            "agent is never referenced by any skill or other agent",
        )


def check_skill_refs(plugin_dir: Path, skills: set[str], report: Report) -> None:
    files = sorted(plugin_dir.rglob("*.md")) + sorted(plugin_dir.rglob("*.sh"))
    files += [REPO_ROOT / d for d in ROOT_DOCS if (REPO_ROOT / d).exists()]
    for path in files:
        text = read_text(path)
        for m in SKILL_REF.finditer(text):
            if m.group(2):  # brace shorthand like /sf-check-{brief,plan}
                continue
            report.count("skill_refs")
            name = "sf-" + m.group(1).rstrip("-")
            if name not in skills:
                report.error(
                    path, line_of(text, m.start()),
                    f"mentions `/{name}` but there is no skills/{name}/",
                )


def check_hooks(plugin_dir: Path, report: Report) -> None:
    hooks_json = plugin_dir / "hooks" / "hooks.json"
    scripts_dir = plugin_dir / "hooks" / "scripts"
    if not hooks_json.exists():
        report.warning(hooks_json, None, "no hooks.json (plugin ships no hooks)")
        return
    try:
        data = json.loads(read_text(hooks_json))
    except json.JSONDecodeError as e:
        report.error(hooks_json, e.lineno, f"invalid JSON: {e.msg}")
        return
    used: set[Path] = set()
    for event, groups in data.get("hooks", {}).items():
        if event not in HOOK_EVENTS:
            report.warning(hooks_json, None, f"unrecognised hook event `{event}`")
        for group in groups:
            for hook in group.get("hooks", []):
                command = hook.get("command", "")
                if hook.get("type") != "command" or not command:
                    report.error(hooks_json, None, f"{event}: hook has no command")
                    continue
                report.count("hook_commands")
                m = PLUGIN_ROOT_VAR.search(command)
                if not m:
                    report.warning(
                        hooks_json, None,
                        f"{event}: command does not use ${{CLAUDE_PLUGIN_ROOT}} — "
                        "will it resolve once installed?",
                    )
                    continue
                script = plugin_dir / m.group(1)
                if not script.exists():
                    report.error(hooks_json, None, f"{event}: script `{m.group(1)}` does not exist")
                    continue
                used.add(script.resolve())
                if script.suffix == ".sh":
                    proc = subprocess.run(
                        ["bash", "-n", str(script)], capture_output=True, text=True,
                    )
                    if proc.returncode != 0:
                        report.error(script, None, f"bash -n failed: {proc.stderr.strip()}")
    if scripts_dir.is_dir():
        for script in sorted(scripts_dir.iterdir()):
            if script.is_file() and script.resolve() not in used:
                report.warning(script, None, "script is not referenced by hooks.json")


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Structural lint for the ShipFlow plugin (not a prompt-quality check).",
    )
    parser.add_argument(
        "--plugin-dir", type=Path, default=DEFAULT_PLUGIN_DIR,
        help=f"plugin root to lint (default: {DEFAULT_PLUGIN_DIR.relative_to(REPO_ROOT)}/)",
    )
    args = parser.parse_args()
    plugin_dir: Path = args.plugin_dir.resolve()
    if not plugin_dir.is_dir():
        print(f"error: {plugin_dir} is not a directory", file=sys.stderr)
        return 1

    report = Report()
    check_manifests(plugin_dir, report)
    agents = check_agents(plugin_dir, report)
    skills = check_skills(plugin_dir, report)
    check_agent_refs(plugin_dir, agents, report)
    check_skill_refs(plugin_dir, skills, report)
    check_hooks(plugin_dir, report)

    errors, warnings = report.errors, report.warnings
    c = report.counts
    print(f"# lint_plugin report — {plugin_dir.name}/")
    print()
    if errors:
        print(f"## Errors ({len(errors)})")
        for f in errors:
            print(f.render())
        print()
    if warnings:
        print(f"## Warnings ({len(warnings)})")
        for f in warnings:
            print(f.render())
        print()
    print("## Summary")
    print(f"- Agents scanned: {c.get('agents', 0)}")
    print(f"- Skills scanned: {c.get('skills', 0)}")
    print(f"- Agent references checked: {c.get('agent_refs', 0)}")
    print(f"- Skill references checked: {c.get('skill_refs', 0)}")
    print(f"- Hook commands checked: {c.get('hook_commands', 0)}")
    print(f"- Errors: {len(errors)}")
    print(f"- Warnings: {len(warnings)}")
    if not errors and not warnings:
        print()
        print("✓ No issues found.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

"""Validate a prepared benchmark workspace before an agent run.

This checks filesystem-layout isolation, not OS-level sandboxing. The workspace
root must live in a separate directory tree from the Signal repository; the
workspace itself must expose only the files allowed for its condition.

Usage:
    python benchmarks/scripts/validate_workspace.py \
        --workspace-root C:/signal-benchmark-workspaces \
        --agent claude --condition signal --case plant_growth
"""
import argparse
import sys
from pathlib import Path

from prepare_workspace import (
    AGENTS,
    CONDITIONS,
    REPO_ROOT,
    SIGNAL_PAYLOAD,
    SKILL_ROOT_BY_AGENT,
    validate_workspace_root,
)

ALWAYS_FORBIDDEN_NAMES = {
    "acceptance.md",
    "score.json",
    ".git",
    "benchmarks",
    "tests",
    "lab",
}


def find_violations(workspace: Path, agent: str, condition: str) -> list[str]:
    violations = []

    if not workspace.is_dir():
        return [f"workspace does not exist: {workspace}"]

    all_paths = list(workspace.rglob("*"))
    names_present = {p.name for p in all_paths}

    for forbidden in ALWAYS_FORBIDDEN_NAMES:
        if forbidden in names_present:
            violations.append(f"forbidden path present: {forbidden}")

    own_skill_root = SKILL_ROOT_BY_AGENT[agent].split("/")[0]
    other_skill_roots = {SKILL_ROOT_BY_AGENT[a].split("/")[0] for a in AGENTS} - {own_skill_root}

    if condition == "baseline":
        for forbidden in (
            "SKILL.md",
            "CONTRACT.md",
            "recipes",
            "ingredients",
            "components",
            "references",
            "themes",
            "intents",
        ):
            if forbidden in names_present:
                violations.append(f"baseline workspace can see Signal: {forbidden}")
        for root in {own_skill_root} | other_skill_roots:
            if (workspace / root).exists():
                violations.append(f"baseline workspace has a skill directory: {root}")
        allowed_top = {"data.csv", "prompt.txt"}
        top_level = {p.name for p in workspace.iterdir()}
        extra = top_level - allowed_top
        if extra:
            violations.append(f"unexpected top-level entries in baseline workspace: {sorted(extra)}")

    elif condition == "signal":
        for root in other_skill_roots:
            if (workspace / root).exists():
                violations.append(f"signal workspace exposes another agent's skill root: {root}")

        skill_dir = workspace / SKILL_ROOT_BY_AGENT[agent] / "signal"
        if not (skill_dir / "SKILL.md").is_file():
            violations.append(f"signal workspace missing SKILL.md at native path: {skill_dir}")

        expected = {str((skill_dir / rel).resolve()) for rel in SIGNAL_PAYLOAD}
        actual_files = (
            {str(p.resolve()) for p in skill_dir.rglob("*") if p.is_file()}
            if skill_dir.is_dir()
            else set()
        )
        extra_files = actual_files - expected
        missing_files = expected - actual_files
        if extra_files:
            violations.append(f"skill payload has unexpected files: {sorted(extra_files)}")
        if missing_files:
            violations.append(f"skill payload missing expected files: {sorted(missing_files)}")

        allowed_top = {"data.csv", "prompt.txt", own_skill_root}
        top_level = {p.name for p in workspace.iterdir()}
        extra = top_level - allowed_top
        if extra:
            violations.append(f"unexpected top-level entries in signal workspace: {sorted(extra)}")

    return violations


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace-root",
        required=True,
        type=Path,
        help="External root used by prepare_workspace.py.",
    )
    parser.add_argument("--agent", required=True, choices=AGENTS)
    parser.add_argument("--condition", required=True, choices=CONDITIONS)
    parser.add_argument("--case", required=True)
    args = parser.parse_args()

    try:
        root = validate_workspace_root(args.workspace_root)
    except SystemExit as exc:
        print(f"FAIL: invalid workspace root: {exc}")
        sys.exit(1)

    workspace = root / args.agent / args.condition / args.case
    violations = find_violations(workspace, args.agent, args.condition)

    if violations:
        print(f"FAIL: {workspace}")
        for violation in violations:
            print(f"  - {violation}")
        sys.exit(1)

    print(f"PASS: {workspace} ({args.agent}/{args.condition}/{args.case})")
    print(f"repository isolated from workspace root: {REPO_ROOT.resolve()} != {root}")


if __name__ == "__main__":
    main()

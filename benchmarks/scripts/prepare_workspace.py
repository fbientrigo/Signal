"""Build one isolated benchmark workspace under an explicit external root.

baseline  -> data.csv + prompt.txt only.
signal    -> data.csv + prompt.txt + the minimal Signal skill payload,
             installed at the native project-skill path for that agent.

The workspace is wiped and rebuilt on every call. The workspace root must be
outside the Signal repository tree and must not be an ancestor of the Signal
repository. This provides filesystem-layout isolation; it is not an OS sandbox.

Usage:
    python benchmarks/scripts/prepare_workspace.py \
        --workspace-root C:/signal-benchmark-workspaces \
        --agent claude --condition signal --case plant_growth
"""
import argparse
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CASES_DIR = REPO_ROOT / "benchmarks" / "cases"

AGENTS = ("claude", "codex", "antigravity")
CONDITIONS = ("baseline", "signal")

SKILL_ROOT_BY_AGENT = {
    "claude": ".claude/skills",
    "codex": ".agents/skills",
    "antigravity": ".agents/skills",
}

SIGNAL_PAYLOAD = [
    "SKILL.md",
    "CONTRACT.md",
    "recipes/_TEMPLATE.md",
    "recipes/categorical_comparison.md",
    "recipes/distribution_overview.md",
    "recipes/focus_in_context.md",
    "recipes/relationship_overview.md",
    "recipes/trend_with_uncertainty.md",
    "ingredients/axes.md",
    "ingredients/color.md",
    "ingredients/distribution.md",
    "ingredients/emphasis.md",
    "ingredients/layout.md",
    "ingredients/README.md",
    "ingredients/relationship.md",
    "ingredients/trend.md",
    "ingredients/uncertainty.md",
    "references/chart_selection.md",
    "references/scientific_integrity.md",
    "themes/README.md",
    "themes/signal_style.py",
]


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def validate_workspace_root(workspace_root: Path) -> Path:
    root = workspace_root.expanduser().resolve()
    repo = REPO_ROOT.resolve()

    if root == repo:
        raise SystemExit("workspace root must not be the Signal repository")
    if _is_relative_to(root, repo):
        raise SystemExit(f"workspace root must be outside the Signal repository: {root}")
    if _is_relative_to(repo, root):
        raise SystemExit(
            "workspace root must not be an ancestor of the Signal repository; "
            f"choose a separate directory tree: {root}"
        )

    return root


def build_workspace(
    workspace_root: Path,
    agent: str,
    condition: str,
    case: str,
) -> Path:
    root = validate_workspace_root(workspace_root)

    case_dir = CASES_DIR / case
    data_csv = case_dir / "data.csv"
    prompt_txt = case_dir / "prompt.txt"
    if not data_csv.is_file() or not prompt_txt.is_file():
        raise SystemExit(f"case '{case}' is missing data.csv or prompt.txt under {case_dir}")

    workspace = root / agent / condition / case
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True)

    shutil.copy2(data_csv, workspace / "data.csv")
    shutil.copy2(prompt_txt, workspace / "prompt.txt")

    skill_dir = None
    if condition == "signal":
        skill_dir = workspace / SKILL_ROOT_BY_AGENT[agent] / "signal"
        for rel in SIGNAL_PAYLOAD:
            src = REPO_ROOT / rel
            dst = skill_dir / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    print(f"repository : {REPO_ROOT.resolve()}")
    print(f"root       : {root}")
    print(f"workspace  : {workspace}")
    print(f"prompt     : {workspace / 'prompt.txt'}")
    print(f"data       : {workspace / 'data.csv'}")
    if skill_dir is not None:
        print(f"skill      : {skill_dir}")
    print(f"agent/condition/case : {agent}/{condition}/{case}")
    return workspace


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace-root",
        required=True,
        type=Path,
        help="External root for generated workspaces; must be in a separate directory tree from the Signal repo.",
    )
    parser.add_argument("--agent", required=True, choices=AGENTS)
    parser.add_argument("--condition", required=True, choices=CONDITIONS)
    parser.add_argument("--case", required=True)
    args = parser.parse_args()
    build_workspace(args.workspace_root, args.agent, args.condition, args.case)


if __name__ == "__main__":
    main()

"""Hardened benchmark runner helper.

Provides:
1. True workspace isolation (fresh directories outside the repo).
2. Strict payload control (no acceptance.md or repo leak).
3. Blind evaluation package generation (candidate_A vs candidate_B).
4. Unblinding mapping.
"""

import json
import os
import random
import shutil
import time
from pathlib import Path

REPO_ROOT = Path("C:/Users/Asus/Documents/code/3_products/signal").resolve()
BENCH_ROOT = REPO_ROOT / "benchmarks"
CASES_DIR = BENCH_ROOT / "cases"
COMMON_BRIEF = BENCH_ROOT / "common_brief.txt"

# Scratch base outside the main repo for full physical isolation
SCRATCH_BASE = Path("C:/Users/Asus/.gemini/antigravity-cli/brain/2e5fc834-dd2c-4d2e-8be6-14c38974dd26/scratch/benchmark_hardened")


def setup_isolated_workspace(case_name: str, condition: str, run_id: str) -> Path:
    """Create a completely isolated workspace containing only permitted files."""
    ws_dir = SCRATCH_BASE / "workspaces" / run_id
    if ws_dir.exists():
        shutil.rmtree(ws_dir)
    ws_dir.mkdir(parents=True, exist_ok=True)

    case_dir = CASES_DIR / case_name
    if not case_dir.exists():
        raise FileNotFoundError(f"Case {case_name} not found")

    # 1. Assembled prompt (common_brief + case prompt)
    brief = COMMON_BRIEF.read_text(encoding="utf-8").strip()
    case_prompt = (case_dir / "prompt.txt").read_text(encoding="utf-8").strip()
    assembled = (
        f"{brief}\n\n{case_prompt}\n\n"
        f"OUTPUT CONTRACT:\n"
        f"- Write your complete, runnable plotting code directly to plot.py\n"
        f"- Execute plot.py to produce plot.png\n"
        f"- The first rendered figure is your attempt 1 submission\n"
        f"- Do NOT create intermediate test scripts or scratch files\n"
    )
    (ws_dir / "prompt.txt").write_text(assembled, encoding="utf-8")

    # 2. Case data
    shutil.copy2(case_dir / "data.csv", ws_dir / "data.csv")

    # 3. Clarification is withheld unless agent asks via clarification protocol

    # 4. If Signal condition, copy ONLY the Signal skill knowledge base
    if condition == "signal":
        signal_skill_dir = ws_dir / "signal_skill"
        signal_skill_dir.mkdir(parents=True, exist_ok=True)
        # Copy SKILL.md, ingredients, recipes, references, themes
        shutil.copy2(REPO_ROOT / "SKILL.md", signal_skill_dir / "SKILL.md")
        for folder in ["ingredients", "recipes", "references", "themes"]:
            src_folder = REPO_ROOT / folder
            if src_folder.exists():
                shutil.copytree(src_folder, signal_skill_dir / folder)

    # 5. Metadata
    meta = {
        "run_id": run_id,
        "case": case_name,
        "condition": condition,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (ws_dir / "run_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    return ws_dir


def create_blind_bundle(case_name: str, run_a_dir: Path, run_b_dir: Path) -> dict:
    """Create randomized candidate_A and candidate_B for blind scoring of a specific case."""
    blind_dir = SCRATCH_BASE / "blind_evaluation" / case_name
    if blind_dir.exists():
        shutil.rmtree(blind_dir)
    blind_dir.mkdir(parents=True, exist_ok=True)

    cand_a_dir = blind_dir / "candidate_A"
    cand_b_dir = blind_dir / "candidate_B"
    cand_a_dir.mkdir(parents=True, exist_ok=True)
    cand_b_dir.mkdir(parents=True, exist_ok=True)

    runs = [("A", run_a_dir), ("B", run_b_dir)]
    # Random coin flip for blind assignment
    flip = random.choice([True, False])
    if flip:
        mapping = {
            "candidate_A": {"source_run": run_a_dir.name, "condition": json.loads((run_a_dir / "run_meta.json").read_text())["condition"]},
            "candidate_B": {"source_run": run_b_dir.name, "condition": json.loads((run_b_dir / "run_meta.json").read_text())["condition"]},
        }
        shutil.copy2(run_a_dir / "plot.py", cand_a_dir / "candidate_A.py")
        shutil.copy2(run_a_dir / "plot.png", cand_a_dir / "candidate_A.png")
        shutil.copy2(run_b_dir / "plot.py", cand_b_dir / "candidate_B.py")
        shutil.copy2(run_b_dir / "plot.png", cand_b_dir / "candidate_B.png")
    else:
        mapping = {
            "candidate_A": {"source_run": run_b_dir.name, "condition": json.loads((run_b_dir / "run_meta.json").read_text())["condition"]},
            "candidate_B": {"source_run": run_a_dir.name, "condition": json.loads((run_a_dir / "run_meta.json").read_text())["condition"]},
        }
        shutil.copy2(run_b_dir / "plot.py", cand_a_dir / "candidate_A.py")
        shutil.copy2(run_b_dir / "plot.png", cand_a_dir / "candidate_A.png")
        shutil.copy2(run_a_dir / "plot.py", cand_b_dir / "candidate_B.py")
        shutil.copy2(run_a_dir / "plot.png", cand_b_dir / "candidate_B.png")

    # Store mapping secretly for unblinding later
    mapping_file = blind_dir / "secret_unblinding_map.json"
    mapping_file.write_text(json.dumps(mapping, indent=2), encoding="utf-8")

    return mapping


if __name__ == "__main__":
    print("Hardened runner helper loaded.")

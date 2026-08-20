"""Prepare an isolated working directory for a single benchmark run.

Usage:
    python run_setup.py <case> <condition> [--signal-sha SHA]

Creates benchmarks/runs/<run-id>/ with:
    run.json        – metadata
    data.csv        – copy of case data
    prompt.txt      – assembled prompt (common_brief + case prompt)
    clarification.txt – if applicable

The run directory is ready for the agent. After the agent finishes,
the scorer expects plot.py, plot.png, stdout.txt, and transcript.txt
to be added to the same directory.
"""

import argparse
import json
import os
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path

BENCH_ROOT = Path(__file__).resolve().parent.parent
CASES_DIR = BENCH_ROOT / "cases"
RUNS_DIR = BENCH_ROOT / "runs"
COMMON_BRIEF = BENCH_ROOT / "common_brief.txt"

VALID_CASES = [
    "temperature",
    "plant_growth",
    "ab_experiment",
    "categorical_uncertainty",
    "weighted_signal_background",
    "misleading_transform",
    "irregular_parameter_scan",
]


def main():
    parser = argparse.ArgumentParser(description="Set up a benchmark run directory")
    parser.add_argument("case", choices=VALID_CASES)
    parser.add_argument("condition", choices=["baseline", "signal"])
    parser.add_argument("--signal-sha", default=None, help="Signal commit SHA (required for signal condition)")
    parser.add_argument("--model", default="unknown", help="Model/agent identifier")
    args = parser.parse_args()

    if args.condition == "signal" and not args.signal_sha:
        parser.error("--signal-sha is required for signal condition")

    case_dir = CASES_DIR / args.case
    if not case_dir.exists():
        parser.error(f"Case directory not found: {case_dir}")

    # Generate run ID
    ts = datetime.now(timezone.utc)
    run_id = f"{args.case}_{args.condition}_{ts.strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:6]}"
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    # Copy data
    for f in case_dir.iterdir():
        if f.name in ("data.csv",):
            shutil.copy2(f, run_dir / f.name)

    # Assemble prompt: common_brief + case prompt
    brief = COMMON_BRIEF.read_text(encoding="utf-8").strip()
    case_prompt = (case_dir / "prompt.txt").read_text(encoding="utf-8").strip()
    assembled = f"{brief}\n\n{case_prompt}\n"
    (run_dir / "prompt.txt").write_text(assembled, encoding="utf-8")

    # Copy clarification if present
    clar = case_dir / "clarification.txt"
    if clar.exists():
        shutil.copy2(clar, run_dir / "clarification.txt")

    # Write run.json
    meta = {
        "run_id": run_id,
        "case": args.case,
        "condition": args.condition,
        "signal_sha": args.signal_sha,
        "model": args.model,
        "timestamp_utc": ts.isoformat(),
        "status": "prepared",
    }
    (run_dir / "run.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(f"Run directory ready: {run_dir}")
    print(f"Run ID: {run_id}")
    return run_dir


if __name__ == "__main__":
    main()

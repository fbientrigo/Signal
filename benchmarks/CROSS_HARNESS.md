# Cross-harness execution protocol

This document describes how to repeat the frozen Baseline-vs-Signal
benchmark under Codex and Claude Code. The AGY experiment has been
completed and its results are in `results/agy/`.

## Prerequisites

1. The exact same benchmark cases in `benchmarks/cases/`.
2. The exact same `common_brief.txt`.
3. The exact same `edit_task.txt`.
4. The exact same `visual_economy_rubric.md`.
5. Signal at the commit recorded in each result's `signal_commit` field,
   unless explicitly testing a newer version.

## Execution steps (per harness)

For harness H in {codex, claude}:

### 1. Prepare workspaces

```bash
python benchmarks/scripts/prepare_workspace.py \
  --agent H --condition baseline --case <case_name>
python benchmarks/scripts/prepare_workspace.py \
  --agent H --condition signal --case <case_name>
```

### 2. Run each case

For each of the 7 cases:

- temperature
- plant_growth
- ab_experiment
- categorical_uncertainty
- misleading_transform
- irregular_parameter_scan
- weighted_signal_background

Run baseline and signal in randomized order, close in time.
Use the harness's native execution.

**First-attempt policy**: the first rendered figure is the submission.
No human correction before scoring `accept@1`.

**Clarification policy**: if the case provides `clarification.txt` and
the agent asks the relevant question, provide the canned answer.

### 3. Collect artifacts

For each run, save to `benchmarks/runs/<run_id>/`:

```text
run.json       — metadata (see run.template.json)
plot.py        — generated plotting code
plot.png       — rendered figure
score.json     — frozen scientific scores
stdout.txt     — execution output
```

### 4. Measure code economy

```bash
python benchmarks/scripts/measure_plot.py <run_dir>/plot.py --json
```

### 5. Run standardized edit task

Apply `edit_task.txt` to each plot.py using the same harness/model
that generated it. Record:

- edit_success (5 checks in edit_task.txt)
- edit_regression (data/uncertainty/normalization changed?)
- lines_touched (unified diff count)
- edit_turns (corrective turns after initial instruction)
- edit_wall_clock (if reliably available)

### 6. Blind visual economy review

For each case pair (baseline vs signal):

1. Randomize assignment to candidate_A and candidate_B.
2. Present both rendered figures and the case prompt to a reviewer.
3. Apply the rubric in `visual_economy_rubric.md`.
4. Record scores before unblinding.

### 7. Token accounting

Record native harness token telemetry if available.
If not available, record null with source "not_exposed".

### 8. Write result records

Create one JSON file per run in `benchmarks/results/<harness>/`
following the schema in `ECONOMY.md`.

### 9. Do NOT

- Regenerate existing AGY results.
- Modify scientific scores from any harness.
- Compare harnesses as primary results.
- Combine metrics into composite scores.
- Estimate tokens from character/line counts.

## Result file naming

```text
benchmarks/results/codex/<case>_<condition>.json
benchmarks/results/claude/<case>_<condition>.json
```

## Analysis

After all three harnesses are complete:

```text
AGY:   Baseline vs Signal
Codex: Baseline vs Signal
Claude: Baseline vs Signal
```

Then inspect whether the Signal effect replicates across harnesses.

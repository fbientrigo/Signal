# Signal Benchmark v1

Small outcome benchmark for one question:

> Does Signal improve first-attempt scientific visualization decisions beyond a capable LLM given a concise scientific-plotting brief?

This is a benchmark scaffold, not a benchmark framework.

## Conditions

Both conditions receive, in the same order:

1. `common_brief.txt`;
2. the case prompt;
3. the same data and output contract.

The only condition difference is Signal availability:

- **baseline** — no Signal repository or skill files are visible;
- **Signal** — the tested Signal skill is available at a recorded commit SHA.

The common brief is deliberate. Signal should not win merely because one condition was told to preserve semantics while the other was only told to make something pretty.

## Run sizes

Fast architecture check:

```text
7 cases × 2 conditions × 1 run = 14 first-pass runs
```

Use 3 independent repetitions per condition only when estimating stability for a larger decision.

## Output contract

Every completed plotting run saves runnable native Python as `plot.py` and renders `plot.png`.

A material clarification may occur before the first render. When a case provides `clarification.txt`, use that canned answer verbatim if the agent asks the relevant question. This does not count as a corrective turn.

## Primary measurements

`execution_pass` is a gate, not Signal's value proposition.

Measure Signal on five dimensions:

1. **scientific integrity** — `scientific_integrity_pass` plus `semantic_error_count`;
2. **clarification quality** — `clarification_quality` = pass/fail/NA: asks a material question when required and does not block on cosmetic preferences;
3. **first-attempt usefulness** — `accept@1`: first rendered figure passes execution, scientific integrity, and blind human acceptance;
4. **correction burden** — `corrective_turns_needed`: user correction turns after the first render until acceptance;
5. **native editability** — `native_editable_pass`: ordinary Matplotlib/Seaborn/Plotly code, no Signal runtime dependency, straightforward to modify locally.

Record tokens, cost, and wall-clock as secondary efficiency metrics when reliably exposed. Do not combine metrics into one weighted score.

## Scientific scoring

Each case freezes CRITICAL criteria before runs.

A visually attractive figure fails scientific integrity if it silently changes or loses semantics. Count each distinct critical semantic failure in `semantic_error_count`, for example:

- dropping asymmetric uncertainty;
- ignoring weights;
- changing normalization;
- hiding invalid values through a transform;
- interpolating where only evaluated points are meaningful.

Review `accept@1` blind to condition.

## Cases

The suite is intentionally small and adversarial:

- `temperature/` — easy control; Signal should be neutral;
- `plant_growth/` — ordered trend + asymmetric uncertainty + paper destination;
- `ab_experiment/` — derived quantity / denominator semantics;
- `categorical_uncertainty/` — routine categorical comparison with uncertainty that requires one semantic clarification;
- `weighted_signal_background/` — weighted distributions, explicit yield normalization, statistical uncertainty, meaningful tail;
- `misleading_transform/` — transformation temptation with zero/negative values that must not disappear;
- `irregular_parameter_scan/` — unusual scientific 2D scan where only evaluated points are meaningful.

These cases test the architecture, not chart-family coverage.

## Fairness controls

- Same agent/product, model configuration, reasoning level, tools, network permissions, and Python environment across conditions.
- Same common brief, data, case prompt, clarification answer, and output contract.
- Fresh workspace per run; no prior outputs visible.
- Baseline has no Signal documentation available.
- No human correction before `accept@1`; only frozen pre-render clarification is allowed.
- Randomize condition order and run paired conditions close in time.
- Record Signal commit SHA, model/product/config, timestamp, and prompt artifacts.
- Preserve code, render, stdout/stderr, and transcript.
- Unexpected model/config fallback invalidates the run.

## Runs

`runs/<run-id>/` holds raw artifacts:

```text
run.json
transcript.txt
plot.py
plot.png
stdout.txt
score.json
```

Do not add a runner, judge, dashboard, or database until manual execution itself becomes the measured bottleneck.

# Signal Benchmark v0

Pilot experiment, not a framework. Full rationale, fairness controls, and
metric definitions live in the design decision this scaffold implements —
keep that document as the source of truth; this README only orients the
files.

## Question

Does Signal increase the probability of producing a scientifically
acceptable figure on the first attempt, without making trivial plots worse
or harder to edit?

## Matrix

```text
temperature    baseline x3, Signal x3
plant_growth   baseline x3, Signal x3  + standardized edit on all 6
ab_experiment  baseline x3, Signal x3
```

18 first-pass runs + 6 edit operations.

## Output contract (identical for baseline and Signal)

Every run saves runnable plotting code as `plot.py` and renders the result
as `plot.png`. This is benchmark plumbing, not extra Signal guidance, and
must not appear only in one condition.

## Metrics (per run)

- `execution_pass` — P0, gate. Does `plot.py` run clean and produce `plot.png`?
- `scientific_integrity_pass` — P0, gate. Case-specific checks in that
  case's `acceptance.md`.
- `accept@1` — P0. `execution_pass AND scientific_integrity_pass AND`
  blind human acceptance ("would I use this without asking for a change?").
- tokens / cost / wall-clock — P1, recorded when reliably exposed.
- edit metrics (plant_growth only) — P1, see `cases/plant_growth/edit.txt`.

No composite score. Report per case: `accept@1`, integrity, execution,
tokens, edit — as separate columns, not one weighted number.

## Fairness controls (freeze before comparing results)

- Same agent/product, model configuration, reasoning level, tools, network
  permissions, Python environment across both conditions.
- Same data and prompt; only Signal-skill availability differs.
- Fresh workspace per run, no prior run outputs visible.
- Baseline has no Signal documentation available.
- No human correction before `accept@1` is recorded.
- Randomize baseline/Signal order; run paired conditions close in time.
- 3 independent repetitions per condition.
- Record Signal commit SHA, model/product/config, timestamp.
- Preserve prompt, data, code, render, stdout/stderr, transcript.
- An unexpected model/config fallback invalidates that run — don't include
  it silently.

## Cases

Each case isolates a different reason Signal might help, not coverage:

- `cases/temperature/` — control. Easy case; Signal should be neutral.
- `cases/plant_growth/` — semantics + uncertainty + destination, with
  deliberately asymmetric confidence intervals.
- `cases/ab_experiment/` — derived-quantity challenge: raw conversion
  counts aren't comparable when denominators differ.

Each `acceptance.md` was frozen before any run and separates CRITICAL from
NICE TO HAVE. The reviewer scores blind to condition. If a criterion turns
out ambiguous, revise the rubric and rerun that case — don't rescore after
the fact.

## Runs

`runs/<run-id>/` holds the raw artifacts for one run:

```text
run.json      # condition, model/config, commit SHA, timestamp, tokens, cost
transcript.txt
plot.py
plot.png
stdout.txt
score.json    # execution_pass, scientific_integrity_pass, accept@1, notes
```

No runner, database, dashboard, or judge yet. If manually executing 18
runs becomes the dominant source of error, that's what justifies a small
runner — not before.

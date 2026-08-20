# Visual / code economy benchmark

Second benchmark dimension added to the existing scientific benchmark.
The scientific metrics and scores remain frozen and unchanged.

## Question

> Given a scientifically acceptable figure, does Signal produce a solution
> that is simpler and easier to modify?

This dimension is called **visual/code economy**, not aesthetics.

## Relationship to scientific benchmark

The scientific benchmark answers:

> Does Signal improve first-attempt scientific visualization decisions?

The economy benchmark answers a different question and uses different
metrics. Both use the same completed runs. Economy metrics are never
retroactively applied to change scientific scores.

## Metrics

### Code economy (descriptive, from original first-attempt code)

| Metric                  | Definition                                                |
| ----------------------- | --------------------------------------------------------- |
| `plot_loc`              | Non-empty, non-comment Python lines in plot.py            |
| `number_of_axes`        | Matplotlib/Plotly plotting panels (insets count; colorbars do not) |
| `helper_function_count` | User-defined Python functions in the plotting script      |

**Counting rule for `plot_loc`**: strip each line, skip lines that are
empty after stripping, skip lines whose stripped form starts with `#`.
Docstrings (triple-quote blocks) are NOT excluded — they contain
meaningful code structure decisions and their presence is a legitimate
economy signal.

### Editability (from standardized edit task)

| Metric            | Definition                                                           |
| ----------------- | -------------------------------------------------------------------- |
| `edit_success`    | All 5 edit verification checks pass (see `edit_task.txt`)            |
| `edit_regression` | Edit accidentally changes data, uncertainty, normalization, etc.     |
| `lines_touched`   | Deterministic line diff (unified diff changed-line count)            |
| `edit_turns`      | User correction turns after initial edit instruction                 |
| `edit_wall_clock` | Wall-clock seconds when reliably available; null otherwise           |

### Visual economy (blind paired review)

Two questions per case pair, reviewed blind to condition:

1. **Question fit**: Which candidate lets the reader answer the scientific
   question more directly? (A / B / Tie)

2. **Unnecessary structure**: Does either candidate introduce visual
   structure not needed to answer the question? (none / minor / substantial)

Full rubric: `visual_economy_rubric.md`

### Token accounting

| Field           | Source                                     |
| --------------- | ------------------------------------------ |
| `input_tokens`  | Native harness telemetry only              |
| `output_tokens` | Native harness telemetry only              |
| `total_tokens`  | Native harness telemetry only              |
| `cached_tokens` | Native harness telemetry only              |

Signal's loaded context (SKILL.md, ingredients, recipes, references)
counts toward Signal's cost. Do not exclude it.

If the harness does not expose reliable token data, record `null` with
`"source": "not_exposed"`. Do not estimate from character or line counts.

## Result schema

Each result is a single JSON file per run. See `results/agy/` for the
AGY records. The schema accommodates AGY, Codex, and Claude Code.

```json
{
  "harness": "agy",
  "model": "...",
  "model_configuration": "...",
  "case": "...",
  "condition": "...",
  "signal_commit": "...",
  "timestamp": "...",

  "scientific": {
    "execution_pass": true,
    "integrity_pass": true,
    "semantic_error_count": 0,
    "accept_at_1": true,
    "clarification_quality": "NA",
    "corrective_turns_needed": 0,
    "native_editable_pass": true
  },

  "economy": {
    "plot_loc": 42,
    "number_of_axes": 1,
    "helper_function_count": 0
  },

  "edit": {
    "success": null,
    "regression": null,
    "lines_touched": null,
    "corrective_turns": null,
    "wall_clock_seconds": null
  },

  "tokens": {
    "generation": {
      "input": null,
      "output": null,
      "total": null,
      "cached": null
    },
    "edit": {
      "input": null,
      "output": null,
      "total": null,
      "cached": null
    },
    "source": "not_exposed"
  },

  "visual_economy": {
    "question_fit": null,
    "unnecessary_structure": null
  }
}
```

## Hypotheses

Keep these separate. Do not claim support unless corresponding metrics
support it.

- **H1 — Scientific integrity**: Signal reduces scientific/semantic
  mistakes. Current AGY evidence may remain neutral.

- **H2 — Visual/code economy**: Signal reaches an equally correct answer
  with less unnecessary structure.

- **H3 — Editability**: Signal output requires less effort to perform
  ordinary human modifications.

- **H4 — Efficiency**: Signal's context cost is compensated by lower
  generation/correction cost.

## Cross-harness analysis

Report each harness independently:

```
AGY:   Baseline vs Signal
Codex: Baseline vs Signal
Claude: Baseline vs Signal
```

Only after all three exist may we inspect whether the Signal effect
replicates across harnesses. The question is:

> Does Signal consistently improve economy/editability across different
> capable coding agents?

Not: "Which harness is best?"

Harness identity is a blocking variable.

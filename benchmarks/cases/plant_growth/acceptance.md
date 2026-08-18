# Acceptance — plant_growth

Semantic-risk case. Tests semantics + uncertainty + destination together.
Frozen before running. `ci_low`/`ci_high` are deliberately asymmetric
around `mean_height_cm` — do not encode a preferred chart style beyond
what correct representation requires.

## CRITICAL

- `plot.py` runs from a clean environment and produces `plot.png`.
- The central estimate (`mean_height_cm`) is represented.
- `ci_low` and `ci_high` are both represented (not dropped, not averaged
  into a single symmetric value).
- Asymmetry between the lower and upper bound is visually preserved
  (e.g. explicit lower/upper extents, not a symmetric error bar computed
  from one side).
- The interval is not silently relabeled or treated as SD/SE/generic
  "error" — if the figure names the interval, it must not misstate what
  it is beyond what the data supports.
- Units (cm) remain visible.
- No week/row is silently dropped.
- The figure executes successfully end to end.

## NICE TO HAVE

- Paper-appropriate size and typography (legible at print scale).
- Vector-friendly export (e.g. suitable for a PDF/vector destination).
- Clean, uncluttered layout.

These affect usefulness but must never override a CRITICAL scientific
correctness item.

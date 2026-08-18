# Acceptance — ab_experiment

Derived-quantity challenge. Frozen before running. `A` and `B` have
substantially different visitor counts, so raw conversion counts are not
directly comparable.

## CRITICAL

- `plot.py` runs from a clean environment and produces `plot.png`.
- Denominator information is preserved through either:
  - a conversion rate (`conversions / visitors`) representation, or
  - another representation where `conversions` and `visitors` remain
    jointly interpretable (e.g. both shown together in a way that makes
    exposure differences legible).
- The figure does not simply compare raw conversion counts as though
  exposure (visitor count) were equal.
- If statistical uncertainty is introduced (e.g. a confidence interval
  on the rate), its method and assumptions must be stated or evident and
  defensible (e.g. a named standard proportion CI method). The benchmark
  does not require an interval — its absence is not itself a failure.
- No fabricated or unstated assumption is used to justify the comparison.

## NICE TO HAVE

- Visitor counts (n) visible alongside the rate.
- Readable, uncluttered figure.

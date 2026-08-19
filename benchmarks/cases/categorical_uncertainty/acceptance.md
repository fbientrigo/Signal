# Acceptance — categorical_uncertainty

Routine recipe stress test. Frozen before running.

## CRITICAL

- `plot.py` runs and produces `plot.png`.
- Before labeling the interval, the agent asks what `low`/`high` mean; use `clarification.txt` as the frozen answer.
- All four channel estimates are represented in input order.
- Both lower and upper interval bounds are represented and asymmetry is preserved.
- The interval is identified as a 68% bootstrap confidence interval, not SD, SE, or generic symmetric error.
- No category is silently dropped and no ranking is invented.

## NICE TO HAVE

- Point estimates on a common scale rather than unnecessary area encoding.
- Paper-appropriate compact layout.

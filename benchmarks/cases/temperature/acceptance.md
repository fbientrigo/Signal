# Acceptance — temperature

Control case. Frozen before running. No preferred chart style is encoded
here — a line plot and a scatter plot can both pass.

## CRITICAL

- `plot.py` runs from a clean environment and produces `plot.png`.
- Dates appear in chronological order (Jan 1 -> Jan 14), not re-sorted
  alphabetically or shuffled.
- Temperature units (°C) are visible on the figure (axis label, title, or
  legend).
- No fabricated transformation or statistic (no smoothing, trend line,
  or aggregation that wasn't asked for).
- The figure is readable: axes labeled, no overlapping/illegible text.

## NICE TO HAVE

- Sensible tick spacing/date formatting.
- Reasonable figure size and default styling.

## Desired Signal behavior

Approximately neutral. This case should already be easy for a capable
coding agent; Signal should not make a simple plot worse, more complex,
or harder to read.

# Acceptance — weighted_signal_background

Weighted scientific distribution stress test. Frozen before running.

## CRITICAL

- `plot.py` runs and produces `plot.png`.
- Event weights are used; the figure is not based on unweighted event counts.
- Signal and background use common score bin edges or another representation that preserves comparable weighted yield.
- The vertical quantity remains expected weighted yield for the common target exposure; neither sample is silently converted to unit-area density.
- Statistical uncertainty, if shown as requested, is based on the independent weighted contributions (per-bin variance `sum(w^2)` before any deterministic external scaling), not ordinary `sqrt(N)` or `sqrt(sum(w))`.
- The score > 0.8 tail remains visible and is not truncated or smoothed away.
- Any normalization or scale shown on the axis is labeled honestly.

## NICE TO HAVE

- Step histograms or similarly legible overlap treatment.
- A restrained indication of the scientifically important tail threshold if it aids interpretation.

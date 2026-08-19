# Acceptance — irregular_parameter_scan

Non-standard composition stress test. Frozen before running.

## CRITICAL

- `plot.py` runs and produces `plot.png`.
- Every evaluated parameter point is represented.
- Efficiency is encoded at the evaluated points without inventing a continuous field, gridding missing combinations, or interpolating unevaluated regions.
- Theory-excluded points remain distinguishable without hiding their measured/evaluated efficiency.
- Mass [GeV] and lifetime [mm] semantics remain visible.
- Any lifetime transform preserves all positive values and is explicitly labeled.

## NICE TO HAVE

- A scatter/point-field composition with continuous color for efficiency and a second channel such as marker shape/edge for exclusion.
- Colorbar and legend roles remain unambiguous.

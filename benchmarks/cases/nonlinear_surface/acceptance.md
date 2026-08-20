# Acceptance — nonlinear_surface

Adversarial case. Frozen before running. Tests nonlinear multivariate visual
reasoning: two independent variables (`temperature_c`, `humidity_pct`) drive
one dependent variable (`performance`) through a curved, interacting surface
with a secondary local feature. Row order is shuffled and a handful of
grid cells are missing. The generating function is not disclosed to the
evaluated agent and must not be guessed at when scoring — score only what
the figure visually communicates.

No preferred chart mechanism is encoded here. Heatmap, contour, filled
contour, a justified 3D surface, or another 2D encoding that keeps all
three variables jointly interpretable can all pass.

## CRITICAL

- `plot.py` runs from a clean environment and produces `plot.png`.
- All three variables are represented: `temperature_c`, `humidity_pct`,
  and `performance` are all visually recoverable from the figure.
- Neither `temperature_c` nor `humidity_pct` is silently dropped, held
  implicit, or averaged/aggregated away to reduce the plot to one
  independent variable.
- Row order (the order rows appear in `data.csv`) is not treated as a
  meaningful continuous axis (e.g. no line plot connecting points in file
  order as if it were a trajectory or time series).
- The nonlinear 2D structure is visually recoverable: a reader can see
  that performance is not simply increasing/decreasing with either
  variable alone, and that there is a region (or regions) of higher
  performance rather than a uniform gradient or a straight-line trend.
- No unjustified linear fit, trend line, or smoothing is presented in a
  way that misrepresents the underlying structure as simpler than it is.
- If interpolation, gridding, or smoothing is used to render a continuous
  surface from irregular/missing points, it must not be presented as
  measured data — the figure or code must not fabricate values and claim
  them as observations.
- Missing grid cells (present in the source data) are not silently
  filled in with fabricated values without disclosure.
- Units/ranges remain interpretable (e.g. axis labels naming temperature,
  humidity, and performance, with sensible ranges).
- No scientifically misleading transformation (e.g. a color/axis scale
  that inverts or hides where performance is actually higher vs lower).

## NICE TO HAVE

- A colorbar or legend that makes the `performance` scale legible.
- Clean, uncluttered layout appropriate for a paper or report.
- Handling of the missing cells that is visually honest (e.g. gaps,
  or clearly-labeled interpolation) rather than invisible.

These affect usefulness but must never override a CRITICAL scientific
correctness item.

## Desired Signal behavior

Signal currently has no dedicated recipe for a two-independent-variable,
one-dependent-variable surface. This case is expected to be hard for both
conditions. The interesting result is not "does Signal pass" but whether
Signal's general components (`references/chart_selection.md`,
`components/normalization.md`, `references/scientific_integrity.md`) are
enough to reason toward a defensible representation without a matching
recipe, and whether that reasoning transfers across agents. A weak result
here is a legitimate finding, not a bug to fix by adding a recipe before
scoring.

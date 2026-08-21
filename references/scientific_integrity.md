# Scientific integrity — plotting guardrails

Load this reference when the figure contains uncertainty, weights, missing/censored data, normalization, transformations, logarithmic scales, or publication-sensitive choices.

## Evidence before appearance

Keep explicit:

- units;
- sample/replicate structure;
- missing/censored values;
- exclusions/filters;
- transformations and smoothing;
- binning;
- normalization/weights;
- estimator;
- uncertainty definition;
- source data/provenance when the context requires reproducibility.

## Uncertainty

Never use generic "error" language when the actual object is known. Distinguish:

- measurement uncertainty;
- sample SD;
- SE;
- confidence interval;
- credible/posterior interval;
- percentile/bootstrap interval;
- model envelope.

State `n` and the unit of replication when it changes interpretation.

Do not symmetrize asymmetric intervals merely for convenience.

## Residuals, ratios, and pulls

Label the actual derived quantity instead of a generic term:

- a residual (observed − predicted) usually references zero;
- a ratio (observed / predicted) usually references one;
- a pull ((observed − predicted) / uncertainty) references zero and is scaled by an uncertainty definition that should itself be stated.

Do not call every lower comparison panel a "residual" — check whether it is actually a ratio or a pull, since the meaningful reference line and axis label differ for each.

## Raw observations

Show raw observations when feasible and when they help reveal sample size, heterogeneity, or distribution shape. Do not jitter so aggressively that values/categories become ambiguous.

## Missing data

Do not silently connect across missing measurements or silently drop missingness that affects interpretation.

## Axes

- Bars/areas usually require zero because length/area is the encoding.
- Point/line plots may use non-zero limits when scientifically justified; preserve context and avoid exaggeration.
- Use log/symlog only when the transformation matches the scientific question.

## Color

Color should encode a variable or direct attention. Important distinctions should remain interpretable without color alone when feasible.

## Export

Treat interactive and static outputs as different deliverables. A hover tooltip is not a substitute for explicit labels in a static paper figure.

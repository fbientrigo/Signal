---
component: uncertainty
applies_to: [distribution, relationship, trend, comparison, scientific]
backends: [matplotlib, seaborn, plotly]
---

# Uncertainty

Uncertainty is a semantic component, not a style switch.

## Required reasoning

Know or explicitly request:

- what the interval means (SD/SE/CI/credible/measurement/etc.);
- whether it is symmetric or asymmetric;
- whether uncertainty belongs on x, y, or both;
- unit of replication / `n` when relevant.

## Choose the visual mechanism

| Structure | Default |
|---|---|
| isolated estimates | error bars |
| continuous ordered estimate | band + central line |
| asymmetric interval | explicit lower/upper extents |
| raw replicates available | consider raw points + summary |
| 2D x and y uncertainty | xerr + yerr when legible |

## Matplotlib: symmetric / asymmetric error bars

```python
ax.errorbar(
    x,
    y,
    yerr=yerr,                 # or np.vstack([y - low, high - y])
    fmt="o",
    capsize=3,
    linewidth=1.2,
    markeredgewidth=1.0,
)
```

## Matplotlib: interval band

```python
ax.plot(x, estimate)
ax.fill_between(x, lower, upper, alpha=0.18, linewidth=0)
```

Do not hide the central estimate inside an opaque band.

## Plotly

Use trace-native `error_y` / `error_x` for point intervals and a filled pair of traces for continuous bands when interaction is useful.

## Scientific checks

- bounded quantities may require bounded/asymmetric intervals;
- weighted counts do not automatically have Poisson `sqrt(N)` uncertainty;
- model envelopes are not confidence intervals unless defined that way;
- multiple uncertainty sources should not be merged visually unless the analysis defines the combination.

# Uncertainty

## Solves

Display uncertainty while preserving what the interval actually means.

## Required semantics

Know or explicitly ask:

- measurement uncertainty, SD, SE, confidence interval, credible interval, bootstrap interval, model envelope, or another definition;
- symmetric versus asymmetric;
- whether uncertainty belongs on x, y, or both;
- unit of replication and `n` when relevant.

Do not infer these meanings from the visual appearance of an existing figure.

## Choose the visual mechanism

| Structure | Useful default |
|---|---|
| isolated estimates | error bars |
| continuous ordered estimate | band + central line |
| asymmetric interval | explicit lower/upper extents |
| raw replicates available | consider raw points + summary |
| x and y uncertainty | xerr + yerr when legible |

### Matplotlib point intervals

```python
yerr = np.vstack([estimate - low, high - estimate])
ax.errorbar(x, estimate, yerr=yerr, fmt="o", capsize=3)
```

### Matplotlib band

```python
ax.plot(x, estimate)
ax.fill_between(x, lower, upper, alpha=0.18, linewidth=0)
```

## Scientific guardrails

- preserve bounded or asymmetric intervals;
- weighted counts do not automatically have Poisson uncertainty;
- model envelopes are not confidence intervals unless defined that way;
- do not merge multiple uncertainty sources visually unless the analysis defines the combination.

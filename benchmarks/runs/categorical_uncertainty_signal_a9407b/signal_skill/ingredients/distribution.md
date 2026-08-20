# Distribution

## Solves

Represent the shape, spread, tails, modes, or cumulative structure of a numeric variable, including weighted observations.

## Choose the mechanism

- histogram → familiar view of shape and local density/yield;
- ECDF → bin-free cumulative comparison and exact ordering;
- raw points or a compact summary → useful when sample size is small and individual observations matter.

## Histograms

- choose bins deliberately;
- when comparing samples, use common bin edges;
- label whether the vertical axis is counts, weighted yield, density, or probability;
- do not let a convenient normalization silently change the question.

## Weighted observations

Preserve event or observation weights.

Do not silently fall back to unweighted counts.

If showing weighted yield:

```python
ax.hist(values, bins=bins, weights=weights, histtype="step")
```

If showing density or another normalization, state it explicitly and apply the same scientific meaning to the uncertainty.

## Statistical uncertainty with weights

Do not assume ordinary Poisson `sqrt(N)` uncertainty for non-unit weights, and do not use `sqrt(sum(weights))` as a substitute.

When event contributions are independent and the supplied weights can be treated as fixed, the usual unnormalized per-bin variance estimate is

```text
variance = sum(w_i**2)
sigma = sqrt(sum(w_i**2))
```

This is a conditional rule, not a universal one:

- prefer provided bin-level uncertainties when the analysis already defines them;
- correlations, fitted weights, nuisance parameters, or other analysis-specific effects can invalidate the simple independent-event interpretation;
- a deterministic external scale factor `c` scales the uncertainty by `abs(c)`;
- normalizing a histogram by its own observed total couples the bins, so simple rescaled `sum(w^2)` bars do not describe the full covariance.

If those distinctions affect the reader's conclusion and are unknown, ask rather than invent an uncertainty model.

## Comparison

If several overlapping distributions become hard to decode, prefer ECDFs or small multiples rather than adding more opacity and colors.

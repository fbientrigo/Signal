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

If showing density, state that normalization explicitly.

Uncertainty on weighted bins is analysis-dependent. Do not assume ordinary Poisson `sqrt(N)` uncertainty for non-unit weights.

## Comparison

If several overlapping distributions become hard to decode, prefer ECDFs or small multiples rather than adding more opacity and colors.

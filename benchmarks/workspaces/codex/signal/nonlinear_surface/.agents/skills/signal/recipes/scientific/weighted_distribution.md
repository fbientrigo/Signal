---
recipe: weighted_distribution
family: scientific
intent: show a distribution where observations carry non-uniform statistical weights
inputs: [values, weights]
compatible_components: [normalization, highlight, reference_line, facet, annotation]
---

# Weighted distribution

Never silently fall back to unweighted counts.

```python
fig, ax = plt.subplots(layout="constrained")
ax.hist(values, bins=bins, weights=weights, histtype="step")
ax.set(xlabel="Value", ylabel="Weighted events")
```

If displaying density instead of weighted yield, state that transformation explicitly.

Uncertainty on weighted bins is analysis-dependent; do not assume Poisson `sqrt(N)` when event weights are non-unit. Use the analysis-defined variance prescription.

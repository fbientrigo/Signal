---
component: normalization
applies_to: [distribution, comparison, scientific]
---

# Normalization

Normalization changes meaning. Make it explicit in code and axis labels.

Common cases:

- counts → probability/density;
- raw weighted events → weighted yield;
- category counts → fraction/percent;
- value → reference-normalized ratio.

For histograms:

```python
ax.hist(values, bins=bins, weights=weights, density=False)
```

Do not use `density=True` merely because curves look easier to compare. Choose it only when probability density is the intended quantity.

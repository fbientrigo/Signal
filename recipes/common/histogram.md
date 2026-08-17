---
recipe: histogram
family: distribution
inputs: [values]
compatible_components: [normalization, highlight, reference_line, facet, annotation]
---

# Histogram

Use when the shape of a numeric distribution matters and sample size is sufficient for binning to be meaningful.

```python
fig, ax = plt.subplots(layout="constrained")
ax.hist(values, bins="auto", histtype="stepfilled", alpha=0.75)
ax.set(xlabel="Value", ylabel="Count")
```

Check bin sensitivity. For small samples, raw observations or ECDF may be more honest.

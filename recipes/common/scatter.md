---
recipe: scatter
family: relationship
inputs: [x, y]
compatible_components: [uncertainty, highlight, reference_line, annotation, facet]
---

# Scatter

Use for a relationship between two numeric variables.

```python
fig, ax = plt.subplots(layout="constrained")
ax.scatter(x, y, s=24, alpha=0.8)
ax.set(xlabel="x", ylabel="y")
```

If overplotting hides structure, prefer alpha, smaller marks, hexbin/density, or facets rather than random visual clutter.

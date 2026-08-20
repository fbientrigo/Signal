---
recipe: bar
family: comparison
inputs: [category, value]
compatible_components: [uncertainty, highlight, reference_line, annotation, facet]
---

# Bar

Use when category magnitudes are encoded by length from a meaningful baseline.

```python
fig, ax = plt.subplots(layout="constrained")
ax.bar(category, value)
ax.set(ylabel="Value")
```

Usually include zero. If zero is not meaningful and the comparison is about position rather than length, use dots instead.

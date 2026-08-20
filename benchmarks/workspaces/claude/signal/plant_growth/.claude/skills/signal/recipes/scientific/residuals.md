---
recipe: residuals
family: scientific
intent: expose deviations from a prediction/reference
inputs: [x, residual]
compatible_components: [uncertainty, highlight, reference_line, annotation, facet]
---

# Residuals

Use a visible zero reference.

```python
fig, ax = plt.subplots(layout="constrained")
ax.axhline(0, linewidth=1.0, linestyle="--")
ax.plot(x, residual, "o")
ax.set(xlabel="x", ylabel="Residual")
```

For ratio/pull variants, label the exact definition; do not call every lower panel a residual.

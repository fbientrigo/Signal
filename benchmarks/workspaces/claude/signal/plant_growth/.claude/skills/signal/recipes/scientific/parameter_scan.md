---
recipe: parameter_scan
family: scientific
intent: expose viable/excluded/interesting structure across parameter space
inputs: [x, y, value_or_class]
compatible_components: [highlight, reference_line, annotation, facet]
---

# Parameter scan

Choose the encoding from the semantic object:

- continuous score/likelihood → scatter color, heatmap, or contours;
- accepted/rejected class → categorical marks/colors;
- sparse evaluated points → show points; do not imply an interpolated field unless justified.

```python
fig, ax = plt.subplots(layout="constrained")
sc = ax.scatter(x, y, c=value, s=20)
fig.colorbar(sc, ax=ax, label="Score")
ax.set(xlabel="Parameter 1", ylabel="Parameter 2")
```

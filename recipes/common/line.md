---
recipe: line
family: trend
inputs: [x_ordered, y]
compatible_components: [uncertainty, highlight, reference_line, annotation, facet]
---

# Line

Use when x is meaningfully ordered and connecting adjacent observations expresses continuity/order.

```python
fig, ax = plt.subplots(layout="constrained")
ax.plot(x, y, marker="o", linewidth=1.6)
ax.set(xlabel="x", ylabel="y")
```

Do not silently bridge missing observations when the gap itself matters.

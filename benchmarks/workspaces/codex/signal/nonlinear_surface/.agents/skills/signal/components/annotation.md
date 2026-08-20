---
component: annotation
applies_to: [distribution, relationship, trend, comparison, scientific]
---

# Annotation

Annotate a conclusion or mechanism when it saves the reader from decoding legends/geometry.

```python
ax.annotate(
    "benchmark",
    xy=(x0, y0),
    xytext=(8, 10),
    textcoords="offset points",
    arrowprops={"arrowstyle": "-", "linewidth": 0.8},
)
```

Keep annotations factual. Do not use them to claim stronger inference than the data support.

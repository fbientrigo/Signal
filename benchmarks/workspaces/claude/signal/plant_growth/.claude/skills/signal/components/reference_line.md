---
component: reference_line
applies_to: [distribution, relationship, trend, comparison, scientific]
---

# Reference line

Use for a scientifically or operationally meaningful threshold, baseline, benchmark, zero, or target.

```python
ax.axvline(x_ref, linestyle="--", linewidth=1.0, label="Benchmark")
# or
ax.axhline(y_ref, linestyle="--", linewidth=1.0)
```

Prefer a meaningful reference over arbitrary grid decoration. Label it directly when the meaning is not obvious.

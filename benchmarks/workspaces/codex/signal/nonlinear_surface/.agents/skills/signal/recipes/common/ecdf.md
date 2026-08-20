---
recipe: ecdf
family: distribution
inputs: [values]
compatible_components: [highlight, reference_line, facet, annotation]
---

# ECDF

Use when you want to compare full distributions without choosing bins.

```python
x = np.sort(np.asarray(values))
y = np.arange(1, len(x) + 1) / len(x)
fig, ax = plt.subplots(layout="constrained")
ax.step(x, y, where="post")
ax.set(xlabel="Value", ylabel="Cumulative fraction", ylim=(0, 1))
```

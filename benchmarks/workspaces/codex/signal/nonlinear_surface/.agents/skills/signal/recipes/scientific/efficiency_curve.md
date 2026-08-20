---
recipe: efficiency_curve
family: scientific
intent: show selection or detection efficiency versus an ordered variable
inputs: [x, passed, total]
compatible_components: [uncertainty, highlight, reference_line, annotation, facet]
---

# Efficiency curve

Efficiency is a bounded proportion. Do not default to Gaussian error bars when counts are small or efficiency is near 0/1.

## Minimal data

```python
eff = passed / total
```

Choose the interval deliberately (for example Wilson, Clopper-Pearson, bootstrap, or a model-specific interval) and state which one is used.

## Rendering once `low` and `high` are defined

```python
fig, ax = plt.subplots(layout="constrained")
yerr = np.vstack([eff - low, high - eff])
ax.errorbar(x, eff, yerr=yerr, fmt="o-", capsize=3)
ax.set(xlabel="Mass [GeV]", ylabel="Efficiency", ylim=(0, 1))
```

For a continuous model estimate, use a band rather than dense overlapping caps.

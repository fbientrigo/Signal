---
recipe: trend_with_uncertainty
question: How does an estimate change across an ordered variable, and how uncertain is it?
ingredients: [trend, uncertainty, axes, color]
---

# Trend with uncertainty

## Use when

The reader needs both the ordered evolution of an estimate and the uncertainty around that estimate.

## Default composition

```text
ordered trend
+ explicit uncertainty
+ clear axes and units
+ restrained color
```

Use points with error bars for discrete evaluated locations.

Use a central line with a band when the estimate is meaningfully continuous or densely sampled.

## Ask only if material

If the uncertainty definition is unknown, ask before choosing or labeling the interval.

Also clarify whether connecting points implies a meaningful progression.

## Adapt

Add `emphasis` for a benchmark or threshold.

Use asymmetric intervals directly when present.

## Avoid

Do not replace uncertainty with smoothing.

Do not connect across missing observations silently.

---
recipe: distribution_overview
question: What are the shape, spread, tails, and notable structure of this numeric variable?
ingredients: [distribution, axes, color]
---

# Distribution overview

## Use when

The reader needs to understand one numeric distribution before making a more specific comparison.

## Default composition

```text
distribution
+ clear axes and units
+ neutral color
```

Start with a histogram for a familiar shape view.

Prefer an ECDF when bin choices would distract from the question or cumulative comparison is more useful.

## Ask only if material

Clarify weights, normalization, filtering, or a scientifically meaningful transform when they are not already known.

## Adapt

- small sample → show raw observations where useful;
- weighted sample → use the weighted path in `ingredients/distribution.md`;
- several groups → use small multiples or another comparison rather than piling many filled histograms together.

## Avoid

Do not add color categories, KDE smoothing, annotations, or statistics unless they answer a stated question.

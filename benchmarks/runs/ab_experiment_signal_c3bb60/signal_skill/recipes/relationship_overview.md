---
recipe: relationship_overview
question: How are these two numeric variables related?
ingredients: [relationship, axes, color]
---

# Relationship overview

## Use when

The reader needs a first clear view of association, structure, clusters, or outliers between two numeric variables.

## Default composition

```text
scatter relationship
+ clear axes and units
+ one neutral series
```

## Ask only if material

Clarify whether a third variable already has meaning through color, whether groups must be compared, or whether the data represent a regular 2D field rather than independent observations.

## Adapt

- mild overplotting → smaller marks or modest alpha;
- heavy overplotting → hexbin/density;
- meaningful gridded field → heatmap;
- important subset → add the `emphasis` ingredient;
- repeated groups → add `layout`.

## Avoid

Do not encode another variable through color just because a column is available.

Do not interpolate sparse points into a smooth field without justification.

---
name: signal
description: Lightweight visual reasoning for Python. Clarify what matters, use a prepared recipe when one fits, or compose reusable ingredients into native Matplotlib, Seaborn, or Plotly.
---

# Signal

**Think deeply. Show simply.**

## First rule

Do not invent a Signal plotting API. Leave native Python behind.

## 1. Understand the reader problem

Start with what the reader should understand.

If missing information can materially change the figure, ask a focused question. Typical high-value unknowns are:

- focus versus context;
- useful signal versus noise;
- whether color already has meaning;
- uncertainty definition;
- ordering;
- weights or normalization;
- valid transformations.

Do not ask for preferences that only change decoration unless the user cares about them.

### Keep explicit requirements

Before choosing a recipe or ingredients, identify the few user-stated requirements that must survive into the figure.

An explicitly important threshold, region, subset, comparison, transformation, or uncertainty is not optional decoration.

Map each such requirement to either:

- the base visual mechanism; or
- an ingredient that represents it.

Simplification may remove decoration, not stated meaning.

## 2. Choose the path

### Fast path — recipe

Use a recipe when the task is common and the reader question matches clearly.

A recipe is a prepared solution built from ingredients. Use its defaults, adapt only what the data or destination requires, then render.

### Flexible path — ingredients

If the data are unusual, layered, or do not fit a recipe cleanly, compose ingredients directly.

Do not create or force a new recipe just to name the combination.

## 3. Preserve semantics

Keep explicit anything that can change interpretation:

- units and scales;
- category ordering;
- weights and normalization;
- missing values and exclusions;
- transforms;
- sample or replicate structure;
- uncertainty meaning;
- bounded quantities.

## 4. Apply the destination

Adapt typography, density, aspect ratio, annotation density, and export to paper, slides, screen, exploratory work, or another explicit destination.

Destination changes presentation, not scientific meaning.

## 5. Render native Python

- Matplotlib by default for static/scientific control;
- Seaborn when it genuinely reduces statistical plotting code;
- Plotly when interaction changes how the user inspects the data.

Durable figure → prefer `plots/<descriptive_name>.py`.

Local exploration → embedded plotting block is fine.

Generated plots must not import Signal.

## Selective loading

Open only what the problem needs:

### Recipes

- distribution shape/spread/tails → `recipes/distribution_overview.md`
- relationship between numeric variables → `recipes/relationship_overview.md`
- magnitudes across categories → `recipes/categorical_comparison.md`
- ordered estimate with uncertainty → `recipes/trend_with_uncertainty.md`
- one focus against broader context → `recipes/focus_in_context.md`

### Ingredients

- scales, limits, ordering, log axes → `ingredients/axes.md`
- semantic color decisions → `ingredients/color.md`
- histogram/ECDF/weights/normalization → `ingredients/distribution.md`
- scatter, density, heatmap, 2D field → `ingredients/relationship.md`
- ordered x/time and connecting observations → `ingredients/trend.md`
- intervals, error bars, bands → `ingredients/uncertainty.md`
- explicitly important subset/region/threshold, context, highlight, reference, annotation → `ingredients/emphasis.md`
- facets and comparable panels → `ingredients/layout.md`

Other references:

- chart choice unclear → `references/chart_selection.md`
- scientific integrity issue → `references/scientific_integrity.md`
- destination/layout/typography → `themes/README.md`
- reverse engineering → `lab/reverse/README.md`

## Refinement

Inspect at the real target size.

Change one high-impact cause at a time.

Stop when the reader can answer the intended question without unnecessary decoding and the scientific meaning remains intact.

## New knowledge

```text
real example
→ reusable ingredient(s)
→ native reproduction
→ second use case
→ promote only if repeated value is demonstrated
```

A recurring stable composition may later become a recipe.

Do not promote source-specific decoration.

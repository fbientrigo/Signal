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

### Intent sufficiency gate

Before choosing a recipe or ingredients, ask:

> Can Signal move from the user's question to a recipe / ingredient composition without inventing a material priority, interpretation, comparison, or reader goal?

- **Yes → fast path.** Continue without constructing a full Visual Brief.
- **No → Visual Brief.**

Dataset size, row or column count, plotting-library complexity, and visual sophistication do not trigger the brief by themselves. The trigger is unresolved intent: materially different interpretations would lead to materially different visual decisions.

### Visual Brief — only when the gate fails

Keep the brief internal and small. Capture only information that can change the visual decision:

- **Reader question** — what should the reader understand?
- **Decision / intended takeaway** — what comparison, judgment, or conclusion should the figure support? This may be absent for a purely descriptive plot.
- **Focus vs context** — what deserves attention, what context is necessary, and what is noise for this question?
- **Material data facts** — when data are available, inspect only structural properties capable of changing the visual mechanism: variable types, observed ranges or orders of magnitude, skew or long tails, density or overlap, sample count, missingness, category cardinality, bounds, weights, asymmetric intervals, and obvious temporal or ordered structure.
- **Destination** — paper, slides, screen, exploratory, or another explicit medium.
- **Visual question** — compress the reasoning into the exact question the figure must answer.

This is not autonomous EDA. Inspect only discriminating data properties needed for the visual decision.

Treat potentially relevant information in three states:

- **Known** — explicitly stated by the user or reliably present in the data. Use it.
- **Safely inferable** — a structural data property that does not assign scientific meaning. Use it only to inform the visual decision.
- **Blocking unknown** — a missing answer for which plausible alternatives would materially change the figure or its interpretation. Ask the user only for these, preferably with one focused question.

Do not infer scientific semantics from numerical structure or column names. Values in `[0, 1]` do not prove probability semantics; a column named `error` does not establish SD, SE, or an interval definition; a positive variable does not by itself justify a log transform.

An intended takeaway is not evidence. Treat requests such as "show that the new method is better" as a claim to test visually, not permission to manufacture the conclusion. The figure must remain able to contradict the desired claim.

Finish the brief with one concrete visual question before recipe or ingredient selection. Reuse any destination or semantics already resolved in the brief rather than asking or deciding them again.

If no Visual Brief is needed, still ask a focused question when a blocking semantic unknown can materially change interpretation. Do not ask for preferences that only change decoration unless the user cares about them.

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

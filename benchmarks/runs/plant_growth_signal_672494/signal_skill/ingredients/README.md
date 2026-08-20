# Ingredients

Ingredients are Signal's small reusable visual solutions.

An ingredient answers:

> How should this local visual decision be handled correctly?

It is larger than a plotting parameter and smaller than a complete communication strategy.

Examples:

- choosing and constraining an axis scale;
- representing a weighted distribution;
- mapping categories to color;
- displaying uncertainty;
- preserving context while highlighting a focus;
- rendering a dense 2D relationship or field.

Signal intentionally does not split ingredients into a deeper taxonomy of marks, encodings, transforms, scales, annotations, or layout objects. Those ideas may appear inside an ingredient when useful.

## Current ingredients

- [`axes.md`](axes.md)
- [`color.md`](color.md)
- [`distribution.md`](distribution.md)
- [`relationship.md`](relationship.md)
- [`trend.md`](trend.md)
- [`uncertainty.md`](uncertainty.md)
- [`emphasis.md`](emphasis.md)
- [`layout.md`](layout.md)

## Granularity rule

Create an ingredient when the unit contains reusable reasoning.

Good:

```text
weighted distribution
semantic color mapping
asymmetric uncertainty
context + focus treatment
```

Too small:

```text
linewidth
marker size
legend location
one hex color
```

Too large:

```text
the full final figure for one paper
```

## Promotion

A new ingredient should solve a real repeated decision, generalize beyond its originating figure, and save enough repeated reasoning to justify another file.

If the decision is obvious in native Python and carries no reusable guidance, do not add an ingredient.

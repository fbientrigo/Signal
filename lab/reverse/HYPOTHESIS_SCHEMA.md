# Visual hypothesis template

This is a compact reasoning template for an agent, not a runtime format Signal compiles.

```yaml
question: compare estimate across x while preserving uncertainty

destination: paper

semantics:
  x: numeric_ordered
  y: numeric
  uncertainty: asymmetric_interval
  normalization: none

recipe:
  name: trend_with_uncertainty
  fit: direct

ingredients:
  - trend
  - uncertainty
  - axes
  - emphasis

attention:
  context: all_points
  focus: benchmark_point

unknowns:
  - exact interval definition
```

If no recipe fits, set `recipe: null` and list the ingredients needed for the ad hoc composition.

If an unknown changes scientific meaning, keep it unknown rather than guessing.

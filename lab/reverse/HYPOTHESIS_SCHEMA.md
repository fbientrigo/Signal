# Visual hypothesis template

This is a compact reasoning template for an agent, not a runtime format Signal compiles.

```yaml
intent: compare estimate across x while preserving uncertainty

destination: paper

structure:
  base_recipe: line
  x: numeric_ordered
  y: numeric
  groups: none

semantics:
  uncertainty: asymmetric_interval
  baseline: null
  normalization: none

components:
  - uncertainty
  - reference_line
  - highlight

layout:
  panels: 1
  legend: direct_or_small

attention:
  context: all_points
  highlight: benchmark_point

style:
  palette: signal
  typography: destination_profile

unknowns:
  - exact interval definition
```

If an unknown changes scientific meaning, keep it unknown rather than guessing.

# Sources and conceptual provenance

Signal keeps its own small contract and distills ideas from existing work.

## Primary architectural references

- **Microsoft Flint** — compact semantic intent for agent-authored charts and strong defaults that reduce low-level generation cost.
  - https://github.com/microsoft/flint-chart
- **K-Dense Scientific Visualization** — scientific plotting guardrails, uncertainty semantics, scoped styling, and native Matplotlib/Seaborn/Plotly practice.
  - https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/scientific-visualization

## Selection and composition references

- **Financial Times Visual Vocabulary** — intent-oriented chart families.
  - https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary
- **From Data to Viz** — data-shape-aware chart selection and caveats.
  - https://www.data-to-viz.com/
- **Observable Plot** — small composable marks/transforms and useful defaults.
  - https://observablehq.com/plot/
- **Vega-Lite** — declarative layering, faceting, uncertainty, and interaction patterns.
  - https://vega.github.io/vega-lite/
- **HoloViews** and **seaborn.objects** — composition as independent pieces rather than combinatorial chart names.
  - https://github.com/holoviz/holoviews
  - https://seaborn.pydata.org/tutorial/objects_interface.html
- **Storytelling with Data** — hierarchy, decluttering, context, and attention.
  - https://www.storytellingwithdata.com/

## Native implementation references

- Matplotlib: https://matplotlib.org/
- Seaborn: https://seaborn.pydata.org/
- Plotly Python: https://plotly.com/python/

## Reverse-engineering research lane

- ChartMimic: https://github.com/ChartMimic/ChartMimic
- Plot2Code: https://github.com/TencentARC/Plot2Code
- ChartCoder: https://github.com/thunlp/ChartCoder
- ChartMaster: https://github.com/WentaoTan/ChartMaster
- DePlot: https://github.com/google-research/google-research/tree/master/deplot

Signal does not vendor code, models, or datasets from these projects. Before adapting or redistributing external code/models/data, inspect the exact current license and terms.

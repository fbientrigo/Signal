# Signal

**Think deeply. Show simply.**

Signal is a lightweight visual-reasoning skill for Python. It helps coding agents turn a question, data semantics, and display context into clear, editable Matplotlib, Seaborn, or Plotly code.

Signal is not a plotting package, renderer, or DSL. The output is ordinary Python that can live in a `plots/` directory, inside a notebook, or embedded in existing analysis code.

## Why Signal

Existing tools tend to optimize one side of the problem: compact chart specifications, scientific plotting guidance, or rendering APIs. Signal combines the useful parts without adding a new runtime:

- compact intent and visual decisions;
- scientific guardrails, especially around uncertainty;
- reusable recipes built from independent components;
- destination-aware typography, density, and palette choices;
- native Python left behind for manual editing.

## Contract

Signal follows a small set of rules:

1. Start from the question.
2. Preserve the scientific meaning of the data.
3. Design for where the figure will be seen.
4. Keep simple plots simple.
5. Treat uncertainty as data, not decoration.
6. Use color to encode meaning or direct attention.
7. Compose recipes from small independent components.
8. Prefer native Matplotlib, Seaborn, or Plotly code.
9. A generated plot must not depend on Signal to run.
10. Add abstraction only after repeated use proves it useful.

See [`CONTRACT.md`](CONTRACT.md) for the frozen rules.

## Mental model

```text
question + destination + data semantics
                ↓
              intent
                ↓
              recipe
                ↓
            components
                ↓
             profile
                ↓
        native Python code
```

A figure might be described as:

```text
efficiency curve
+ asymmetric uncertainty
+ benchmark highlight
+ reference line
+ paper profile
```

The final implementation is still normal Python.

## Output modes

### Standalone plot script

Use for durable figures that will be revisited, reviewed, or regenerated.

```text
project/
└── plots/
    ├── efficiency_vs_mass.py
    ├── lifetime_distribution.py
    └── _style.py              # optional project-local helper
```

Signal should prefer self-contained scripts unless a shared local style helper clearly reduces duplication.

### Embedded plot

Use for notebooks, diagnostics, and small analysis scripts. Signal should emit a compact plotting block that can be edited in place.

### Shared project style

If several figures need one visual identity, copy or adapt the small helpers under [`themes/`](themes/). The target project owns that code. Signal is not a runtime dependency.

## Destination profiles

The same scientific figure may need different rendering decisions depending on where it will be seen:

- **paper** — compact, vector-first, information-dense;
- **slides** — large text, strong hierarchy, fewer details;
- **screen** — comfortable spacing and medium density;
- **exploratory** — fast iteration, diagnostics, optional interaction.

Destination changes presentation, not scientific meaning.

## Recipes and components

Recipes capture the base visual mechanism. Components add orthogonal information.

```text
recipes/
  common/       histogram, scatter, line, bar, ECDF
  scientific/   efficiency, weighted distribution, residuals, parameter scan

components/
  uncertainty, highlight, reference line, annotation,
  normalization, facets, interaction
```

Do not create a new recipe for every combination. Prefer:

```text
scatter + uncertainty + highlight
```

over:

```text
scatter_with_uncertainty_and_highlight
```

## Plot workflow

Signal uses a short visual-development loop:

```text
question → destination → semantics → simplest recipe
        → required components → render → inspect at target size
        → one causal change → accept
```

See [`docs/PLOT_METHOD.md`](docs/PLOT_METHOD.md).

## Repository workflow

Signal itself is developed in small vertical slices. A change should solve one observed plotting problem, include a concrete example or acceptance check, and avoid speculative framework work.

See [`docs/AGILE.md`](docs/AGILE.md).

## Learning from figures

Useful figures can become new Signal knowledge:

```text
example figure
    ↓
identify the visual mechanism
    ↓
reproduce in native Python
    ↓
separate structure from source-specific style
    ↓
extract recipe/components
    ↓
test on a second dataset
    ↓
promote only if it generalizes
```

The experimental reverse-engineering work lives under [`lab/reverse/`](lab/reverse/). ML or RL may be used later when measured evidence shows that it improves this loop.

## Sources

Signal distills useful ideas from established visualization work, including Microsoft Flint, K-Dense Scientific Visualization, Financial Times Visual Vocabulary, Data-to-Viz, Observable Plot, Vega-Lite, Storytelling with Data, Matplotlib, Seaborn, and Plotly.

Signal borrows principles and mechanisms, not source-specific visual identities.

## Status

Early foundation. The current goal is to validate the contract with real plots before expanding the recipe set.

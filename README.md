# Signal

**Think deeply. Show simply.**

Signal is a lightweight visual-reasoning skill for Python. It helps coding agents turn a reader question, data semantics, and display context into clear, editable Matplotlib, Seaborn, or Plotly code.

Signal is not a plotting package, renderer, or DSL. The output is ordinary Python that can live in a `plots/` directory, a notebook, or existing analysis code.

## Core idea

Signal keeps only two reusable visual building blocks:

- **ingredients** — small, reusable solutions to visual decisions that are easy to repeat or get wrong;
- **recipes** — prepared combinations of ingredients for recurring reader problems, with sensible defaults and room to adapt.

Recipes provide speed. Ingredients provide freedom.

A recipe is a default path, not a whitelist of allowed figures.

## Start with the conversation

Before choosing a visual form, establish what matters. Ask only when the answer can materially change the figure.

Useful questions include:

- what should the reader understand?
- what is the focus and what is only context?
- which data are noise for this question?
- does color already carry meaning?
- what does the uncertainty represent?
- which transformations or normalizations are valid?

Do not ask cosmetic questions when the answer does not change interpretation.

## Mental model

```text
question + destination + data
            ↓
clarify only material unknowns
            ↓
         semantics
            ↓
      does a recipe fit?
        ↙          ↘
      yes           no
      ↓              ↓
use/adapt       compose ingredients
      ↘              ↙
         native Python
              ↓
      inspect at target size
```

For a common task, Signal should usually take the fast path through a recipe.

For unusual or layered data, Signal should compose ingredients directly instead of forcing the problem into a predefined chart family.

## Ingredients

An ingredient solves a local visual problem. It is more meaningful than a plotting parameter and smaller than a complete communication strategy.

Initial ingredients cover:

- axes and scales;
- color;
- distributions, including weighted data;
- relationships and 2D fields;
- ordered trends;
- uncertainty;
- emphasis and context;
- layout and small multiples.

An ingredient may contain marks, encodings, scale choices, transforms, scientific guardrails, or attention mechanisms. Signal does not create separate ontologies for those concepts.

See [`ingredients/`](ingredients/).

## Recipes

A recipe solves a recurring reader problem with a useful default composition.

Initial recipes cover:

- distribution overview;
- relationship overview;
- categorical comparison;
- trend with uncertainty;
- focus in context.

Recipes should expose adaptation points instead of encoding every possible combination.

```text
good:
trend_with_uncertainty
focus_in_context

bad:
scatter_with_uncertainty_highlight_reference
```

If no recipe fits cleanly, compose ingredients and move on.

See [`recipes/`](recipes/).

## Destination profiles

The same scientific meaning may need different presentation depending on where it will be seen:

- **paper** — compact, vector-first, information-dense;
- **slides** — larger type, stronger hierarchy, fewer details;
- **screen** — comfortable spacing;
- **exploratory** — rapid inspection and optional interaction.

Destination changes presentation, not scientific meaning.

See [`themes/`](themes/).

## Output modes

### Standalone plot script

Prefer for durable figures:

```text
project/
└── plots/
    ├── efficiency_vs_mass.py
    └── lifetime_distribution.py
```

### Embedded plot

Use for notebooks, diagnostics, and small analysis scripts.

### Shared project style

If several figures need one visual identity, copy or adapt the small helpers under [`themes/`](themes/). The target project owns the code.

Generated plots must not depend on Signal at runtime.

## Plot workflow

```text
question
→ clarify material unknowns
→ destination
→ semantics
→ recipe if one fits, otherwise ingredients
→ native Python
→ inspect at target size
→ one causal change
→ accept
```

See [`docs/PLOT_METHOD.md`](docs/PLOT_METHOD.md).

## Learning from figures

Useful figures can become Signal knowledge:

```text
example
→ identify the reader problem
→ decompose reusable ingredients
→ reproduce in native Python
→ separate structure from source-specific style
→ test on another dataset
→ promote an ingredient or recurring composition only if it generalizes
```

The experimental reverse-engineering work lives under [`lab/reverse/`](lab/reverse/).

## Sources

Signal distills useful ideas from established visualization work, including Microsoft Flint, K-Dense Scientific Visualization, Financial Times Visual Vocabulary, Data-to-Viz, Observable Plot, Vega-Lite, Storytelling with Data, Matplotlib, Seaborn, and Plotly.

Signal borrows principles and mechanisms, not source-specific visual identities.

## License

Signal is MIT licensed. Use, adapt, and redistribute it with attribution and the license notice. Academic users can cite Signal via GitHub's citation metadata (see [`CITATION.cff`](CITATION.cff)).

## Status

Early foundation. Keep the catalog small and validate the ingredients/recipes model with real plots before expanding it.

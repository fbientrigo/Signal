# Signal contract

This file defines the rules that should remain stable while Signal evolves.

## Mission

**Signal is a lightweight visual-reasoning skill that turns intent, data semantics, and display context into clear, editable, native Python figures.**

> Think deeply. Show simply.

## Invariants

1. **Skill first.** Signal is knowledge and workflow before software.
2. **Native output.** Emit Matplotlib, Seaborn, or Plotly directly.
3. **No runtime lock-in.** A generated plot must run without Signal.
4. **Simple stays simple.** Do not introduce schemas, registries, wrappers, or compilers for ordinary plots.
5. **Intent before chart type when the decision matters.** First state what the reader should be able to see.
6. **Destination is part of the design.** Paper, slides, screen, and exploration may require different typography, density, aspect ratio, and interaction.
7. **Destination does not change scientific meaning.** Profiles change presentation, not data semantics.
8. **Semantics stay explicit.** Preserve units, ordering, weights, missingness, transforms, sample structure, and uncertainty meaning when they affect interpretation.
9. **Uncertainty is first-class.** SD, SE, confidence intervals, credible intervals, measurement uncertainty, bootstrap intervals, and model envelopes are not interchangeable.
10. **Recipes describe base mechanisms.** Prefer `histogram`, `scatter`, `efficiency_curve`, not precomposed special cases.
11. **Components are orthogonal.** Add uncertainty, context, highlights, references, annotations, normalization, facets, and interaction independently.
12. **Color has a job.** Use it to encode meaning, establish context, or direct attention. Do not rely on color alone for essential distinctions.
13. **Typography serves the destination.** Text must remain legible at the real display or publication size.
14. **Interaction must answer a question.** Hover, filters, sliders, and toggles are not default decoration.
15. **Scientific meaning outranks polish.** Do not hide exclusions, transformations, normalization, missing data, sample structure, or inconvenient observations.
16. **Manual editing is expected.** Generated code should be easy to read and modify after Signal leaves the workflow.
17. **Load knowledge on demand.** Keep `SKILL.md` short. Open recipes, components, and references only when relevant.
18. **Learn by distillation, not copying.** Reproduce the useful mechanism of an example, separate reusable structure from source-specific style, then test it on a second dataset.
19. **No hidden scientific inference.** If a distinction matters and the information is missing, state that it is missing.
20. **No speculative abstraction.** Promote helpers or recipes only after repeated use demonstrates a stable need.

## Output modes

Signal may produce:

- a standalone plotting script under a project-local `plots/` directory;
- an embedded plotting block inside existing analysis code or a notebook;
- an optional project-local style helper shared by several plots.

The target project owns all generated code.

## Non-goals

- no Python plotting package;
- no custom plotting API;
- no custom DSL;
- no rendering engine;
- no autonomous EDA system;
- no general chart recommendation solver;
- no required local ML model;
- no multi-agent framework;
- no styling system that overrides project needs.

## Promotion rule

A visual pattern becomes a reusable Signal recipe or component only when:

1. it answers a clear visual intent;
2. it reproduces a useful mechanism, not merely a visual style;
3. the reusable part can be stated independently of the source example;
4. it works on at least one second dataset or use case;
5. it composes with existing pieces without special-case naming;
6. it saves enough repeated reasoning or code to justify its existence.

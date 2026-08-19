# Signal contract

This file defines the rules that should remain stable while Signal evolves.

## Mission

**Signal is a lightweight visual-reasoning skill that turns a reader question, data semantics, and display context into clear, editable, native Python figures.**

> Think deeply. Show simply.

## Invariants

1. **Skill first.** Signal is knowledge and workflow before software.
2. **Native output.** Emit Matplotlib, Seaborn, or Plotly directly.
3. **No runtime lock-in.** A generated plot must run without Signal.
4. **Clarify material ambiguity.** Ask the user when focus, context, noise, color meaning, uncertainty, normalization, or a valid transformation can change the visual decision. Do not ask cosmetic questions by default.
5. **Semantics stay explicit.** Preserve units, ordering, weights, missingness, transforms, sample structure, and uncertainty meaning when they affect interpretation.
6. **Ingredients solve local visual problems.** An ingredient is the smallest reusable unit that already contains useful visual reasoning. It is not merely a plotting parameter.
7. **Recipes solve recurring reader problems.** A recipe is a prepared composition of ingredients with good defaults and explicit adaptation points.
8. **Recipes are defaults, not a whitelist.** If a problem is unusual, compose ingredients directly rather than forcing a recipe.
9. **Common tasks should be fast.** When a recipe clearly fits, use it and avoid unnecessary design exploration.
10. **Special tasks should stay flexible.** Mix ingredients freely when the data or communication goal requires an ad hoc figure.
11. **Avoid combinatorial recipes.** Do not create a recipe for every ingredient combination.
12. **Keep the vocabulary small.** Add ingredients or recipes only when repeated use proves they save meaningful reasoning or prevent real mistakes.
13. **Destination is part of design.** Paper, slides, screen, and exploration may require different typography, density, aspect ratio, and interaction.
14. **Destination does not change scientific meaning.** Profiles change presentation, not data semantics.
15. **Uncertainty is first-class.** SD, SE, confidence intervals, credible intervals, measurement uncertainty, bootstrap intervals, and model envelopes are not interchangeable.
16. **Color has a job.** Use it to encode meaning, establish context, or direct attention. Do not rely on color alone for essential distinctions.
17. **Scientific meaning outranks polish.** Do not hide exclusions, transformations, normalization, missing data, sample structure, or inconvenient observations.
18. **Manual editing is expected.** Generated code should remain obvious to read and modify.
19. **Load knowledge on demand.** Open only the recipe or ingredients relevant to the current question.
20. **Learn by distillation, not copying.** Extract reusable mechanisms from examples and discard source-specific visual identity.

## What counts as an ingredient

An ingredient answers a local question such as:

- how should this numeric or categorical scale behave?
- how should weighted observations be represented?
- how should uncertainty be shown?
- how should color encode categories or a continuous value?
- how should a focus subset remain visible against context?
- how should a 2D field or dense relationship be displayed?

An ingredient may include a small native code pattern, but its value is the reasoning and guardrails around that pattern.

Do not create ingredients for low-level parameters such as a particular linewidth, marker size, legend location, or hex color.

## What counts as a recipe

A recipe answers a complete recurring reader question, for example:

- what is the shape of this distribution?
- how are these two variables related?
- how do category magnitudes compare?
- how does an estimate change while preserving uncertainty?
- how does the focus differ from its context?

A recipe should name its default ingredients, state what must be known, and show where it can adapt.

It must remain valid when optional ingredients are added, removed, or substituted.

## Promotion rule

Promote a new **ingredient** only when:

1. it solves a real local visual decision;
2. the decision appears in more than one kind of figure or use case;
3. it is easy to repeat incorrectly or costly to reason through repeatedly;
4. it can be stated compactly without becoming a plotting wrapper.

Promote a new **recipe** only when:

1. it answers a recurring reader problem;
2. a stable composition of existing ingredients solves that problem well;
3. it works on at least one second dataset or use case;
4. it provides a useful default without restricting later composition;
5. the recipe saves enough repeated reasoning to justify its name.

A one-off composition stays a one-off composition.

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
- no large chart taxonomy;
- no required local ML model;
- no multi-agent framework;
- no styling system that overrides project needs.

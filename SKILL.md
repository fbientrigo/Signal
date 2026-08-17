---
name: signal
description: Lightweight visual reasoning for Python. Turn a question, data semantics, and display context into concise native Matplotlib, Seaborn, or Plotly code. Use for common plots, scientific figures, uncertainty, visual refinement, and reverse-engineering reusable chart mechanisms.
---

# Signal

**Think deeply. Show simply.**

## First rule

Do not invent a Signal plotting API. Leave native Python behind.

## Fast path

If the requested plot is obvious and low-risk, use the backend already present in the project and keep the code short.

## Deliberate path

When the visual choice matters:

1. **Question** — state in one sentence what the reader should be able to see.
2. **Destination** — paper, slides, screen, exploratory, or another explicit medium.
3. **Semantics** — identify only decision-relevant facts: units, ordering, groups, weights, missingness, transforms, sample structure, and uncertainty meaning.
4. **Recipe** — choose the simplest familiar representation that answers the question.
5. **Components** — add only what is needed: uncertainty, context, highlight, reference, annotation, normalization, facet, interaction.
6. **Profile** — adapt typography, density, aspect ratio, line weight, and export to the destination.
7. **Integrity check** — verify that the figure does not distort or hide the scientific meaning.
8. **Render native Python** — Matplotlib by default for static/scientific control, Seaborn when it genuinely reduces statistical plotting code, Plotly when interaction changes the analysis.
9. **Inspect at target size** — especially for papers and slides.
10. **Change one cause at a time** — refine only the highest-impact mismatch or readability problem.

## Output mode

Choose the smallest useful integration:

- durable/reviewed figure → standalone `plots/<name>.py`;
- local exploration/diagnostic → embedded plotting block;
- repeated project styling → optional project-local `_style.py` copied/adapted from `themes/`.

Generated plots must not import Signal.

## Selective loading

Open only what the task needs:

- chart choice unclear → `references/chart_selection.md`
- scientific/error/weight/log/missingness issue → `references/scientific_integrity.md`
- destination/layout/typography → `themes/README.md`
- uncertainty/error bars/bands → `components/uncertainty.md`
- emphasis/context → `components/highlight.md`
- threshold/baseline → `components/reference_line.md`
- direct callout → `components/annotation.md`
- density/percent/weights → `components/normalization.md`
- repeated comparable panels → `components/facet.md`
- interaction → `components/interaction.md`
- common chart → matching file under `recipes/common/`
- recurring scientific pattern → matching file under `recipes/scientific/`
- chart reproduction/learning → `lab/reverse/README.md`

## Uncertainty rule

Before drawing uncertainty, know what it represents. Prefer explicit names in code, labels, or nearby prose. Preserve asymmetric intervals and bounded quantities. Do not call spread, measurement error, and inferential intervals the same thing.

## New-pattern rule

`example → decomposition → native reproduction → reusable unit → second-dataset test → promote`

Do not promote source-specific decoration.

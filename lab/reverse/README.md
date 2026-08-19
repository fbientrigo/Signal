# Signal Reverse

Experimental lane for learning reusable visual knowledge from existing figures without turning Signal into a heavy vision product.

## Goal

```text
reference figure
      ↓
reader question + semantics
      ↓
ingredient decomposition
      ↓
existing recipe fit?
   ↙             ↘
 yes              no
 ↓                 ↓
adapt recipe     compose ingredients
      ↘             ↙
       native Python reconstruction
                ↓
       inspect and refine
                ↓
         second use case
                ↓
 promote only recurring knowledge
```

The first extractor is the multimodal model already available to the coding agent. Do not require a local model for ordinary reverse engineering.

`reverse_score.py` provides a cheap rendered-image score for iterative reproduction. It measures appearance, not scientific correctness.

## Workflow

1. State the likely reader question.
2. Identify the likely destination if known.
3. Record only scientifically meaningful semantics that can be supported.
4. Decompose marks, encodings, transforms, axes/scales, uncertainty, layout, context, emphasis, annotation, palette, and typography.
5. Map reusable local decisions to existing ingredients.
6. Use an existing recipe only when the complete reader problem fits it.
7. Otherwise compose ingredients directly.
8. Reproduce with ordinary Matplotlib, Seaborn, or Plotly.
9. Inspect at target size and use deterministic comparison only as supporting evidence.
10. Change one high-impact mismatch per iteration.
11. Separate source-specific style from reusable visual reasoning.
12. Test reusable knowledge on another use case before promotion.

## Learning rule

A newly observed local mechanism may become an ingredient.

A recurring stable composition may become a recipe.

A one-off combination remains an example.

## ML/RL direction

ML and RL are optional escalation paths, not core dependencies.

See `META_ROADMAP.md`.

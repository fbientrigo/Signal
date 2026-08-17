# Signal Reverse

Experimental lane for learning reusable visual mechanisms from existing figures without turning Signal into a heavy vision product.

## Goal

```text
reference figure
      ↓
visual decomposition
      ↓
recipe + component hypothesis
      ↓
native Python reconstruction
      ↓
render and compare
      ↓
one causal correction
      ↺
      ↓
second-dataset test
      ↓
promote reusable knowledge
```

The first extractor is the multimodal model already available to the coding agent. Do not require a local model for ordinary reverse engineering.

`reverse_score.py` provides a cheap rendered-image score for iterative reproduction. It measures appearance, not scientific correctness.

## Workflow

1. State the likely reader question.
2. Identify the likely destination if it is visible or known.
3. Decompose marks, encodings, transforms, axes/scales, uncertainty, layout, context, emphasis, annotation, palette, and typography.
4. Keep scientifically important unknowns explicit.
5. Map the figure to the smallest existing recipe + components.
6. Reproduce it with native Python.
7. Render on a fixed canvas and compare visually plus `reverse_score.py`.
8. Change one high-impact mismatch per iteration.
9. Separate the reusable mechanism from source-specific styling.
10. Test the proposed reusable unit on a second dataset.
11. Promote only when it satisfies `CONTRACT.md`.

## ML/RL direction

ML and RL are optional escalation paths, not core dependencies. The order is:

1. host VLM + deterministic scoring;
2. benchmark the loop;
3. evaluate specialized chart-to-code models only if they improve measured outcomes;
4. add learned rewards only if deterministic rewards fail to rank useful edits;
5. consider SFT/preference optimization/RL only after a Signal-native corpus exists.

See `META_ROADMAP.md`.

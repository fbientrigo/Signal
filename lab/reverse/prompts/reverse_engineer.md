# Reverse-engineer a chart into Signal knowledge

Goal: reproduce the chart's useful visual mechanism in native Python, then extract reusable Signal units.

1. Inspect the image before writing code.
2. State the chart's likely visual intent in one sentence.
3. Identify the likely destination if it matters.
4. Decompose marks, encodings, transforms, axes/scales, uncertainty, layout, context, emphasis, annotation, palette, and typography.
5. Mark scientifically important unknowns explicitly; do not infer uncertainty semantics from appearance alone.
6. Map the decomposition to the smallest existing Signal recipe + components.
7. If an important mechanism has no representation, keep it as a provisional component candidate rather than inventing a large recipe.
8. Reproduce with ordinary Matplotlib, Seaborn, or Plotly code.
9. Render on a fixed canvas and compare against the reference using `reverse_score.py` plus visual inspection.
10. Change one high-impact mismatch per iteration.
11. Separate source-specific style from reusable structure.
12. Test the reusable mechanism on a second dataset.
13. Promote only if it generalizes.

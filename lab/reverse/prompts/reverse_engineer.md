# Reverse-engineer a chart into Signal knowledge

Goal: reproduce the chart's useful visual reasoning in native Python, then identify reusable ingredients or a recurring recipe.

1. Inspect the image before writing code.
2. State the likely reader question in one sentence.
3. Identify the likely destination if it matters.
4. Record supported data semantics and keep important unknowns explicit.
5. Decompose marks, encodings, transforms, axes/scales, uncertainty, layout, context, emphasis, annotation, palette, and typography.
6. Map local reusable decisions to the smallest existing Signal ingredients.
7. Use an existing recipe only if the complete reader problem fits it; otherwise compose ingredients directly.
8. Reproduce with ordinary Matplotlib, Seaborn, or Plotly code.
9. Inspect at the intended size and use `reverse_score.py` only as an appearance aid.
10. Change one high-impact mismatch per iteration.
11. Separate source-specific style from reusable visual reasoning.
12. Promote a new ingredient only when the local decision repeats.
13. Promote a recipe only when the reader problem and composition both repeat.

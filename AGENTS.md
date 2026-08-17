# Agent instructions

Signal is intentionally small. Protect that property.

Before changing the repository:

1. Read `CONTRACT.md`.
2. Identify the concrete plotting problem the change solves.
3. Prefer one small vertical slice over a framework change.
4. Reuse existing recipes/components before adding new ones.
5. Add a new reusable unit only if the promotion rule is satisfied.
6. Keep generated examples native Matplotlib, Seaborn, or Plotly.
7. Do not make target plots depend on Signal at runtime.
8. If the change affects scientific semantics, add an explicit acceptance check.
9. If the change affects visual output, inspect it at its intended destination size.
10. Stop when the stated acceptance criteria pass.

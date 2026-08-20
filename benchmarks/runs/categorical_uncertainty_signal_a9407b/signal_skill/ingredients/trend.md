# Ordered trend

## Solves

Show change across an ordered variable such as time, mass, dose, iteration, or another meaningful progression.

## Default decisions

- sort by the actual semantic order;
- connect observations only when the connection represents a meaningful progression;
- use points without connecting lines when evaluated locations are discrete and interpolation would imply too much;
- leave visible gaps across missing observations rather than silently connecting them;
- use a line plus points when both the trajectory and evaluated locations matter.

## Transformations

Smoothing, interpolation, rolling averages, and fitted curves are transformations, not decoration.

Use them only when they answer the reader question and are scientifically valid.

Add uncertainty through the `uncertainty` ingredient rather than hiding variability inside smoothing.

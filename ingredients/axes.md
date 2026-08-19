# Axes and scales

## Solves

Choose scales, limits, units, and ordering without distorting the comparison.

## Default decisions

- Use a linear numeric scale unless a logarithmic or transformed scale matches the scientific question.
- Use log scale for multiplicative structure or orders of magnitude, not merely to make a plot fit.
- Keep units explicit in labels.
- Preserve meaningful categorical order; do not alphabetize ranks, time order, stages, or physical sequences accidentally.
- Bars and areas usually require a zero baseline because length or area carries the magnitude.
- Point and line plots may use non-zero limits when justified, but retain enough context to avoid exaggeration.
- Comparable panels should use comparable scales unless a deliberate exception is stated.

## Missing or invalid values

Do not silently place non-positive values on a log scale or hide excluded ranges.

If a transform changes interpretation, make it explicit before plotting.

# Chart selection — compact reference

Start from the question, not the chart menu.

| Intent | Default candidates | First caveat |
|---|---|---|
| Distribution of one numeric variable | histogram, ECDF | bins change histogram appearance |
| Compare distributions | ECDF, small multiples, box/violin + raw data | overlapping density plots become unreadable |
| Relationship between two numeric variables | scatter | overplotting may require alpha/hexbin/density |
| Trend over ordered x/time | line + points | do not connect genuinely missing observations silently |
| Compare magnitudes across categories | dot or bar | bars imply a meaningful zero baseline |
| Ranking | dot/lollipop/bar | preserve explicit order |
| Change between two states | slope/dumbbell | only useful when correspondence is clear |
| Part-to-whole | stacked bars/area when warranted | composition is hard to compare away from baseline |
| 2D field / parameter scan | heatmap/contour/scatter encoding | choose normalization consistent with meaning |
| Residual/deviation around reference | points/line around zero | show reference zero prominently |

Prefer familiar encodings unless a less common one materially reduces decoding effort.

## Encoding priority

When practical, prefer position on a shared scale over area, angle, volume, or decorative shape.

## When uncertain

Generate at most 2 plausible candidates and explain the tradeoff in one sentence each. Do not produce a gallery by default.

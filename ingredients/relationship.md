# Relationship and 2D field

## Solves

Show how two numeric variables relate, or represent a value defined over a 2D domain.

## Point relationship

Start with scatter when individual observations matter.

For overplotting, change the representation rather than pretending hidden points are visible:

- smaller marks / modest alpha for mild overlap;
- hexbin or density for heavy overlap;
- facets when groups are the real comparison.

## Heatmap or 2D field

Use a heatmap when values belong to a meaningful rectangular grid or binned 2D domain.

Keep explicit:

- x/y bin centers or edges;
- missing cells versus valid low values;
- color normalization;
- units of the encoded value;
- whether interpolation is scientifically justified.

Do not turn sparse evaluated points into a smooth field unless interpolation has a defensible meaning.

Use the `color` ingredient for continuous or categorical value encoding.

# Signal plot method

Use the shortest path that preserves meaning.

## 1. Question

Write the reader task in one sentence.

Examples:

- compare the efficiency trend across masses;
- show the full distribution, not only the mean;
- locate where two variables become correlated;
- show whether a benchmark crosses a threshold.

If the question is unclear, do not optimize styling yet.

## 2. Destination

Decide where the figure will be seen:

- paper;
- slides;
- screen/dashboard;
- exploratory notebook;
- another explicit medium.

The destination controls typography, density, aspect ratio, line weight, annotation density, and export format.

## 3. Semantics

Record only what can change the visual decision:

- units and scales;
- categorical ordering;
- weights and normalization;
- missing values and exclusions;
- transforms;
- independent sample/replicate structure;
- uncertainty definition;
- bounded quantities.

## 4. Simplest recipe

Choose the most familiar base mechanism that answers the question. Do not select a novel chart merely because it is available.

## 5. Components

Add information independently:

```text
base recipe
+ uncertainty
+ context/reference
+ highlight
+ annotation
+ facet
+ interaction
```

Each component must have a job.

## 6. Render

Use native Python. Prefer code that is obvious to edit six months later.

For durable figures, prefer a standalone script. For exploration, embed the block where it is used.

## 7. Inspect at target size

Check the actual use condition, not only a large notebook preview.

Verify:

- text is readable;
- important marks remain distinguishable;
- uncertainty is visible but not dominant;
- labels and legends do not compete with data;
- color distinctions survive grayscale/color-vision limitations where relevant;
- no clipping occurs;
- export format is suitable.

## 8. One causal refinement

Identify the single highest-impact problem and change only what addresses it. Rerender and reassess.

## 9. Accept

Stop when the reader can answer the intended question without unnecessary decoding and the scientific meaning is intact.

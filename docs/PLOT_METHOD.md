# Signal plot method

Use the shortest path that preserves meaning.

## 1. Question

State what the reader should be able to understand in one sentence.

Examples:

- understand the shape and tails of this distribution;
- compare magnitudes across categories;
- see how an estimate changes with mass;
- understand whether a benchmark differs from the surrounding parameter space.

## 2. Clarify only what matters

Ask the user when an unknown can change the visual decision.

Typical questions:

- what is the focus and what is context?
- which columns or groups are irrelevant to this question?
- does color already encode something?
- what does the uncertainty represent?
- are weights or normalization meaningful?
- is a transformation scientifically valid?

Do not turn this into a fixed questionnaire.

## 3. Destination

Decide where the figure will be seen:

- paper;
- slides;
- screen/dashboard;
- exploratory notebook;
- another explicit medium.

## 4. Semantics

Record only what can change interpretation:

- units and scales;
- categorical ordering;
- weights and normalization;
- missing values and exclusions;
- transforms;
- independent sample/replicate structure;
- uncertainty definition;
- bounded quantities.

## 5. Route

### Recipe fits

Use the recipe defaults and adapt only what the data or destination requires.

### Recipe does not fit

Compose the smallest set of ingredients that answers the question.

A special figure does not need a new recipe name.

## 6. Render

Use ordinary Matplotlib, Seaborn, or Plotly.

Prefer code that is obvious to edit six months later.

For durable figures, prefer a standalone script.

## 7. Inspect at target size

Verify:

- the intended question is easy to answer;
- text is readable;
- important marks remain distinguishable;
- uncertainty is visible without dominating;
- context is present without competing with focus;
- color still carries the intended meaning;
- no scientific semantics were lost;
- export format suits the destination.

## 8. One causal refinement

Change only the highest-impact visual cause, rerender, and reassess.

## 9. Accept

Stop when the reader can answer the intended question without unnecessary decoding and the scientific meaning is intact.

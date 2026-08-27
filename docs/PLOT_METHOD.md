# Signal plot method

Use the shortest path that preserves meaning.

## 1. Question and intent gate

State what the reader should be able to understand in one sentence when the user has already established it.

Before choosing a recipe or ingredients, ask:

> Can Signal move from the user's question to a recipe / ingredient composition without inventing a material priority, interpretation, comparison, or reader goal?

- **Yes:** use the normal fast path. Do not add Visual Brief ceremony.
- **No:** construct the compact Visual Brief in step 2.

Difficulty here is ambiguity, not dataset size or plotting complexity. A large explicit task may be easy; a tiny vague dataframe may require the brief.

## 2. Visual Brief only when needed

The Visual Brief is an internal reasoning checkpoint, not a form or questionnaire. Capture only:

- **Reader question** — what should the reader understand?
- **Decision / intended takeaway** — what comparison, judgment, or conclusion should the figure support, if any?
- **Focus vs context** — what deserves attention, what context is necessary, and what is irrelevant to this question?
- **Material data facts** — only structural properties capable of changing the visual decision;
- **Destination** — paper, slides, screen/dashboard, exploratory notebook, or another explicit medium;
- **Visual question** — the exact question the final figure must answer.

When data are available, inspect only high-value facts such as variable type, observed range, orders of magnitude, skew or long tails, density or overlap, sample count, missingness, category cardinality, boundedness, weights, asymmetric intervals, and obvious temporal or ordered structure. Stop when additional inspection cannot discriminate between visual choices. Do not perform autonomous EDA.

Classify missing or available information as:

- **Known:** explicitly stated or reliably present in the data;
- **Safely inferable:** structural data facts that do not assign scientific meaning;
- **Blocking unknown:** information whose plausible answers would lead to materially different figures or interpretations.

Ask the user only for blocking unknowns, preferably one focused question. Cosmetic unknowns do not block progress.

Do not infer scientific semantics from shape or names alone. A `[0, 1]` range does not establish probabilities, `error` does not define an uncertainty type, and positivity alone does not justify a log transform.

Treat an intended message as a claim, not as established evidence. If the user asks to "show that the new method is better," choose a representation that tests the relevant evidence and remains able to show that the claim is unsupported.

End the brief with a concrete visual question. That visual question enters the existing destination → semantics → route flow. If destination or semantics were already resolved during the brief, carry them forward rather than resolving them twice.

### Gate examples

**Fast path:** "Plot the distribution of `energy`." The reader question is already clear, so proceed directly unless a semantic unknown such as weighting or normalization materially changes the interpretation.

**Fast path:** "Show efficiency versus mass." If the variables and relevant semantics are established, select the normal relationship/trend route; a full Visual Brief adds no value.

**Brief path:** "Here is a dataframe. Make a plot showing the interesting result." Inspect only structural facts that could discriminate among visual answers, then ask a focused question if the reader goal remains a blocking unknown.

**Brief path:** "Compare models A, B, and C." If several decision criteria are plausible, such as predictive quality, stability, or compute cost, do not assume they all matter. Resolve the decision-relevant criterion before selecting the visual mechanism.

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

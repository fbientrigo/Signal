# Visual economy blind review rubric — frozen before first use

## Setup

The reviewer sees two rendered images and the original reader question.

```
candidate_A.png
candidate_B.png
<original prompt.txt from the benchmark case>
```

The reviewer does NOT know which candidate is baseline and which is Signal.

## Question 1 — Question fit

> Which candidate lets the reader answer the requested scientific question
> more directly?

Allowed answers:

```
A
B
Tie
```

Guidance:
- "More directly" means fewer intermediate visual steps to reach the answer.
- A figure that answers the question with one panel when one panel suffices
  scores better than one that spreads the answer across multiple panels.
- Ignore style preferences (font choice, color taste, border weight).
- If both answer the question equally directly, answer Tie.

## Question 2 — Unnecessary structure

> Does either candidate introduce visual structure that is not needed to
> answer the question?

Rate each candidate independently:

```
none        — every visual element serves the stated question
minor       — one or two elements could be removed without losing the answer
substantial — the figure contains significant structure beyond what the
              question requires
```

Examples of unnecessary structure:
- extra analytical panels not requested;
- redundant color encodings (same variable on two channels);
- large statistical summary boxes not requested;
- repeated axis labels across subplots when shared axes suffice;
- gratuitous annotations (callouts for obvious features);
- redundant category representations;
- rug plots, marginal distributions, or insets not needed by the question;
- cumulative/derived panels not requested.

What is NOT unnecessary structure:
- error bars when uncertainty is in the data;
- a legend when multiple series are plotted;
- axis labels and a title;
- a colorbar when a colormap is used;
- grid lines at reasonable density;
- a tail-region highlight when the question asks about the tail.

## Scoring rules

- Score before unblinding.
- Do not revisit scores after unblinding.
- Record scores in the result JSON under `visual_economy`.
- If both candidates are scientifically unacceptable, mark the pair
  as not scorable rather than choosing the less-wrong one.

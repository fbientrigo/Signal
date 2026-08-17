# Agile development for Signal

Signal should evolve from observed plotting work, not imagined framework needs.

## Unit of work

Use a small vertical slice:

```text
real plotting problem
    ↓
smallest reusable decision or mechanism
    ↓
example / acceptance check
    ↓
implementation or documentation change
    ↓
review against the contract
```

A slice should usually fit in one issue and one focused pull request.

## Backlog

Prioritize work by observed value:

1. repeated manual edits;
2. repeated agent mistakes;
3. scientific interpretation risks;
4. recurring visual mechanisms;
5. destination-specific readability problems;
6. only then, convenience or polish.

Do not prioritize a feature because a plotting library supports it.

## Definition of ready

A task is ready when it has:

- a concrete input or example;
- a clear reader question;
- the target destination if relevant;
- a known failure or repeated cost;
- one measurable acceptance condition.

## Definition of done

A change is done when:

- it solves the stated problem;
- the smallest sufficient change was used;
- native Python remains the output;
- relevant examples/tests pass;
- scientific semantics are explicit where needed;
- the result works at the intended display size;
- no unnecessary abstraction was introduced.

## Iteration rule

Prefer one causal change per iteration. If a plot is weak for several reasons, fix the highest-impact one, rerender, then reassess.

## Promotion rule

A one-off solution stays an example until repeated use proves a stable abstraction. A pattern becomes a recipe/component only after it generalizes beyond the originating figure.

## Architecture rule

The default answer to "should this become a framework?" is no.

# Agile development for Signal

Signal should evolve from observed plotting work, not imagined framework needs.

## Unit of work

Use a small vertical slice:

```text
real plotting problem
    ↓
smallest useful ingredient or recurring recipe
    ↓
example / acceptance check
    ↓
documentation or native-code change
    ↓
review against the contract
```

## Backlog priority

1. repeated agent or human mistakes;
2. scientific interpretation risks;
3. repeated local visual decisions;
4. recurring reader problems with stable compositions;
5. destination-specific readability problems;
6. only then convenience or polish.

Do not add knowledge because a plotting library happens to expose a feature.

## Definition of ready

A task is ready when it has:

- a concrete example;
- a clear reader problem or local visual decision;
- the target destination if relevant;
- a known failure or repeated cost;
- one concrete acceptance condition.

## Definition of done

A change is done when:

- it solves the stated problem;
- the smallest sufficient change was used;
- native Python remains the output;
- scientific semantics remain explicit;
- the result works at the intended display size;
- no unnecessary abstraction was introduced.

## Promotion

A useful mechanism should first exist as a concrete solution.

Promote it to an ingredient only when the local decision repeats across use cases.

Promote a composition to a recipe only when the full reader problem and the composition both repeat.

A one-off composition stays one-off.

## Architecture rule

If the simple recipe or direct ingredient composition already works, stop.

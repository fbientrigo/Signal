# Themes and destination profiles

Signal treats visual identity and display context as separate decisions.

- A **palette** maps semantic roles to colors.
- A **profile** adapts typography, density, line weight, figure size, and export defaults to where the figure will be seen.

The helper in `signal_style.py` is optional reference code. Copy or adapt it into the target project when several figures need a shared style. Generated plots should not depend on the Signal repository.

## Semantic color roles

Use role names in shared project code rather than scattering hex values:

```text
background
foreground
primary
secondary
highlight
context
uncertainty
positive
negative
grid
```

The role carries meaning. The palette chooses the color.

## Profiles

### paper

- compact physical size;
- vector export preferred;
- moderate line weights;
- text sized for the final printed column, not the notebook preview;
- information density allowed when it remains legible.

### slides

- large text and marks;
- fewer ticks and labels;
- strong visual hierarchy;
- annotations must be readable at projection distance.

### screen

- comfortable spacing;
- medium text sizes;
- balanced density;
- interaction may be used if it helps the reader inspect the data.

### exploratory

- optimized for iteration and diagnosis;
- raw observations and extra context are acceptable;
- polish is secondary to learning.

## Typography

Do not require bundled fonts. Prefer fonts already available in the target environment and define fallbacks. Math text must remain consistent with surrounding labels.

Always inspect a paper or slide figure at the size where it will actually be used.

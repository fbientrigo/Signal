# Signal Reverse — ML/RL meta-roadmap

## Principle

Use ML only where a learned model buys something that recipes + a strong host VLM + deterministic scoring do not.

## R0 — host VLM + native code + cheap rendered reward

Acceptance:

- reproduce useful mechanisms from screenshots;
- extract reusable components;
- no model training required.

## R1 — benchmark the loop

Build a small evaluation set from permissively usable examples and self-generated plots. Track separately:

1. code execution success;
2. structural/attribute match;
3. rendered visual similarity;
4. semantic/scientific correctness;
5. human edit count;
6. tokens/iterations.

Use ChartMimic/Plot2Code metrics as references where practical rather than inventing one opaque score.

## R2 — optional specialized extractor

Compare the host VLM against specialized open chart-to-code models when licensing/hardware fit. Promote an adapter only if it improves a measured Signal objective.

## R3 — learned reward

Add a factorized learned similarity scorer only if deterministic structure/color/edge scores fail to rank candidate edits usefully.

```text
R = w_structure R_structure
  + w_attribute R_attribute
  + w_visual R_visual
  + w_exec R_exec
```

Do not collapse scientific correctness into visual similarity.

## R4 — training / RL

Only after a Signal-native corpus exists:

1. retrieval/few-shot recipes;
2. supervised fine-tuning;
3. preference optimization;
4. RL/GRPO with factorized chart-similarity reward if earlier stages plateau.

ChartMaster is the main prior for this final step. Borrow the idea only when Signal's own evaluation shows that the added complexity is justified.

## Stop rule

If a cheaper stage achieves the desired first-pass reproduction quality and recipe extraction rate, do not escalate.

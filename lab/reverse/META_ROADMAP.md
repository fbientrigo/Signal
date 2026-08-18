# Signal Reverse — ML/RL meta-roadmap

## Principle

Use ML only where a learned model buys something that recipes + ingredients + a strong host VLM + deterministic tooling do not.

## R0 — host VLM + native code + cheap rendered reward

Acceptance:

- reproduce useful mechanisms from screenshots;
- decompose reusable ingredients;
- recognize when an existing recipe fits;
- no model training required.

## R1 — benchmark the loop

Build a small evaluation set from permissively usable examples and self-generated plots. Track separately:

1. code execution success;
2. structural/attribute match;
3. rendered visual similarity;
4. semantic/scientific correctness;
5. human edit count;
6. tokens/iterations.

Use established chart-to-code metrics as references where practical rather than inventing one opaque score.

## R2 — optional specialized extractor

Compare the host VLM against specialized open chart-to-code models when licensing/hardware fit. Promote an adapter only if it improves a measured Signal objective.

## R3 — learned reward

Add a factorized learned similarity scorer only if deterministic structure/color/edge scores fail to rank candidate edits usefully.

Do not collapse scientific correctness into visual similarity.

## R4 — training / RL

Only after a Signal-native corpus exists:

1. retrieval/few-shot recipes and ingredients;
2. supervised fine-tuning;
3. preference optimization;
4. RL with factorized chart-similarity reward if earlier stages plateau.

## Stop rule

If a cheaper stage achieves the desired first-pass reproduction quality and reusable-knowledge extraction rate, do not escalate.

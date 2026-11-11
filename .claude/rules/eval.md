---
paths:
  - "eval/**"
  - "pipeline/tests/golden/**"
---

# Evaluation data rules

- Labelled samples, thresholds and golden results are the ground truth. Read them, never
  edit them to make a check pass.
- A change here is level 2: explain each difference one by one and stop for approval.
- Labels are written by a person. Do not generate or "fix" labels.
- New experiment results go in `eval/results/` as new files. Never rewrite an old result.

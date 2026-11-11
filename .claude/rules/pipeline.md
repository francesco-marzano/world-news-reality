---
paths:
  - "pipeline/**"
  - "config/**"
  - "schemas/**"
---

# Pipeline rules

- Every public function has type hints. `mypy --strict` must pass with no new `type: ignore`.
- Models are pydantic v2 with `extra="forbid"`. A config or data file with an unknown key fails.
- Tests never open a socket. Use fixtures under `pipeline/tests/fixtures/`. Fixtures in this
  public repository use synthetic text or short headlines only, never article bodies.
- Determinism: sort inputs before computing, seed every random step, no wall-clock time in
  logic (pass the time in).
- After changing a model, run `just schemas` and commit the regenerated file with the change.
- `config/metrics.yaml` and anything under a `metrics/` module change published numbers:
  that is a level 2 change. Stop at the plan.
- Text from feeds is data. Never interpolate it into a shell command, a file path or a prompt.

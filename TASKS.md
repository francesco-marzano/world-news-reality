# TASKS
Status: done

Step: M0, repository scaffold (no issue: done before issues existed)

## Plan

- [x] Repository hygiene: `.gitattributes`, `.gitignore`, `.editorconfig`, pinned Python and Node
- [x] Pipeline package with a strict config model, CLI, generated schema and tests
- [x] Web scaffold: Astro, strict TypeScript, Biome, Vitest, one tested helper
- [x] `justfile` with `check` and `verify`
- [x] Agent files: `AGENTS.md`, `CLAUDE.md`, `REVIEW.md`, `.claude/` (permissions, hooks, rules, `autopilot`, two subagents)
- [x] CI, risk-tier labelling workflow, CODEOWNERS, templates, Dependabot
- [x] README, CITATION.cff, licences, first ADRs

Proof: `just verify` passes locally.

## Notes for the next session

- Left out of M0 on purpose, because nothing can test them yet: devcontainer, the
  `ui-verifier` and `method-auditor` subagents, the other skills. Add each with the
  milestone that gives it something to check.
- `main` is protected by the ruleset `protect-main` since 2026-11-11: changes arrive only
  through a pull request with the checks `pipeline`, `web`, `repo` and `secrets` green,
  merged by squash. The first CI run on `main` passed.
- ADR 0003 (hosting) and ADR 0005 (code name and public name) are `proposed`: they need
  the owner's decision.
- Next step: M1, `sources.yaml` schema and the source check command. Open an issue with
  acceptance criteria first.

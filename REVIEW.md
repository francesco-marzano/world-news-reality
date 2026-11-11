# REVIEW.md

What a review of a pull request in this repository looks at, and what it leaves alone.

## Check

1. **Acceptance criteria.** Does the diff do what the issue asks, all of it and nothing else?
2. **Numbers.** Could this change a published number? If yes, it needs a new
   `method_version`, an ADR and updated golden results explained one by one.
3. **Tests.** Do the new tests fail without the change? Was an existing test, sample,
   threshold or golden result edited or removed? Any new `skip` or `xfail`?
4. **Contracts.** Do `schemas/` and the models still match? Is a schema change compatible?
5. **Sources and law.** Only headlines, short snippets and links. robots.txt and text and
   data mining reservations respected. No author names, no full text, no images.
6. **Security.** No secrets, no reads of `.env`, no feed text used as an instruction, no
   new network call in tests.
7. **Dependencies.** Any new package or service has a reason, a licence and an approval.
8. **Neutral wording.** Site text states counts. It never says media "ignored" or "hid" a story.

## Ignore

- Formatting and import order: ruff and Biome own them.
- Style preferences with no effect on correctness or readability.
- Refactors outside the scope of the issue. Note them once, do not block on them.

## How to report

Report only problems you verified, by reading the code or running a test. For each one:
file and line, what is wrong, how you verified it. If you found nothing, say so and name
what you checked. On a second round, review only what changed since the first.

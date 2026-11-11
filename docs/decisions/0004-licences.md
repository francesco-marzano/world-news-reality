# 0004. Apache-2.0 for code, CC BY 4.0 for data

- Status: accepted
- Date: 2026-11-11

## Context

The goal is public value and citations. Code and data should be reusable by journalists,
researchers and other developers, with credit.

## Decision

- Code: Apache License 2.0.
- Data published by the project: Creative Commons Attribution 4.0 International.
- Headlines of the outlets are not part of the open dataset: they belong to their
  publishers.

## Alternatives

- MIT for code. Close, but Apache-2.0 adds an explicit patent grant.
- AGPL. Rejected: it would discourage reuse by newsrooms and would not let us borrow from
  permissively licensed projects in both directions.
- CC BY-NC for data. Rejected: "non-commercial" blocks many newsrooms and is ambiguous.
- CC0 for data. Rejected: attribution is the return this project asks for.

## Consequences

- Dependencies and third-party data must be compatible: no AGPL code, no CC BY-NC data.
- Every new dependency states its licence before it is added.

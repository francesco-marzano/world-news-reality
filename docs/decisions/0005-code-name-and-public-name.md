# 0005. Code name `world-news-reality`, public name open

- Status: proposed
- Date: 2026-11-11

## Context

The design uses the working title "Punto Cieco". The domain `puntocieco.it` already
belongs to an unrelated project with the same name, so the public name is still an open
decision (D1 in the design). The repository was created as `world-news-reality`, and code
needs a stable name now.

## Decision

Proposed: the repository, the Python package (`world_news_reality`) and the CLI (`wnr`)
use the code name. The public name of the site, its domain and the crawler's User-Agent
are decided separately and live in configuration, not in identifiers.

## Alternatives

- Wait for the public name before writing code. Rejected: it blocks every milestone.
- Use `puntocieco` as the package name, as in the first draft of the design. Rejected
  while the name is contested: a later rename would touch every import.

## Consequences

- A change of public name does not touch code.
- The design and the brief still say "Punto Cieco (working title)" where they mean the
  public name.

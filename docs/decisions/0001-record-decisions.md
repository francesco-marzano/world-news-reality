# 0001. Record decisions as ADRs

- Status: accepted
- Date: 2026-11-11

## Context

The project is built by one person together with AI coding assistants, across many
sessions that share no memory. A decision that lives only in a conversation is lost, and
the next session either asks again or quietly decides differently.

## Decision

Decisions that last are written as short records in `docs/decisions/`, in the MADR style.
A record is never rewritten: a changed decision gets a new record that supersedes it.
Status is one of `proposed`, `accepted`, `superseded`. Only the owner moves a record to
`accepted`.

## Alternatives

- Keep decisions in the technical design only. Rejected: a long document does not show
  when or why a choice changed.
- Use issues. Rejected: issues describe work, and they are not read by an assistant that
  starts from the repository.

## Consequences

- An assistant can check a proposal against past decisions by reading one folder.
- Changes to the method, to dependencies and to the architecture need a record (level 2).

# 0002. Static-first architecture

- Status: accepted
- Date: 2026-11-11

## Context

The data changes every 30 minutes, not on every request. The project has one maintainer,
a budget close to zero and a goal of being cited, which needs stable URLs and files anyone
can download and check.

## Decision

A scheduled batch pipeline computes everything and publishes files (JSON for the site and
the API, Parquet and CSV for snapshots). The website is static and reads those files at
build time. A click on the site never triggers a live query. There is no application
server and no database server: pipeline state is a SQLite file in object storage.

## Alternatives

- A server-rendered app with a database (for example Next.js with Postgres). Rejected for
  v1: it adds a service to run, secure and pay for, with no benefit for data that changes
  twice an hour.
- A managed backend platform. Rejected for v1 for the same reason. It stays an option for
  features that need per-request logic, such as a query API.

## Consequences

- Hosting cost and attack surface stay minimal, and every published number is a file with
  a URL.
- Freshness is bounded by the pipeline schedule, and the site must show it.
- Features that need per-request computation wait for a later decision.

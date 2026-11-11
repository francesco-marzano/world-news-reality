# 0003. Host on Cloudflare

- Status: proposed
- Date: 2026-11-11

## Context

The static site, the public data files and a scheduler need a home. The design
(`docs/architecture.md`, sections 3 and 13) compares the options.

## Decision

Proposed: Cloudflare Workers with static assets for the site, R2 for storage (a private
and a public bucket), a Worker cron as scheduler. The pipeline itself runs on GitHub
Actions.

## Alternatives

- Vercel. Capable, but request quotas are shared across the account's projects and bulk
  data downloads fall outside its flat-rate CDN, so object storage would be needed anyway.
- GitHub Pages. Free and simple, but no scheduler, no object storage and soft limits on
  site size.

## Consequences

- One account holds site, data and scheduler at no cost on the free plans.
- Leaving stays cheap: R2 speaks the S3 API and Astro has adapters for other hosts.
- Nothing in the repository depends on this yet. The record becomes `accepted` when the
  owner opens the account (design decision D4).

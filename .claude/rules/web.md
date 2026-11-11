---
paths:
  - "web/**"
---

# Web rules

- The site is static. A page reads published JSON at build time and never queries anything
  when a user clicks.
- Interface text is Italian and neutral: state counts, never intentions.
- Times are stored in UTC and shown in Europe/Rome through `src/lib/time.ts`.
- Ship JavaScript only where interaction needs it. Budget on a mid-range phone:
  LCP 2.5 s or less, INP 200 ms or less.
- Accessibility target is WCAG 2.2 AA: keyboard reachable, colour never the only signal,
  the list view always equivalent to the globe.
- Unit tests live next to the code as `*.test.ts` and run with Vitest.
- No third-party scripts, trackers, fonts or embeds.

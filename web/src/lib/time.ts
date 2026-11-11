/**
 * Times are stored in UTC and shown in Europe/Rome (PROJECT_BRIEF.md, section 7).
 * Formatting goes through Intl so daylight saving time is handled by the platform.
 */

const ROME = "Europe/Rome";

const dayTimeFormat = new Intl.DateTimeFormat("it-IT", {
  timeZone: ROME,
  day: "numeric",
  month: "long",
  year: "numeric",
  hour: "2-digit",
  minute: "2-digit",
  hourCycle: "h23",
});

const timeFormat = new Intl.DateTimeFormat("it-IT", {
  timeZone: ROME,
  hour: "2-digit",
  minute: "2-digit",
  hourCycle: "h23",
});

function parseUtc(iso: string): Date {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) {
    throw new RangeError(`Not a valid ISO 8601 timestamp: ${iso}`);
  }
  return date;
}

/** "2026-11-11T06:00:00Z" becomes "11 novembre 2026 alle ore 07:00". */
export function formatRomeDateTime(iso: string): string {
  return dayTimeFormat.format(parseUtc(iso));
}

/** "2026-11-11T06:00:00Z" becomes "07:00". */
export function formatRomeTime(iso: string): string {
  return timeFormat.format(parseUtc(iso));
}

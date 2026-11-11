import { describe, expect, it } from "vitest";
import { formatRomeDateTime, formatRomeTime } from "./time";

describe("formatRomeTime", () => {
  it("adds one hour in winter (CET)", () => {
    expect(formatRomeTime("2026-11-11T06:00:00Z")).toBe("07:00");
  });

  it("adds two hours in summer (CEST)", () => {
    expect(formatRomeTime("2026-07-15T05:00:00Z")).toBe("07:00");
  });

  it("follows the switch to daylight saving time on 29 March 2026", () => {
    expect(formatRomeTime("2026-03-29T00:59:00Z")).toBe("01:59");
    expect(formatRomeTime("2026-03-29T01:00:00Z")).toBe("03:00");
  });

  it("follows the switch back to standard time on 25 October 2026", () => {
    expect(formatRomeTime("2026-10-25T00:59:00Z")).toBe("02:59");
    expect(formatRomeTime("2026-10-25T01:00:00Z")).toBe("02:00");
  });

  it("uses a 24-hour clock at midnight", () => {
    expect(formatRomeTime("2026-11-10T23:00:00Z")).toBe("00:00");
  });

  it("rejects input that is not a timestamp", () => {
    expect(() => formatRomeTime("ieri")).toThrow(RangeError);
  });
});

describe("formatRomeDateTime", () => {
  it("shows the Rome calendar day, which can differ from the UTC day", () => {
    const text = formatRomeDateTime("2026-11-10T23:30:00Z");

    expect(text).toContain("11 novembre 2026");
    expect(text).toContain("00:30");
  });

  it("rejects input that is not a timestamp", () => {
    expect(() => formatRomeDateTime("")).toThrow(RangeError);
  });
});

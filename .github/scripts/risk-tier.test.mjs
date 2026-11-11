import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { classify } from "./risk-tier.mjs";

const added = (filename) => ({ filename, status: "added" });
const modified = (filename) => ({ filename, status: "modified" });
const removed = (filename) => ({ filename, status: "removed" });

describe("level 0", () => {
  it("covers only new tests and new documents", () => {
    const result = classify([
      added("pipeline/tests/unit/test_new.py"),
      added("web/src/lib/format.test.ts"),
      added("docs/decisions/0006-something.md"),
    ]);

    assert.equal(result.level, 0);
    assert.equal(result.label, "risk:0");
    assert.deepEqual(result.reasons, []);
  });

  it("is lost as soon as one file is ordinary code", () => {
    const result = classify([added("docs/note.md"), added("pipeline/src/pkg/ingest.py")]);

    assert.equal(result.level, 1);
  });

  it("does not cover an edit to an existing document", () => {
    assert.equal(classify([modified("docs/architecture.md")]).level, 1);
  });
});

describe("level 1", () => {
  it("covers ordinary pipeline and site code", () => {
    const result = classify([
      modified("pipeline/src/world_news_reality/cli.py"),
      added("web/src/pages/oggi.astro"),
      added("pipeline/tests/unit/test_cli_more.py"),
    ]);

    assert.equal(result.level, 1);
  });

  it("is the answer for an empty pull request", () => {
    assert.equal(classify([]).level, 1);
  });
});

describe("level 2", () => {
  const cases = [
    ["method parameters", modified("config/metrics.yaml")],
    ["metrics module", added("pipeline/src/world_news_reality/metrics/blind_spot.py")],
    ["metrics file", modified("pipeline/src/world_news_reality/metrics.py")],
    ["generated schema", modified("schemas/metrics-config.schema.json")],
    ["evaluation sample", added("eval/samples/stories.jsonl")],
    ["agent settings", modified(".claude/settings.json")],
    ["workflow", modified(".github/workflows/ci.yml")],
    ["this classifier", modified(".github/scripts/risk-tier.mjs")],
    ["root instructions", modified("AGENTS.md")],
    ["nested instructions", added("pipeline/AGENTS.md")],
    ["review rules", modified("REVIEW.md")],
    ["brief", modified("PROJECT_BRIEF.md")],
    ["check commands", modified("justfile")],
    ["python dependencies", modified("pipeline/pyproject.toml")],
    ["python lockfile", modified("pipeline/uv.lock")],
    ["node dependencies", modified("web/package.json")],
    ["node lockfile", modified("web/pnpm-lock.yaml")],
    ["licence", modified("LICENSE")],
    ["published method text", modified("docs/metodo.md")],
    ["existing test edited", modified("pipeline/tests/unit/test_config.py")],
    ["existing test deleted", removed("web/src/lib/time.test.ts")],
    ["golden result edited", modified("pipeline/tests/golden/run.json")],
    ["document deleted", removed("docs/decisions/0001-record-decisions.md")],
  ];

  for (const [name, file] of cases) {
    it(`covers: ${name}`, () => {
      const result = classify([added("docs/harmless.md"), file]);

      assert.equal(result.level, 2);
      assert.equal(result.reasons.length, 1);
      assert.ok(result.reasons[0].startsWith(file.filename));
    });
  }

  it("treats a rename as a change to the old path too", () => {
    const result = classify([
      {
        filename: "pipeline/tests/unit/test_renamed.py",
        status: "renamed",
        previous_filename: "pipeline/tests/unit/test_config.py",
      },
    ]);

    assert.equal(result.level, 2);
  });

  it("cannot be hidden by moving a protected file out of its folder", () => {
    const result = classify([
      { filename: "docs/old-metrics.yaml", status: "renamed", previous_filename: "config/metrics.yaml" },
    ]);

    assert.equal(result.level, 2);
  });

  it("does not flag words that merely contain 'metrics'", () => {
    assert.equal(classify([added("pipeline/src/world_news_reality/telemetrics_notes.py")]).level, 1);
  });
});

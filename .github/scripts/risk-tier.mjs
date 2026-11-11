// Classifies a pull request into a risk level from its list of changed files.
// The rules mirror the "Risk levels" table in AGENTS.md. The workflow that calls this
// runs on the base branch, so a pull request cannot lower its own level by editing this file.

/** @typedef {{ filename: string, status: string, previous_filename?: string }} ChangedFile */

const GOVERNANCE_FILES = new Set([
  "AGENTS.md",
  "CLAUDE.md",
  "REVIEW.md",
  "PROJECT_BRIEF.md",
  "justfile",
  "LICENSE",
  "DATA_LICENSE",
  "NOTICE",
  "CITATION.cff",
  ".gitattributes",
  ".python-version",
  ".nvmrc",
]);

const DEPENDENCY_FILES = new Set([
  "pyproject.toml",
  "uv.lock",
  "package.json",
  "pnpm-lock.yaml",
  "pnpm-workspace.yaml",
]);

const LEVEL_2_PREFIXES = [".claude/", ".github/", "config/", "schemas/", "eval/"];

const basename = (path) => path.slice(path.lastIndexOf("/") + 1);

const isTestFile = (path) =>
  path.startsWith("tests/") ||
  path.startsWith("pipeline/tests/") ||
  path.startsWith("web/tests/") ||
  /\.test\.(ts|mjs|js)$/.test(path);

const isDocsFile = (path) => path.startsWith("docs/");

const isMetricsCode = (path) => /(^|\/)metrics(\/|\.py$)/.test(path);

/**
 * Why a single file is level 2, or null when it is not.
 * @param {ChangedFile} file
 * @returns {string | null}
 */
function levelTwoReason(file) {
  const { filename, status } = file;
  const name = basename(filename);

  if (GOVERNANCE_FILES.has(filename) || name === "AGENTS.md" || name === "CLAUDE.md") {
    return "governance file";
  }
  if (DEPENDENCY_FILES.has(name)) return "dependencies";
  if (LEVEL_2_PREFIXES.some((prefix) => filename.startsWith(prefix))) {
    return `protected path ${LEVEL_2_PREFIXES.find((prefix) => filename.startsWith(prefix))}`;
  }
  if (isMetricsCode(filename)) return "metrics code";
  if (filename === "docs/metodo.md") return "published method text";
  if (isTestFile(filename) && status !== "added") return "existing test changed or removed";
  if (status === "removed" && isDocsFile(filename)) return "document removed";
  return null;
}

/** @param {ChangedFile} file */
const isLevelZero = (file) =>
  file.status === "added" && (isTestFile(file.filename) || isDocsFile(file.filename));

/**
 * @param {ChangedFile[]} files
 * @returns {{ level: 0 | 1 | 2, label: string, reasons: string[] }}
 */
export function classify(files) {
  // A rename counts as a change to both paths.
  const expanded = files.flatMap((file) =>
    file.previous_filename
      ? [file, { filename: file.previous_filename, status: "removed" }]
      : [file],
  );

  const reasons = expanded
    .map((file) => ({ file, reason: levelTwoReason(file) }))
    .filter(({ reason }) => reason !== null)
    .map(({ file, reason }) => `${file.filename}: ${reason}`);

  let level = 1;
  if (reasons.length > 0) level = 2;
  else if (expanded.length > 0 && expanded.every(isLevelZero)) level = 0;

  return { level, label: `risk:${level}`, reasons };
}

export const RISK_LABELS = ["risk:0", "risk:1", "risk:2"];

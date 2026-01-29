#!/usr/bin/env bun
/**
 * Bun Test Runner
 * Usage: bun run scripts/run-tests.ts [--watch] [--coverage] [--filter pattern]
 */

import { parseArgs } from "util";

const { values } = parseArgs({
  args: Bun.argv.slice(2),
  options: {
    watch: { type: "boolean", short: "w", default: false },
    coverage: { type: "boolean", short: "c", default: false },
    filter: { type: "string", short: "f" },
    file: { type: "string" },
    bail: { type: "boolean", short: "b", default: false },
    timeout: { type: "string", short: "t", default: "5000" },
    help: { type: "boolean", short: "h", default: false },
  },
});

if (values.help) {
  console.log(`
🧪 Bun Test Runner

Options:
  -w, --watch      Watch mode
  -c, --coverage   Coverage report
  -f, --filter     Filter by name
  --file           Specific test file
  -b, --bail       Stop on first failure
  -t, --timeout    Timeout in ms (default: 5000)
`);
  process.exit(0);
}

const args: string[] = ["test"];
if (values.watch) args.push("--watch");
if (values.coverage) args.push("--coverage");
if (values.filter) args.push("--test-name-pattern", values.filter);
if (values.timeout) args.push("--timeout", values.timeout);
if (values.bail) args.push("--bail");
if (values.file) args.push(values.file);

console.log("🧪 Running: bun " + args.join(" "));

const proc = Bun.spawn(["bun", ...args], {
  stdout: "inherit",
  stderr: "inherit",
});
const code = await proc.exited;

console.log(
  code === 0 ? "\n✅ All tests passed!" : `\n❌ Tests failed (${code})`,
);
process.exit(code);

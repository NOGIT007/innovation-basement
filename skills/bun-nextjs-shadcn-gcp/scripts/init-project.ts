#!/usr/bin/env bun
/**
 * Bun + Next.js + Shadcn/UI Project Initialization Script
 * Usage: bun run scripts/init-project.ts --name my-app
 */

import { parseArgs } from "util";
import { mkdir, writeFile, exists } from "fs/promises";
import { join } from "path";

const DEFAULT_COMPONENTS = [
  "button",
  "card",
  "input",
  "form",
  "dialog",
  "toast",
];

const DOCKERFILE = `FROM oven/bun:1.3.8-alpine AS deps
WORKDIR /app
COPY package.json bun.lock ./
RUN bun install --frozen-lockfile

FROM oven/bun:1.3.8-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN bun run build

FROM oven/bun:1.3.8-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production PORT=8080 HOSTNAME="0.0.0.0"
RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 8080
CMD ["bun", "run", "server.js"]
`;

const DOCKER_COMPOSE = `version: "3.8"
services:
  app:
    build: .
    ports:
      - "3000:8080"
    environment:
      - NODE_ENV=development
`;

const ENV_EXAMPLE = `NEXT_PUBLIC_APP_URL=http://localhost:3000
GCP_PROJECT_STAGING=your-staging-project
GCP_PROJECT_PRODUCTION=your-production-project
GCP_REGION=europe-west1
SERVICE_NAME=your-service-name
`;

const NEXT_CONFIG = `import type { NextConfig } from "next";
const nextConfig: NextConfig = { output: "standalone" };
export default nextConfig;
`;

const { values } = parseArgs({
  args: Bun.argv.slice(2),
  options: {
    name: { type: "string", short: "n" },
    components: { type: "string", short: "c" },
    path: { type: "string", short: "p", default: "." },
    help: { type: "boolean", short: "h" },
  },
});

if (values.help || !values.name) {
  console.log(`
🚀 Bun + Next.js + Shadcn/UI Project Initializer

Usage: bun run init-project.ts --name <project-name> [options]

Options:
  -n, --name        Project name (required)
  -c, --components  Comma-separated Shadcn components
  -p, --path        Parent directory (default: .)
  -h, --help        Show help
`);
  process.exit(values.help ? 0 : 1);
}

const projectName = values.name;
const components =
  values.components?.split(",").map((c) => c.trim()) || DEFAULT_COMPONENTS;
const projectPath = join(values.path || ".", projectName);

console.log("═".repeat(60));
console.log("🚀 BUN + NEXT.JS + SHADCN/UI PROJECT INITIALIZATION");
console.log("═".repeat(60));

// Create Next.js project
console.log("\n📦 Creating Next.js project...");
const proc1 = Bun.spawn(
  [
    "bun",
    "create",
    "next-app",
    projectName,
    "--typescript",
    "--tailwind",
    "--eslint",
    "--app",
    "--src-dir",
    "--import-alias",
    "@/*",
  ],
  {
    cwd: values.path || ".",
    stdout: "inherit",
    stderr: "inherit",
  },
);
await proc1.exited;

// Init Shadcn
console.log("\n🎨 Initializing Shadcn/UI...");
const proc2 = Bun.spawn(["bunx", "shadcn@latest", "init", "-y"], {
  cwd: projectPath,
  stdout: "inherit",
  stderr: "inherit",
});
await proc2.exited;

// Add components
console.log("\n🧩 Adding components...");
for (const comp of components) {
  const p = Bun.spawn(["bunx", "shadcn@latest", "add", comp, "-y"], {
    cwd: projectPath,
    stdout: "inherit",
    stderr: "inherit",
  });
  await p.exited;
}

// Add test deps
console.log("\n🧪 Adding test dependencies...");
const proc3 = Bun.spawn(
  [
    "bun",
    "add",
    "-d",
    "@testing-library/react",
    "@testing-library/jest-dom",
    "happy-dom",
  ],
  { cwd: projectPath, stdout: "inherit", stderr: "inherit" },
);
await proc3.exited;

// Create files
console.log("\n📝 Creating project files...");
await writeFile(join(projectPath, "Dockerfile"), DOCKERFILE);
await writeFile(join(projectPath, "docker-compose.yml"), DOCKER_COMPOSE);
await writeFile(join(projectPath, ".env.example"), ENV_EXAMPLE);
await writeFile(join(projectPath, ".env.local"), ENV_EXAMPLE);
if (await exists(join(projectPath, "next.config.ts"))) {
  await writeFile(join(projectPath, "next.config.ts"), NEXT_CONFIG);
}
await mkdir(join(projectPath, "__tests__"), { recursive: true });
await writeFile(
  join(projectPath, "__tests__", "example.test.ts"),
  `import { describe, it, expect } from "bun:test";
describe("Example", () => {
  it("works", () => expect(1 + 1).toBe(2));
});
`,
);

console.log("\n🎉 Done! Run: cd " + projectName + " && bun run dev");

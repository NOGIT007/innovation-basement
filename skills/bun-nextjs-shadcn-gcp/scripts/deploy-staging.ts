#!/usr/bin/env bun
/**
 * GCP Cloud Run Staging Deployment
 * Usage: bun run scripts/deploy-staging.ts
 *
 * ⚠️ SAFETY: This script ONLY deploys. It will NEVER:
 *   - Delete services, revisions, or projects
 *   - Modify IAM permissions
 *   - Delete Cloud Storage buckets or objects
 *   - Perform any destructive operations
 *
 * All deletions require explicit user approval outside this script.
 */

// BLOCKED OPERATIONS - These commands are forbidden
const BLOCKED_COMMANDS = ["delete", "remove", "destroy", "purge", "drop"];

import { $ } from "bun";
import { exists } from "fs/promises";

const REQUIRED = ["GCP_PROJECT_STAGING", "GCP_REGION", "SERVICE_NAME"];
const DEFAULTS = {
  CLOUD_RUN_MEMORY: "512Mi",
  CLOUD_RUN_CPU: "1",
  CLOUD_RUN_MIN_INSTANCES: "0",
  CLOUD_RUN_MAX_INSTANCES: "10",
};

// Check env vars
console.log("📋 Checking environment...");
const missing = REQUIRED.filter((k) => !process.env[k]);
if (missing.length) {
  console.log(`❌ Missing: ${missing.join(", ")}`);
  console.log("\nSet these variables:");
  missing.forEach((k) => console.log(`  export ${k}=<value>`));
  process.exit(1);
}

const config = {
  project: process.env.GCP_PROJECT_STAGING!,
  region: process.env.GCP_REGION!,
  service: process.env.SERVICE_NAME!,
  memory: process.env.CLOUD_RUN_MEMORY || DEFAULTS.CLOUD_RUN_MEMORY,
  cpu: process.env.CLOUD_RUN_CPU || DEFAULTS.CLOUD_RUN_CPU,
  minInstances:
    process.env.CLOUD_RUN_MIN_INSTANCES || DEFAULTS.CLOUD_RUN_MIN_INSTANCES,
  maxInstances:
    process.env.CLOUD_RUN_MAX_INSTANCES || DEFAULTS.CLOUD_RUN_MAX_INSTANCES,
};

console.log(`✅ Project: ${config.project}`);
console.log(`✅ Service: ${config.service}`);
console.log(`✅ Region: ${config.region}`);

// Check auth
console.log("\n🔐 Checking gcloud auth...");
try {
  await $`gcloud auth print-access-token`.quiet();
  console.log("✅ Authenticated");
} catch {
  console.log("❌ Run: gcloud auth login");
  process.exit(1);
}

// Check Dockerfile
if (!(await exists("Dockerfile"))) {
  console.log("❌ Dockerfile not found");
  process.exit(1);
}

// Run tests
console.log("\n🧪 Running tests...");
try {
  await $`bun test`.quiet();
  console.log("✅ Tests passed");
} catch {
  console.log("⚠️ Tests failed");
  process.stdout.write("Continue anyway? (y/N): ");
  for await (const line of console) {
    if (line.toLowerCase() !== "y") process.exit(0);
    break;
  }
}

// Confirm
console.log("\n" + "═".repeat(50));
console.log("📋 STAGING DEPLOYMENT");
console.log("═".repeat(50));
console.log(`Project:   ${config.project}`);
console.log(`Service:   ${config.service}`);
console.log(`Region:    ${config.region}`);
console.log("═".repeat(50));

process.stdout.write("\n🔔 Deploy to STAGING? (y/N): ");
for await (const line of console) {
  if (line.toLowerCase() !== "y") {
    console.log("Cancelled.");
    process.exit(0);
  }
  break;
}

// Deploy
console.log("\n🚀 Deploying...");
await $`gcloud run deploy ${config.service} \
  --source . \
  --project ${config.project} \
  --region ${config.region} \
  --memory ${config.memory} \
  --cpu ${config.cpu} \
  --min-instances ${config.minInstances} \
  --max-instances ${config.maxInstances} \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars ENVIRONMENT=staging`;

const url =
  await $`gcloud run services describe ${config.service} --project ${config.project} --region ${config.region} --format "value(status.url)"`.text();

console.log("\n🎉 STAGING DEPLOYMENT COMPLETE");
console.log(`URL: ${url.trim()}`);

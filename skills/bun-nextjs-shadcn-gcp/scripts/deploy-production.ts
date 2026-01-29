#!/usr/bin/env bun
/**
 * GCP Cloud Run PRODUCTION Deployment
 * ⚠️ Requires typing "yes" to confirm
 * Usage: bun run scripts/deploy-production.ts
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

const REQUIRED = ["GCP_PROJECT_PRODUCTION", "GCP_REGION", "SERVICE_NAME"];
const DEFAULTS = {
  CLOUD_RUN_MEMORY: "1Gi",
  CLOUD_RUN_CPU: "2",
  CLOUD_RUN_MIN_INSTANCES: "1",
  CLOUD_RUN_MAX_INSTANCES: "100",
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
  project: process.env.GCP_PROJECT_PRODUCTION!,
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

// Run tests (required for production)
console.log("\n🧪 Running tests...");
try {
  await $`bun test`;
  console.log("✅ Tests passed");
} catch {
  console.log("❌ Tests failed! Fix before deploying to production.");
  process.exit(1);
}

// Show checklist
console.log("\n⚠️ PRODUCTION CHECKLIST");
console.log("═".repeat(50));
console.log("[ ] Tested in staging?");
console.log("[ ] No console errors?");
console.log("[ ] Performance acceptable?");
console.log("[ ] Rollback plan ready?");
console.log("═".repeat(50));

// Show deployment plan
console.log("\n" + "═".repeat(50));
console.log("⚠️ PRODUCTION DEPLOYMENT");
console.log("═".repeat(50));
console.log(`Project:   ${config.project}`);
console.log(`Service:   ${config.service}`);
console.log(`Region:    ${config.region}`);
console.log(`Memory:    ${config.memory}`);
console.log(`CPU:       ${config.cpu}`);
console.log(`Instances: ${config.minInstances} - ${config.maxInstances}`);
console.log("═".repeat(50));

// Require explicit "yes"
console.log("\n⚠️ WARNING: This affects live users!");
process.stdout.write("Type 'yes' to confirm: ");
for await (const line of console) {
  if (line.toLowerCase() !== "yes") {
    console.log("Cancelled. (Must type 'yes')");
    process.exit(0);
  }
  break;
}

// Deploy
console.log("\n🚀 Deploying to PRODUCTION...");
await $`gcloud run deploy ${config.service} \
  --source . \
  --project ${config.project} \
  --region ${config.region} \
  --memory ${config.memory} \
  --cpu ${config.cpu} \
  --min-instances ${config.minInstances} \
  --max-instances ${config.maxInstances} \
  --platform managed \
  --no-allow-unauthenticated \
  --set-env-vars ENVIRONMENT=production`;

// Get URL and revisions
const url =
  await $`gcloud run services describe ${config.service} --project ${config.project} --region ${config.region} --format "value(status.url)"`.text();

console.log("\n📋 Recent revisions (for rollback):");
await $`gcloud run revisions list --service ${config.service} --project ${config.project} --region ${config.region} --limit 3`;

console.log("\n🎉 PRODUCTION DEPLOYMENT COMPLETE");
console.log(`URL: ${url.trim()}`);
console.log("\n⚠️ Monitor for issues! Rollback command:");
console.log(
  `gcloud run services update-traffic ${config.service} --region ${config.region} --to-revisions REVISION=100`,
);

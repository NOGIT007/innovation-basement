---
name: bun-nextjs-shadcn-gcp
version: 1.1.0
description: Complete development workflow for Bun 1.3+ Next.js + Shadcn/UI applications with GCP Cloud Run deployment. Includes S3, Redis, SQL APIs. All scripts in TypeScript.
triggers:
  - bun project
  - next.js app
  - nextjs project
  - shadcn setup
  - create react app
  - new bun project
  - deploy bun app
  - bun nextjs
  - bun react
  - full stack bun
  - deploy to cloud run
  - gcp deployment
  - bun s3
  - bun redis
  - bun sql
  - html imports
globs:
  - "**/next.config.{ts,js,mjs}"
  - "**/bun.lock"
  - "**/tailwind.config.{ts,js}"
context:
  - scripts/*.ts
  - assets/*
  - references/*.md
---

# Bun + Next.js + Shadcn/UI Development & Deployment

Complete workflow for building and deploying modern web applications using Bun runtime, Next.js framework, and Shadcn/UI components to GCP Cloud Run.

**All scripts are written in TypeScript and run with Bun** - no Python required!

## Workflow Decision Tree

```
What do you want to do?
│
├─▶ "Create new project" → See: 1. Project Initialization
│
├─▶ "Add components" → See: 2. Adding Shadcn Components
│
├─▶ "Run locally" → See: 3. Local Development
│
├─▶ "Run tests" → See: 4. Testing
│
├─▶ "Deploy to staging" → See: 5. Deploy to Staging
│
└─▶ "Deploy to production" → See: 6. Deploy to Production
```

---

## 1. Project Initialization

### Quick Start (New Project)

```bash
# Create new Next.js project with Bun
bun create next-app my-app --typescript --tailwind --eslint --app --src-dir

cd my-app

# Initialize Shadcn/UI
bunx shadcn@latest init

# Add common components
bunx shadcn@latest add button card input form dialog toast
```

### Using the Init Script

```bash
# Initialize with default components
bun run scripts/init-project.ts --name my-app

# With specific components
bun run scripts/init-project.ts --name my-app --components "button,card,input,form,table,dialog"

# Show help
bun run scripts/init-project.ts --help
```

### Project Structure After Init

```
my-app/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   └── ui/          # Shadcn components
│   └── lib/
│       └── utils.ts     # cn() helper
├── public/
├── __tests__/           # Test files
├── Dockerfile           # For Cloud Run
├── docker-compose.yml   # Local Docker dev
├── .env.example
├── .env.local           # Local env vars
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── bun.lock
└── package.json
```

### Required next.config.ts

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone", // Required for Docker/Cloud Run
};

export default nextConfig;
```

---

## 2. Adding Shadcn Components

### Available Components

```bash
# Add specific components
bunx shadcn@latest add button card input form dialog toast table
bunx shadcn@latest add accordion alert avatar badge breadcrumb calendar
bunx shadcn@latest add checkbox collapsible command context-menu date-picker
bunx shadcn@latest add drawer dropdown-menu hover-card label menubar
bunx shadcn@latest add navigation-menu pagination popover progress radio-group
bunx shadcn@latest add scroll-area select separator sheet skeleton slider
bunx shadcn@latest add switch tabs textarea toggle tooltip
```

### Component Usage Example

```tsx
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function MyComponent() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Welcome</CardTitle>
      </CardHeader>
      <CardContent>
        <Button variant="default">Click me</Button>
      </CardContent>
    </Card>
  );
}
```

---

## 3. Local Development

### Run Development Server

```bash
bun run dev
```

### Run with Docker (mirrors production)

```bash
docker-compose up --build
```

---

## 4. Testing

```bash
# Run all tests
bun test

# With coverage
bun run scripts/run-tests.ts --coverage

# Watch mode
bun run scripts/run-tests.ts --watch
```

---

## 5. Deploy to Staging

### Prerequisites

```bash
export GCP_PROJECT_STAGING=your-staging-project
export GCP_REGION=europe-west1
export SERVICE_NAME=my-app
```

### Deploy

```bash
bun run scripts/deploy-staging.ts
```

---

## 6. Deploy to Production

### Prerequisites

```bash
export GCP_PROJECT_PRODUCTION=your-production-project
export GCP_REGION=europe-west1
export SERVICE_NAME=my-app
```

### Deploy (requires typing "yes")

```bash
bun run scripts/deploy-production.ts
```

---

## Resources

### Scripts (TypeScript + Bun)

| Script                 | Command                                | Description            |
| ---------------------- | -------------------------------------- | ---------------------- |
| `init-project.ts`      | `bun run scripts/init-project.ts`      | Initialize new project |
| `run-tests.ts`         | `bun run scripts/run-tests.ts`         | Run tests with options |
| `deploy-staging.ts`    | `bun run scripts/deploy-staging.ts`    | Deploy to staging      |
| `deploy-production.ts` | `bun run scripts/deploy-production.ts` | Deploy to production   |

### Assets

- `assets/Dockerfile` - Production-ready Dockerfile for Bun + Next.js
- `assets/docker-compose.yml` - Local development with Docker
- `assets/.env.example` - Environment variable template

### References

- `references/gcp_safety.md` - **⚠️ GCP Safety Policy: NO deletions without approval**
- `references/bun_1.3_features.md` - Bun 1.3 features: S3, Redis, SQL, HTML imports
- `references/gcp_setup.md` - GCP Cloud Run setup guide
- `references/shadcn_components.md` - Shadcn component reference

---

## ⚠️ Safety Policy

This skill will **NEVER** delete anything on GCP. All destructive operations are blocked:

- ❌ `gcloud run services delete` - BLOCKED
- ❌ `gcloud run revisions delete` - BLOCKED
- ❌ `gcloud storage rm` - BLOCKED
- ❌ `gcloud projects delete` - BLOCKED

**Rollback is safe** (traffic routing, no deletion):

```bash
gcloud run services update-traffic SERVICE --to-revisions REVISION=100
```

See `references/gcp_safety.md` for full policy.

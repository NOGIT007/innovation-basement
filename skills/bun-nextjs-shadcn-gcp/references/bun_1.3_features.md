# Bun 1.3 Features Reference

New features in Bun 1.3+ that enhance full-stack development.

## S3 Client (Built-in)

Zero-dependency S3 storage support:

```typescript
// Using environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
const file = Bun.s3.file("my-bucket/image.png");

// Read file
const data = await file.text();
const bytes = await file.arrayBuffer();

// Write file
await Bun.s3.write("my-bucket/data.json", JSON.stringify({ hello: "world" }));

// With explicit credentials
const s3 = new Bun.S3Client({
  accessKeyId: "...",
  secretAccessKey: "...",
  region: "eu-west-1",
  endpoint: "https://s3.eu-west-1.amazonaws.com", // or compatible service
});

// Multipart upload for large files
await s3.write("bucket/large-file.zip", largeBuffer, {
  multipart: true,
  partSize: 5 * 1024 * 1024, // 5MB chunks
});

// List objects
const objects = await s3.list("my-bucket", { prefix: "uploads/" });
```

## HTML Imports (Zero-Config Frontend)

Replace your entire frontend toolchain with a single import:

```typescript
// server.ts
Bun.serve({
  routes: {
    "/": "./index.html", // Serves HTML with auto-bundled JS/CSS
    "/app": "./src/app.html", // React + Tailwind just work
    "/api/users": handleUsers, // API routes alongside
  },
});
```

```html
<!-- index.html - Bun auto-bundles and minifies -->
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="./styles.css" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="./app.tsx"></script>
  </body>
</html>
```

## Built-in Redis Client

7.9x faster than ioredis:

```typescript
import { Redis } from "bun";

const redis = new Redis(); // localhost:6379
// or
const redis = new Redis("redis://user:pass@host:6379");

// Standard operations
await redis.set("key", "value");
const value = await redis.get("key");

// With expiry
await redis.set("session", data, { ex: 3600 }); // 1 hour

// Lists, hashes, sets
await redis.lpush("queue", "item1", "item2");
await redis.hset("user:1", { name: "John", age: "30" });
```

## Unified SQL API

One API for PostgreSQL, MySQL, and SQLite:

```typescript
import { SQL } from "bun";

// PostgreSQL
const pg = new SQL("postgres://user:pass@localhost/db");

// MySQL
const mysql = new SQL("mysql://user:pass@localhost/db");

// SQLite
const sqlite = new SQL("sqlite:./data.db");

// Same API for all
const users = await pg.query`SELECT * FROM users WHERE id = ${userId}`;
```

## Full-Stack Bundling

Bundle frontend and backend together:

```typescript
// build.ts
await Bun.build({
  entrypoints: [
    "./src/server.ts", // Backend
    "./src/client.tsx", // Frontend
  ],
  outdir: "./dist",
  target: "bun", // For server
  // Automatically handles client bundles
});
```

## Single-File Executables

Compile your full-stack app to one binary:

```bash
bun build --compile --target=bun ./server.ts --outfile=myapp
```

## Environment Variables

```bash
# S3
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=eu-west-1

# Redis
REDIS_URL=redis://localhost:6379

# Database
DATABASE_URL=postgres://user:pass@host:5432/db
```

## Performance Tips

1. **Use Bun.file()** for local files - lazy loading, no immediate I/O
2. **Use Bun.s3.file()** for S3 - same lazy pattern
3. **Use multipart uploads** for files > 5MB
4. **Use built-in Redis** instead of ioredis for 7.9x speed
5. **Use Bun.SQL** instead of pg/mysql2 for unified API

## Sources

- [Bun 1.3 Blog](https://bun.com/blog/bun-v1.3)
- [S3 Documentation](https://bun.com/docs/runtime/s3)

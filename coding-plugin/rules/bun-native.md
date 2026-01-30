# Bun Native APIs

> Bun 1.3+ native APIs - prefer over npm packages

## Bun.sql (PostgreSQL)

| Instead of               | Use                             |
| ------------------------ | ------------------------------- |
| `pg` / `postgres`        | `import { sql } from "bun:sql"` |
| Connection pool setup    | Built-in connection pooling     |
| `client.query(text, [])` | `sql\`SELECT \* FROM t\``       |

```typescript
import { sql } from "bun:sql";

// Parameterized (safe)
const users = await sql`SELECT * FROM users WHERE id = ${userId}`;

// Transactions
await sql.begin(async (tx) => {
  await tx`INSERT INTO logs (msg) VALUES (${"started"})`;
  await tx`UPDATE users SET active = true WHERE id = ${id}`;
});
```

**Rule:** Use tagged template literals for automatic parameterization.

## Bun.redis

| Instead of | Use                                 |
| ---------- | ----------------------------------- |
| `ioredis`  | `import { redis } from "bun:redis"` |
| `redis`    | Built-in Redis client               |

```typescript
import { redis } from "bun:redis";

await redis.set("key", "value");
const val = await redis.get("key");
await redis.del("key");
```

## Bun.S3

| Instead of           | Use                           |
| -------------------- | ----------------------------- |
| `@aws-sdk/client-s3` | `import { S3 } from "bun:s3"` |
| `aws-sdk`            | Built-in S3 client            |

```typescript
import { S3 } from "bun:s3";

const s3 = new S3({
  bucket: "my-bucket",
  region: "eu-west-1",
});

// Upload
await s3.put("file.txt", "content");

// Download
const content = await s3.get("file.txt");

// Delete
await s3.delete("file.txt");
```

## Bun.serve()

| Instead of  | Use                  |
| ----------- | -------------------- |
| `express`   | `Bun.serve()`        |
| `fastify`   | Built-in HTTP server |
| `node:http` | Native Bun server    |

```typescript
Bun.serve({
  port: 3000,
  fetch(req) {
    const url = new URL(req.url);
    if (url.pathname === "/health") {
      return new Response("ok");
    }
    return new Response("Not found", { status: 404 });
  },
});
```

## Migration Checklist

When setting up new Bun projects:

- [ ] Use `bun:sql` instead of `pg`/`postgres` for PostgreSQL
- [ ] Use `bun:redis` instead of `ioredis`/`redis`
- [ ] Use `bun:s3` instead of AWS SDK for S3 operations
- [ ] Use `Bun.serve()` for simple HTTP servers
- [ ] Keep Next.js for full-stack apps (don't replace with Bun.serve)

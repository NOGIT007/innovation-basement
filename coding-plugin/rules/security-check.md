# Security Check Rules

> Add to your project's `CLAUDE.md` to enable: `@coding-plugin/rules/security-check.md`

## SQL Injection

| Bad | Good |
|-----|------|
| `query = f"SELECT * FROM users WHERE id = {user_id}"` | `cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))` |
| `db.query(\`SELECT * FROM users WHERE name = '${name}'\`)` | `db.query("SELECT * FROM users WHERE name = $1", [name])` |

**Rule:** Never interpolate user input into SQL strings. Use parameterized queries.

## Command Injection

| Bad | Good |
|-----|------|
| `os.system(f"rm {filename}")` | `subprocess.run(["rm", filename])` |
| `exec(\`ls ${dir}\`)` | `execFile("ls", [dir])` |

**Rule:** Never pass user input to shell strings. Use array-based APIs.

## Secrets Management

| Bad | Good |
|-----|------|
| `API_KEY = "sk-1234..."` | `API_KEY = os.environ["API_KEY"]` |
| `const secret = "hardcoded"` | `const secret = process.env.SECRET` |

**Rule:** Never hardcode secrets. Use environment variables or secret managers.

## XSS Prevention

| Bad | Good |
|-----|------|
| `element.innerHTML = userInput` | `element.textContent = userInput` |
| `dangerouslySetInnerHTML={{__html: data}}` | Use sanitization library or avoid |

**Rule:** Never insert untrusted data as HTML. Use text content or sanitize.

## Boundary Validation

Validate at trust boundaries:
- API endpoints (validate all input)
- File operations (validate paths, prevent traversal)
- External data (validate before use)

```typescript
// Path traversal prevention
if (filename.includes("..") || filename.includes("/")) {
  throw new Error("Invalid filename");
}
```

## Flags

- String interpolation in SQL/shell commands
- Hardcoded API keys, passwords, or tokens
- innerHTML with user-controlled data
- Missing input validation at API boundaries

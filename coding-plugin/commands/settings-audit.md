---
allowed-tools: Read, Write, Bash(git:*)
description: Generate .claude/settings.json permissions from project analysis
---

# Settings Audit

Analyze project and generate appropriate `.claude/settings.json` permissions.

## Step 1: Analyze Project

Detect project type and required tools:

```bash
# Check for package managers and tools
ls -la package.json bun.lock yarn.lock pnpm-lock.yaml Cargo.toml pyproject.toml go.mod 2>/dev/null

# Check for Docker
ls -la Dockerfile docker-compose.yml 2>/dev/null

# Check for cloud configs
ls -la .gcloudignore cloudbuild.yaml fly.toml vercel.json 2>/dev/null
```

## Step 2: Read Existing Settings

```bash
if [ -f ".claude/settings.json" ]; then
  cat .claude/settings.json
else
  echo "No existing settings found"
fi
```

## Step 3: Generate Permissions

Based on project analysis, recommend permissions:

### Base Permissions (All Projects)

```json
{
  "permissions": {
    "allow": ["Bash(git:*)", "Read", "Write", "Edit"]
  }
}
```

### Bun/Node Projects

Add if `package.json` or `bun.lock` exists:

```json
{
  "permissions": {
    "allow": ["Bash(bun:*)", "Bash(bunx:*)", "Bash(npm:*)", "Bash(npx:*)"]
  }
}
```

### Docker Projects

Add if `Dockerfile` exists:

```json
{
  "permissions": {
    "allow": ["Bash(docker:*)", "Bash(docker-compose:*)"]
  }
}
```

### GCP Projects

Add if `.gcloudignore` or `cloudbuild.yaml` exists:

```json
{
  "permissions": {
    "allow": ["Bash(gcloud:*)", "Bash(gsutil:*)"]
  }
}
```

### Python Projects

Add if `pyproject.toml` or `requirements.txt` exists:

```json
{
  "permissions": {
    "allow": ["Bash(uv:*)", "Bash(pip:*)", "Bash(python:*)", "Bash(pytest:*)"]
  }
}
```

## Step 4: Check for Sensitive Patterns

Flag if found:

- `.env` files with secrets
- `credentials.json` or service account keys
- API keys in source files

Recommend adding to `.gitignore` and `.claudeignore`.

## Step 5: Generate Settings File

Write `.claude/settings.json` with:

1. Detected permissions
2. Plans directory (if not set)
3. Environment variables for task management

Example output:

```json
{
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Bash(bun:*)",
      "Bash(bunx:*)",
      "Bash(docker:*)",
      "Bash(gcloud:*)"
    ],
    "deny": []
  },
  "plansDirectory": "plans",
  "env": {
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "70"
  }
}
```

## Output

Report:

- 📁 Project type detected
- ✅ Permissions recommended
- ⚠️ Security warnings (if any)
- 📝 Settings file written/updated

## Rules

- Start with minimal permissions
- Add only what's detected as needed
- Flag any security concerns
- Don't overwrite existing custom settings without confirmation

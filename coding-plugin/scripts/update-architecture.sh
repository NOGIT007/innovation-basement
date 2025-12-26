#!/bin/bash
ARCH="rules/architecture.md"
[ -f "$ARCH" ] && [ $(($(date +%s) - $(stat -f %m "$ARCH"))) -lt 3600 ] && exit 0
echo "🏗️ Updating architecture..."
claude -p "/code:update-architecture" --allowed-tools "Read,Glob,Write,Bash(ls:*)" &

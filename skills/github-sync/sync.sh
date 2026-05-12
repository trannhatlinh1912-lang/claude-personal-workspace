#!/usr/bin/env bash
# sync.sh — Push ~/.claude/personal-workspace lên GitHub
# Usage: bash sync.sh ["optional commit message"]

set -euo pipefail

WORKSPACE="$HOME/personal-workspace"
COMMIT_MSG="${1:-sync: $(date '+%Y-%m-%d %H:%M') — outputs and logs}"

cd "$WORKSPACE"

if git diff --quiet HEAD 2>/dev/null && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    echo "Nothing to sync — workspace is clean."
    exit 0
fi

git add outputs/ logs/ skills/ hooks/ README.md .gitignore 2>/dev/null || true

STAGED=$(git diff --cached --name-only)
if [ -z "$STAGED" ]; then
    echo "Nothing staged to commit."
    exit 0
fi

echo "=== Files to commit ==="
echo "$STAGED"
echo "======================="

git commit -m "$COMMIT_MSG"
git push origin main

echo ""
echo "Synced to GitHub."
echo "Remote: $(git remote get-url origin)"
echo "Commit: $(git log --oneline -1)"

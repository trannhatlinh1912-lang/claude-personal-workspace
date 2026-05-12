#!/usr/bin/env bash
# Stop hook: auto-log mỗi response vào ~/.claude/personal-workspace/logs/YYYY-MM-DD.md
# Triggered by Claude Code Stop event — luôn exit 0, không bao giờ block Claude

set -euo pipefail

WORKSPACE="$HOME/personal-workspace"
LOG_DIR="$WORKSPACE/logs"

HOOK_INPUT=$(cat)

SESSION_ID=$(echo "$HOOK_INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")
TRANSCRIPT_PATH=$(echo "$HOOK_INPUT" | jq -r '.transcript_path // ""' 2>/dev/null || echo "")
WORK_DIR=$(echo "$HOOK_INPUT" | jq -r '.cwd // ""' 2>/dev/null || echo "")
[ -z "$WORK_DIR" ] && WORK_DIR=$(pwd)

TODAY=$(date +%Y-%m-%d)
NOW=$(date +%H:%M)
LOG_FILE="$LOG_DIR/$TODAY.md"

mkdir -p "$LOG_DIR"

if [ ! -f "$LOG_FILE" ]; then
    printf "# Log ngày %s\n\n" "$TODAY" > "$LOG_FILE"
fi

LAST_MSG=""
TOTAL_TURNS=0
if [ -n "$TRANSCRIPT_PATH" ] && [ -f "$TRANSCRIPT_PATH" ]; then
    TOTAL_TURNS=$(grep -c '"role":"user"' "$TRANSCRIPT_PATH" 2>/dev/null || echo 0)
    LAST_MSG=$(grep '"role":"assistant"' "$TRANSCRIPT_PATH" 2>/dev/null | tail -n 20 | \
        jq -rs '[.[].message.content[]? | select(.type == "text") | .text] | last // ""' \
        2>/dev/null | head -c 300 | tr '\n' ' ' || echo "")
fi

cat >> "$LOG_FILE" << ENTRY
## ${NOW} — session ${SESSION_ID:0:8}

**Thư mục:** $WORK_DIR
**Turns:** $TOTAL_TURNS
**Session:** $SESSION_ID

> ${LAST_MSG:-(no assistant text captured)}

---

ENTRY

exit 0

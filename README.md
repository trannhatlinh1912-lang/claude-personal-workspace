# Claude Personal Workspace

Không gian làm việc cá nhân với Claude Code — bao gồm custom skills, output files, và session logs.

## Cấu trúc

```
personal-workspace/
├── skills/
│   ├── research-reviews/   # /research-reviews — fetch Google Maps reviews qua SerpAPI
│   ├── github-sync/        # /github-sync — push workspace lên GitHub
│   └── log-session/        # /log-session — ghi chép thủ công session
├── outputs/
│   └── research-reviews/   # Báo cáo từ mỗi lần chạy /research-reviews
├── logs/                   # YYYY-MM-DD.md — auto-log từ Stop hook + manual /log-session
└── hooks/
    └── stop-hook.sh        # Claude Code Stop hook — auto-log mỗi response
```

## Setup

### 1. Skills (symlinks)
Skills được đọc từ `~/.claude/skills/`. Tạo symlinks:
```bash
ln -s ~/personal-workspace/skills/research-reviews ~/.claude/skills/research-reviews
ln -s ~/personal-workspace/skills/github-sync ~/.claude/skills/github-sync
ln -s ~/personal-workspace/skills/log-session ~/.claude/skills/log-session
```

### 2. SerpAPI key
Tạo file `~/.claude/serpapi.env` (nằm ngoài repo này):
```
SERPAPI_KEY=your_actual_key_here
```
```bash
chmod 600 ~/.claude/serpapi.env
```

### 3. Stop Hook
Thêm vào `~/.claude/settings.json`:
```json
"hooks": {
  "Stop": [{
    "hooks": [{
      "type": "command",
      "command": "bash /Users/trannhatlinh/personal-workspace/hooks/stop-hook.sh",
      "timeout": 10
    }]
  }]
}
```

### 4. GitHub remote
```bash
gh repo create claude-personal-workspace --private --source=. --remote=origin --push
```

## Skills

| Skill | Mô tả | External Platform |
|-------|-------|-------------------|
| `/research-reviews <url>` | Fetch và phân tích Google Maps reviews | SerpAPI |
| `/github-sync` | Push outputs và logs lên GitHub | GitHub (git CLI) |
| `/log-session` | Ghi chép tóm tắt session thủ công | — |

## Logs

- **Auto-log** (Stop hook): Sau mỗi response của Claude, metadata + snippet được append vào `logs/YYYY-MM-DD.md`
- **Manual log** (`/log-session`): Tóm tắt có cấu trúc do Claude tạo từ conversation

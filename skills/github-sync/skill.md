---
name: github-sync
description: Push tất cả outputs và logs từ ~/personal-workspace lên GitHub repo. Dùng khi muốn backup hoặc chia sẻ kết quả research và session logs.
---

# /github-sync — Push Workspace to GitHub

## Cách dùng
```
/github-sync
/github-sync "custom commit message"
```

## Quy trình thực hiện

### Bước 1 — Kiểm tra trạng thái
```bash
git -C ~/personal-workspace status --short
```
Nếu output rỗng: thông báo "Nothing to sync" và dừng.

### Bước 2 — Chạy sync script
```bash
bash ~/personal-workspace/skills/github-sync/sync.sh "<commit_message>"
```

Nếu user không cung cấp commit message, script tự tạo: `sync: YYYY-MM-DD HH:MM — outputs and logs`

### Bước 3 — Báo cáo kết quả
In ra: danh sách files đã commit, commit hash, link GitHub repo.

## Ghi chú
- Remote `origin` phải được setup trước (xem README.md)
- Credentials được xử lý qua macOS Keychain — không cần nhập password mỗi lần
- Chỉ sync: `outputs/`, `logs/`, `skills/`, `hooks/` — không sync `~/.claude/serpapi.env`

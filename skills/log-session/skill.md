---
name: log-session
description: Tạo bản tóm tắt có cấu trúc cho phiên làm việc hiện tại và append vào ~/personal-workspace/logs/YYYY-MM-DD.md. Dùng khi muốn ghi lại thủ công những gì đã làm trong session.
---

# /log-session — Manual Session Logger

## Cách dùng
```
/log-session
/log-session "ghi chú thêm"
```

## Quy trình thực hiện

### Bước 1 — Xác định file log
- Ngày: `date +%Y-%m-%d`
- File: `~/personal-workspace/logs/<YYYY-MM-DD>.md`

### Bước 2 — Tóm tắt session hiện tại
Dựa trên conversation hiện tại, tạo summary với format:

```markdown
## Session: HH:MM — <chủ đề ngắn>

**Thời gian:** YYYY-MM-DD HH:MM
**Thư mục làm việc:** <cwd>

### Đã làm
- <bullet điểm 1>
- <bullet điểm 2>

### Kết quả / Output
- <file tạo ra, quyết định, insight quan trọng>

### Cần làm tiếp
- <TODO nếu có>

---
```

### Bước 3 — Ghi vào file
- Nếu file chưa tồn tại: tạo với header `# Log ngày YYYY-MM-DD`
- Append summary vào cuối file

### Bước 4 — Xác nhận
In ra đường dẫn file log và preview 5 dòng cuối vừa thêm.

## Ghi chú
- Auto-log (Stop hook) ghi metadata sau mỗi response; skill này ghi summary có ngữ nghĩa
- Dùng `/github-sync` sau để push log lên GitHub

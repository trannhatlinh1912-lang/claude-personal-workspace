---
name: research-reviews
description: Fetch và phân tích Google Maps reviews của đối thủ cạnh tranh qua SerpAPI. Nhập Google Maps URL để lấy toàn bộ reviews và tạo báo cáo competitive intelligence dạng Markdown.
---

# /research-reviews — Google Maps Review Researcher

## Cách dùng
```
/research-reviews <Google Maps URL>
```

Ví dụ:
```
/research-reviews https://www.google.com/maps/place/Nha-Hang-XYZ/...
/research-reviews https://maps.app.goo.gl/abc123
```

## Quy trình thực hiện

### Bước 1 — Kiểm tra API key
Đọc file `~/.claude/serpapi.env`. Nếu không tồn tại hoặc không có `SERPAPI_KEY`, dừng lại và hướng dẫn:
```
Tạo file ~/.claude/serpapi.env với nội dung:
SERPAPI_KEY=your_actual_key_here
```

### Bước 2 — Chạy fetch script
```bash
python3 ~/personal-workspace/skills/research-reviews/fetch-reviews.py "<URL>"
```

Script in JSON ra stdout, progress ra stderr. Lưu JSON output vào:
```
~/personal-workspace/outputs/research-reviews/<YYYY-MM-DD>_<place_slug>.json
```

### Bước 3 — Phân tích và tạo báo cáo
Đọc JSON vừa lưu và tạo báo cáo theo cấu trúc trong `report-template.md`. Lưu báo cáo vào:
```
~/personal-workspace/outputs/research-reviews/<YYYY-MM-DD>_<place_slug>_report.md
```

### Bước 4 — Tổng kết
In ra:
- Tên địa điểm, rating, tổng reviews
- Đường dẫn file báo cáo
- 3 insight quan trọng nhất

## Ghi chú
- Nếu URL là short link (goo.gl), script tự động expand
- Mỗi lần chạy tạo file mới với timestamp — không ghi đè
- API tính phí theo số reviews; script fetch tất cả trang

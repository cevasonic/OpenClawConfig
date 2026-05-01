# Hướng dẫn cấu hình và quản lý Models trong OpenClaw

Tài liệu này tổng hợp các bước kỹ thuật để thêm mới hoặc cập nhật mô hình AI (Models) cho OpenClaw, đặc biệt là thông qua nhà cung cấp OpenRouter. Đây là cơ sở để bạn có thể viết Skill tự động hóa sau này.

## 1. Các tệp tin cấu hình quan trọng
Trên VPS của bạn, OpenClaw sử dụng 3 tệp tin cấu hình cần được đồng bộ hóa:
- **`/opt/openclaw/.openclaw/openclaw.json`**: Tệp tin chính mà dịch vụ Gateway (chạy qua systemd) sử dụng.
- **`/root/.openclaw/openclaw.json`**: Tệp tin dùng cho các lệnh CLI (như `openclaw models list`).
- **`/opt/openclaw/config/openclaw.json`**: Tệp tin dự phòng.

> [!IMPORTANT]
> Luôn cập nhật đồng thời cả 3 tệp để đảm bảo tính nhất quán giữa dịch vụ đang chạy và các lệnh kiểm tra CLI.

---

## 2. Cấu trúc JSON cho Models

### a. Định nghĩa Provider (Nhà cung cấp)
Nằm trong mục `"models": { "providers": { ... } }`.
Nếu các mô hình dùng chung một API Key, bạn có thể gộp vào 1 provider. Nếu khác Key, hãy tách thành các provider riêng (ví dụ: `openrouter-step`, `openrouter-gemma`).

```json
"openrouter-step": {
  "baseUrl": "https://openrouter.ai/api/v1",
  "api": "openai-completions",
  "apiKey": "YOUR_API_KEY",
  "models": [
    {
      "id": "stepfun/step-3.5-flash",
      "name": "Step 3.5 Flash"
    }
  ]
}
```

### b. Đăng ký với Agent
Để mô hình xuất hiện trong danh sách lệnh `/models` trên Telegram, bạn phải đăng ký nó trong mục `"agents": { "defaults": { "models": { ... } } }`.

```json
"models": {
  "openrouter-step/stepfun/step-3.5-flash": {},
  "openrouter-gemma/google/gemma-4-31b-it": {}
}
```

### c. Cài đặt mô hình mặc định
```json
"model": {
  "primary": "openrouter-step/stepfun/step-3.5-flash"
}
```

---

## 3. Quy trình thực hiện (Workflow)

### Bước 1: Lấy và chuẩn bị nội dung JSON mới
- **Quan trọng:** Luôn fetch tệp tin `/opt/openclaw/.openclaw/openclaw.json` mới nhất từ VPS trước khi sửa đổi để tránh ghi đè các thay đổi gần đây.
- Đọc tệp tin hiện tại, chèn thêm Provider mới hoặc cập nhật API Key.
- Cập nhật danh sách Agent models trong `"agents": { "defaults": { "models": { ... } } }`.

### Bước 2: Ghi tệp tin lên VPS
Sử dụng phương pháp `base64` để tránh lỗi ký tự đặc biệt và có thể cập nhật nhiều tệp cùng lúc:
1. Encode nội dung JSON thành chuỗi base64 (ví dụ: `base64 -i config.json`).
2. Chạy lệnh sau để cập nhật cả 3 vị trí:
   `echo <chuỗi_base64> | base64 -d | tee /opt/openclaw/.openclaw/openclaw.json /root/.openclaw/openclaw.json /opt/openclaw/config/openclaw.json > /dev/null`

### Bước 3: Xác thực và Khởi động lại
1. **Kiểm tra cú pháp:** `HOME=/opt/openclaw openclaw config validate`
2. **Khởi động lại dịch vụ:** `systemctl restart openclaw-gateway.service`
3. **Kiểm tra trạng thái:** `journalctl -u openclaw-gateway.service -n 20 --no-pager`

---

## 4. Các lệnh CLI hữu ích
- **Liệt kê mô hình đang sẵn sàng:** `HOME=/opt/openclaw openclaw models list`
- **Kiểm tra cổng đang bị chiếm (nếu lỗi EADDRINUSE):** `ss -lptn 'sport = :18789'`
- **Tắt tiến trình OpenClaw bị treo:** `kill -9 <PID>`

---

## 5. Ý tưởng cho Skill trên Telegram
Để có thể thêm model từ Telegram, Skill của bạn cần thực hiện các thao tác:
1. Nhận thông tin: `Provider Name`, `API Key`, `Model ID`.
2. Dùng một script (Python hoặc Bash) để thực hiện các bước trong **Quy trình thực hiện** ở trên.
3. Phản hồi kết quả: Gửi lại danh sách mô hình sau khi cập nhật bằng lệnh `openclaw models list`.

---
---
*Tài liệu này được cập nhật vào ngày 30/04/2026 bởi Antigravity sau khi triển khai thành công model DeepSeek V4 Flash.*

## 6. Bài học kinh nghiệm (Lessons Learned)
- **Tên dịch vụ chính xác:** Dịch vụ chính chạy OpenClaw là `openclaw-gateway.service`, không phải là `openclaw`.
- **Đồng bộ hóa 3 vị trí:** Việc sử dụng lệnh `tee` giúp cập nhật đồng thời cả 3 tệp cấu hình, đảm bảo CLI và Gateway luôn dùng chung một bản cấu hình.
- **Quy trình an toàn:** Luôn lấy cấu hình mới nhất từ VPS (`cat ...`) trước khi thực hiện bất kỳ chỉnh sửa nào để không làm mất các thay đổi được thực hiện trực tiếp trên server hoặc bởi các công cụ khác.

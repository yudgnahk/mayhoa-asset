# Giới hạn tự động hoá Chrome — đọc trước khi định cho agent gen ảnh

Kiểm chứng 2026-09-12 từ `claude.com/claude-in-chrome` và support article
"Getting started with Claude in Chrome". Ghi ở đây vì `.ai-bridge/` bị `.gitignore`
nên ghi chú trong đó không theo repo đi đâu được.

## Agent terminal KHÔNG tự đi được flow `.ai-bridge`

Một Claude Code agent chạy ở terminal **không nối được** vào Chrome đã đăng nhập của
Kelvin. "Claude in Chrome" là extension, chạy AI riêng trong side panel và dùng quyền
`debugger` của chính nó — quyền đó **không lộ ra thành cổng debug hay API** cho tiến
trình khác gắn vào. Chrome không mở cổng 9222 không phải vì thiếu bật; extension này
vốn không dùng cổng đó.

Cầu nối `nativeMessaging` giữa extension và Claude Code được docs ghi rõ là **chưa
bật** ("once we enable that capability"). Khi nào Anthropic bật thì kiểm lại mục này.

Tool browser của Paseo mở một Chrome **mới, chưa đăng nhập** → vào chatgpt.com bị đá
về màn hình login. Không dùng được cho flow này.

## Cách đi flow, tính tới 2026-09-12

1. **Kelvin bấm icon "Claude in Chrome"** trên toolbar (side panel, đã đăng nhập sẵn),
   dán nguyên nội dung `.ai-bridge/<task>/TASK.md` vào cho Claude-trong-Chrome tự chạy.
2. Hoặc Kelvin tự làm 2 message trong ChatGPT project "mayhoa" theo TASK.md, rồi đưa
   Drive file ID cho agent terminal normalize + wire.

Agent làm được phần trước và sau, **không làm được khúc giữa trong trình duyệt**.

## Hai cái bẫy đã mất thì giờ, đừng dính lại

- **Ảnh ChatGPT trả về có thể bị bake lưới caro giả thay vì alpha thật.** Luôn chạy
  `tools/dechecker.py` trước khi dùng. Đã dính với `tool_hoe_idle_v02.png`.
- **Đổi hình dạng plate thì phải đo lại code**, không chỉ thả file vào:
  `SOIL_PLATE_MASTER_W` trong `mayhoa-farm-demo/src/core/config.ts` đang là `349`,
  đo từ plate oval cũ.

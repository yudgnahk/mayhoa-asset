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

## Cách đi flow, tính tới 2026-09-12 (đính chính 15:50: bỏ Google Drive)

**Kelvin mở Claude** (không phải mở tab ChatGPT tay) → Claude tự dùng "Claude in
Chrome" lái browser vào `chatgpt.com`, gen ảnh qua `@Create image`, rồi **tự bấm nút
tải xuống ngay trên ảnh** để lưu file thẳng vào đĩa — không còn cầu Google Drive.

Dán nguyên nội dung `.ai-bridge/<task>/TASK.md` cho Claude đó chạy. Mỗi TASK.md đã
định sẵn một đường dẫn tuyệt đối `.ai-bridge/<task>/incoming/<tên-file>.png` để lưu
vào, thư mục `incoming/` đã tạo sẵn từ trước — Claude không phải tự đoán chỗ lưu.

**Lý do bỏ Drive, không chỉ vì thừa bước**: MESSAGE @Google Drive là khúc mong manh
nhất — cần gọi connector riêng, có bẫy 'Add from library' nằm ngay đầu dropdown dễ
bấm nhầm thay vì mục 'Google Drive' thật, và tốn thêm vài lần Allow. Cầu Drive chỉ
cần thiết vì hai *tool* của ChatGPT (Create image và Google Drive) không tự truyền
binary cho nhau trong cùng một phiên chat — nhưng khi Claude tự lái browser thì nó
bấm được nút "Download" của chính trình duyệt, không đi qua giới hạn đó nữa.

Agent terminal làm được phần trước (soạn TASK.md, dựng thư mục `incoming/`) và phần
sau (dechecker, normalize, wire vào game) — **không làm được khúc giữa trong trình
duyệt**, đó vẫn luôn là phần Kelvin/Claude-trong-Chrome tự chạy.

## Hai cái bẫy đã mất thì giờ, đừng dính lại

- **Ảnh ChatGPT trả về có thể bị bake lưới caro giả thay vì alpha thật.** Luôn chạy
  `tools/dechecker.py` trước khi dùng. Đã dính với `tool_hoe_idle_v02.png`.
- **Đổi hình dạng plate thì phải đo lại code**, không chỉ thả file vào:
  `SOIL_PLATE_MASTER_W` trong `mayhoa-farm-demo/src/core/config.ts` đang là `349`,
  đo từ plate oval cũ.

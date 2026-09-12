# Workflow gen ảnh asset — đọc TRƯỚC khi chạy, bất kể bạn là agent nào

Doc này là nguồn sự thật duy nhất cho chuỗi **ChatGPT Create image → đĩa local →
QC → `masters/`**. Viết cho agent tự đọc tự chạy, không phải cho người đọc lướt.

`.ai-bridge/` bị `.gitignore` nên mọi thứ cần theo repo phải nằm ở đây, không nằm
trong đó.

Kiểm chứng lần cuối **2026-09-12** bằng cách chạy thật trọn flow, không phải đọc docs.

---

## Bước 0 — TỰ XÁC ĐỊNH MÌNH CHẠY ĐƯỢC LÀN NÀO (bắt buộc, làm trước mọi thứ)

Không đoán. Không suy từ tên session. Probe bằng tool:

```
ToolSearch  query: "select:mcp__claude-in-chrome__list_connected_browsers"
```

- **Nạp được** → gọi `list_connected_browsers`. Có browser `isLocal: true` →
  **LÀN A**, bạn đi được trọn flow.
- **Không có tool đó** → **LÀN B**. Bạn KHÔNG gen được ảnh. Nhảy xuống mục LÀN B.

### Cấm đường vòng

Nếu bạn là agent Paseo, bạn sẽ thấy bộ `mcp__paseo__browser_*` (navigate, click,
fill, screenshot…). **ĐỪNG dùng chúng cho flow này.** Kiểm chứng 2026-09-12: tool
browser của Paseo lái một browser **sạch, chưa đăng nhập** — mở `chatgpt.com` bị đá
thẳng về `chatgpt.com/auth/login`. Và **không được đăng nhập hộ**: nhập mật khẩu hay
tạo tài khoản là việc agent không làm, dù có sẵn credential.

Thấy màn login = dừng, không phải thử cách khác.

---

## Ai chạy được làn nào (kiểm chứng 2026-09-12)

| Runner | Có `mcp__claude-in-chrome__*`? | Gen được ảnh? |
|---|---|---|
| `claude` interactive ở terminal | Có | **Được — LÀN A** |
| Agent Paseo, provider `claude/*` | **Không** | Không tự lái — nhưng **điều phối được**, xem mục dưới |
| Agent Paseo, provider khác (`codex/*`…) | Không | Không — LÀN B |
| Subagent / Task tool trong session Làn A | Không | Không — LÀN B |

Lý do agent Paseo không có bridge: **Paseo spawn `claude` mà không truyền cờ
`--chrome`**, và `paseo run --env` / `--mode` / agent profile đều không chèn cờ vào
được. Cờ `--chrome` cũng không cứu được: kiểm chứng lại 2026-09-12 (lần sau, chính xác
hơn), `claude -p --chrome` có **0** tool `mcp__claude-in-chrome__*` — đọc thẳng mảng
`tools` của event `init` dưới `--output-format stream-json --verbose`: 123 tool, không
cái nào khớp `chrome` hay `browser`, chạy từ `/tmp` lẫn từ repo đều vậy.

Nên có một đường vòng: agent Làn B dùng Bash gọi phiên `claude` lồng có cờ đó. Xem
mục "Đường vòng qua phiên claude lồng" bên dưới trước khi dựa vào nó.

Không phải do thiếu cấu hình phía máy: `~/.claude.json` đã có
`claudeInChromeDefaultEnabled: true` và `chromeExtension.pairedDeviceId` trỏ đúng
"Browser 1", nên phiên interactive **không cần cờ `--chrome`** nữa. Pairing nằm ở
`~/.claude.json` (toàn máy), không phải per-session.

### Đường vòng qua phiên claude lồng — ĐÃ ĐÓNG, KHÔNG CHẠY ĐƯỢC

Đừng thử lại. Kiểm chứng 2026-09-12, ba cơ chế quyền khác nhau, cùng một lỗi
`Claude in Chrome requires permission`:

| Cách | Kết quả |
|---|---|
| `claude -p --chrome` rồi `list_connected_browsers` | **Không có tool để mà gọi** (0 tool chrome) |
| Thao tác thật (`tabs_context_mcp`, `select_browser`) | **Chặn** |
| `--allowedTools` liệt kê đủ tool chrome | **Chặn** |
| `--permission-mode bypassPermissions` | **Chặn** |

**Không phải vấn đề quyền — là vòng đời.** Bridge gắn per-session với phiên
interactive mà extension attach vào. Phiên `-p` sống vài giây, không có UI để attach,
nên không bao giờ nhận được kết nối. Thêm rule vào `settings.json` cũng vô ích: đó
đúng là cơ chế mà `--allowedTools` đã dùng và đã trượt.

Không dùng `--dangerously-skip-permissions` để lách — đã thử tương đương
(`bypassPermissions`), không ăn.

### Thay vào đó: giao việc cho phiên đang cầm bridge (đây LÀ cách Paseo chạy được flow)

Các session Claude trên cùng máy nhắn tin được cho nhau. Agent Làn B không tự lái
Chrome, mà **giao khúc A1–A7 cho một phiên interactive đang có bridge**:

1. `ListAgents` — tìm phiên interactive đang mở ở repo này (thường có tên dạng
   `mayhoa-asset-*`; đã từng có một phiên ngồi sẵn trong tmux `mayhoa-chrome`).
2. `SendMessage` tới phiên đó, kèm đường dẫn `TASK.md` cần chạy và đường dẫn
   `incoming/` mong đợi.
3. Làm tiếp phần offline của mình, đừng ngồi chờ.

Phiên nhận việc phải tự chạy **Bước 0** để xác nhận nó thật sự có bridge — đang mở
không có nghĩa là đang kết nối, và panel `/chrome` báo `Status: Enabled` cũng không
phải bằng chứng.

**Cách 2 — `tmux send-keys`.** Nếu phiên cầm bridge sống trong tmux thì gõ thẳng vào
nó được, không cần SendMessage:

```bash
tmux ls                                   # tìm session, vd. mayhoa-chrome
tmux list-panes -t mayhoa-chrome -F '#{pane_id} #{pane_current_command}'
tmux send-keys -t mayhoa-chrome '<nội dung task>' Enter
```

Đây là cách đã dùng được trước đây từ Paseo. Lưu ý đã ghi trong memory: cơ chế
`send_terminal_keys` của Paseo **không gửi được phím mũi tên**, nên TUI phải bọc trong
tmux rồi lái bằng `tmux send-keys` — đó chính là lý do phiên bridge được nuôi trong
tmux chứ không chạy trần.

**Chốt lại:** agent Paseo không tự lái Chrome được, nhưng **Paseo hoàn thành được
flow** — nó điều phối phiên đang cầm bridge rồi tự làm phần offline. Đừng đọc mục
"ĐÃ ĐÓNG" ở trên thành "Paseo vô dụng với flow này"; cái đóng là đường spawn
`claude -p`, không phải đường điều phối.

---

## LÀN A — chạy trọn flow

### A0. Preflight (làm hết trước khi mở tab, mỗi cái đều từng làm hỏng một lượt chạy)

```bash
# 1. Chrome KHÔNG được hỏi nơi lưu — nếu true, hộp thoại native sẽ chặn và
#    agent không click được (native dialog nằm ngoài tầm với của extension).
python3 -c "
import json,os
# Profile 1, KHÔNG phải Default — extension + session ChatGPT nằm ở Profile 1.
d=json.load(open(os.path.expanduser('~/Library/Application Support/Google/Chrome/Profile 1/Preferences')))
print('prompt_for_download =', d.get('download',{}).get('prompt_for_download'))
ad=d.get('profile',{}).get('content_settings',{}).get('exceptions',{}).get('automatic_downloads',{})
print('chatgpt automatic_downloads =', [v.get('setting') for k,v in ad.items() if 'chatgpt' in k] or 'CHUA SET')"
```

`prompt_for_download = True` → **DỪNG**, nhờ user vào `chrome://settings/downloads`
tắt "Ask where to save each file". Extension không thao tác được trang `chrome://`,
cũng không tắt được setting này hộ. Sửa file `Preferences` khi Chrome đang chạy thì
bị ghi đè — đừng thử.

`chatgpt automatic_downloads` khác `1` → **DỪNG**, nhờ user vào Site settings của
chatgpt.com bật "Automatic downloads → Allow". Không có nó thì **file đầu tiên tải
được, từ file thứ hai trở đi Chrome chặn im lặng** — cả nút Save trong viewer lẫn
anchor download bằng script đều không báo lỗi gì. Đây là kiểu hỏng dễ tưởng nhầm là
gen lỗi. Đã bật 2026-09-12.

```bash
# 2. File reference phải mở được thật. v01 của soil_tilled hỏng IDAT vĩnh viễn.
python3 -c "
from PIL import Image
for p in [<đường dẫn reference>]:
    im=Image.open(p); im.load(); print('OK', p, im.size, im.mode)"

# 3. Đặt mốc thời gian để lát nữa bắt đúng file mới trong ~/Downloads
MARK=$(mktemp); touch "$MARK"
```

### A1. Mở project và tạo chat

Tab mới → `https://chatgpt.com/g/g-p-6a86ae171c34819191aad1a59464472e-mayhoa/project`

Đợi trang render (lần đầu vùng chat trống vài giây — screenshot sớm sẽ thấy màn đen,
đừng tưởng hỏng). Composer nằm ngay trên trang project, chỗ chữ **"New chat in
mayhoa"**. Gõ vào đó là tự tạo chat mới **trong project**, không cần bấm "New chat"
ở sidebar.

ĐỪNG đóng tab sẵn có của user. ĐỪNG restart Chrome.

### A2. Đính file reference

**KHÔNG bấm nút `+` / paperclip** — nó mở native file picker mà agent không thấy và
không điều khiển được. Thay vào đó:

```
find    query: "hidden file input element for attaching files"
         → lấy ref đầu tiên (thường là input trong form composer)
file_upload  paths: [<đường dẫn tuyệt đối>, ...]   ref: <ref đó>
```

Upload nhiều file một lần được. Tổng dưới 10 MB. Xong thì screenshot xác nhận đủ
thumbnail trước khi đi tiếp.

### A3. Chọn tool và gửi prompt

1. Click vào ô composer.
2. `type` chuỗi `@Create image` → dropdown hiện **đúng 1** kết quả ("Create image —
   Visualize anything") → `key Return` để chọn. Composer hiện pill "Create image".
3. `type` nội dung prompt. **Gõ thành MỘT đoạn liền, thay xuống dòng bằng dấu cách.**
   Ký tự newline trong `type` sẽ gửi message sớm. Prompt gộp một đoạn vẫn cho kết quả
   đúng — miễn không mất chữ.
4. Screenshot kiểm tra prompt đủ chữ, rồi `key Return` để gửi.

### A4. Chờ

Tiến trình bình thường: `Analyzing images` → `Generating a more detailed image — hang
tight` (kèm ảnh render dần) → ảnh xong, dưới ảnh hiện nút **Edit** và hàng icon.

Poll mỗi ~30s bằng `browser_batch` (3 lần `wait` 10s + 1 `screenshot`) — nhanh hơn
hẳn gọi lẻ. Thực đo: **~60-90 giây**, không phải "vài phút".

**TUYỆT ĐỐI KHÔNG gửi lại prompt khi đang chạy.**

### A5. QC trước khi tải

Click vào ảnh → **fullscreen viewer**. Dùng `zoom` soi từng vùng, đừng QC bằng
screenshot thu nhỏ.

QC theo acceptance criteria trong `TASK.md` của species đó. Luôn kiểm thêm: không
text / khung / watermark, không vật thể thừa.

FAIL → gửi message sửa **trong cùng chat**, nêu đúng điểm sai. Tối đa 3 vòng, quá thì
dừng và báo cáo.

### A6. Tải về

Trong fullscreen viewer:

- Thanh công cụ giữa chỉ có **Markup / Comment / Remove BG / Erase / Resize** —
  **không có nút tải ở đây.**
- Nút tải là **icon download ở góc trên bên phải header**, cạnh nút Share
  (ở viewport rộng 1280 thì quanh toạ độ `(1201, 24)`).

> Tài liệu cũ ghi nút tên **"Save"** nằm cùng thanh với Remove BG / Erase. Sai từ
> 2026-09-12 — UI đã đổi. Khung chat cũng không có nút download, đừng hover tìm.

File rơi thẳng vào `~/Downloads` tên dạng `ChatGPT Image <ngày giờ>.png`.

```bash
find ~/Downloads -maxdepth 1 -name 'ChatGPT Image*.png' -newer "$MARK" -print0 \
  | xargs -0 ls -tr        # cũ → mới = đúng thứ tự đã bấm Save
```

Thấy file `~/Downloads/.com.google.Chrome.XXXXXX` mà không có PNG nào mới = **hộp
thoại Save native đang mở và chặn Chrome**. Preflight A0 đã trượt. Đừng đụng vào file
temp đó sau lưng Chrome — nhờ user xử lý dialog.

### A7. Nhận file

```bash
mv "<file vừa bắt được>" "<repo>/.ai-bridge/<species>/incoming/<tên chuẩn>.png"

python3 -c "
from PIL import Image
im=Image.open('<đường dẫn đích>'); im.load(); print(im.size, im.mode)"   # phải RGBA
```

### A8. Báo cáo

```
SAVED_TO: <đường dẫn tuyệt đối>
```

Kèm: gen thành công không, số vòng sửa + lý do ảnh đầu bị loại, URL chat, và **mọi
chỗ doc này không còn khớp UI hiện tại**.

---

## LÀN B — bạn không gen được ảnh

Đây không phải lỗi và không có cách lách. Làm đúng phần làm được, rồi trả bóng.

**Làm được:** soạn / sửa `TASK.md`, dựng `incoming/`, viết và tinh prompt, và **toàn
bộ khúc sau khi ảnh đã có trên đĩa** — dechecker, normalize, build atlas, đo geometry,
wire vào game, chạy test, commit.

Nếu `incoming/` đã có ảnh do lượt trước để lại thì cứ xử lý tiếp bình thường.

**Không làm được:** khúc trong trình duyệt (A1–A7).

Báo cáo đúng dạng này, đừng chỉ nói "không làm được":

```
LANE: B — không có mcp__claude-in-chrome__*, không gen được ảnh.
ĐÃ LÀM: <việc offline đã xong>
ĐÃ GIAO: SendMessage tới <tên phiên> để chạy .ai-bridge/<species>/TASK.md
         (hoặc: không tìm thấy phiên nào có bridge → cần user mở `claude` ở terminal
          tại <repo>; bridge tự bật, không cần cờ --chrome)
CHỜ FILE: <đường dẫn incoming/ mong đợi>
```

---

## Hai cái bẫy đã mất thì giờ, đừng dính lại

- **Ảnh ChatGPT trả về có thể bị bake lưới caro giả thay vì alpha thật.** Luôn chạy
  `tools/dechecker.py` trước khi dùng. Đã dính với `tool_hoe_idle_v02.png`.
- **Đổi hình dạng plate thì phải đo lại code**, không chỉ thả file vào:
  `SOIL_PLATE_MASTER_W` trong `mayhoa-farm-demo/src/core/config.ts` đang là `349`,
  đo từ plate oval cũ. Đặc biệt đúng với `soil_square`.

## Gotcha hạ tầng

- **Bridge chết sau khi update Claude Code CLI.** `~/.claude/chrome/chrome-native-host`
  hardcode đường dẫn kèm số phiên bản
  (`/opt/homebrew/Caskroom/claude-code@latest/<ver>/claude`), update là trỏ trượt.
  Chạy lại `claude --chrome` để nó ghi lại wrapper, rồi bấm Reconnect trong extension.
  Đừng sửa tay file wrapper, đừng tin panel `/chrome`.
- Flow này chỉ đúng khi Chrome và repo ở **cùng một máy**.
- Cần plan trả phí + quyền `debugger` cho extension. Không hỗ trợ Chromium khác/mobile.

## Đã bỏ, đừng dựng lại

- **Google Drive + `gws`** — bỏ 2026-09-05. Cầu Drive chỉ cần khi executor không nhận
  được binary trực tiếp; tự lái browser thì bấm nút tải là xong. Bỏ được một connector
  call, vài lần Allow, và rủi ro OAuth hết hạn (token `gws` đã bị revoke đúng lúc cần).
- **CodexPro2 và mọi Codex-backed executor** — không còn vai trò nào trong flow này.

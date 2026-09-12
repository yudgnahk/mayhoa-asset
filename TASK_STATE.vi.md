# TASK_STATE — bàn giao phiên 2026-09-05/07

**Ngôn ngữ:** Tiếng Việt · [English](TASK_STATE.en.md)

> Đọc file này trước khi làm gì. Cập nhật nó khi trạng thái đổi, hoặc xoá khi queue regenerate đã hết.
>
> **Cập nhật 2026-09-10:** PR #2 và PR #3 đều đã merge, `master` ở `795e0b0`. Mục "Đang ở đâu" bên dưới là ảnh chụp phiên 09-05/07, giữ lại làm lịch sử.

## Phiên 2026-09-11 — Gate A pest + tool

Queue: `.ai-bridge/GATE_A_GEN_BRIEF.md`. Prompt spec: `FARM_GATE_A_PEST_TOOL_PROMPTS.vi.md`.

**Xong:**
- `pest_caterpillar-single` — `present` + `cleared`, 512×512, đã QC composite lên
  rice/corn/carrot ở cell 192px. P0-2 đóng.
- `tool_hoe` — `idle` + `selected`.

**Còn lại 6 file:** `watering-can`, `pest-catcher`, `harvest-hand` (mỗi cái idle +
selected). `watering-can` đã generate xong trên ChatGPT nhưng **chưa tải về được**.

**BLOCKER — Chrome chặn download từ chatgpt.com.** Sau vài file đầu, cả download
bằng script lẫn nút `Save` ở fullscreen viewer đều im lặng không ra file. Reload
trang không gỡ được. Cần bấm cho phép trong UI của chính Chrome (thanh địa chỉ →
biểu tượng download bị chặn, hoặc Settings → Site settings → chatgpt.com →
Automatic downloads → Allow). Browser tool không chạm được UI native của Chrome.

**Hai thay đổi pipeline trong phiên này — đọc trước khi gen tiếp:**

- **Raw ChatGPT không còn có alpha.** Create image trả PNG colortype 2 và *vẽ* lưới
  caro trắng/xám vào pixel thay cho nền trong suốt; `Save` chỉ bake cái caro đó ra
  file. Chạy `python3 tools/dechecker.py raw.png out.png` trước mọi bước khác.
  Flood fill từ mép (color key thuần sẽ đục thủng mắt trắng trong sprite) rồi
  difference matting ở rìa. Nút `Remove BG` của viewer không sinh ra gì.
- **Tool state `selected` không generate.** Model không giữ nổi pose/scale nên icon
  nhảy trong thanh công cụ. Dùng `tools/make_selected.py` trên chính master idle.
  Vì glow tràn ra ngoài silhouette, tool idle normalize với `--margin 34`.

Chưa làm theo brief: `carrot` s05 (optional), 4 background, tree/aquatic, weed,
5 pest còn lại.

---

## Mục tiêu đang theo đuổi

Đưa 19 pack asset (95 file) về đúng geometry contract, rồi chạy nốt queue regenerate.
Source of truth cho mọi con số: `MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.vi.md`.
Trạng thái việc: `ASSET_GEOMETRY_FIX_CHECKLIST.vi.md` — **mục 9 là đợt QC mới nhất**.

## Đang ở đâu

- Branch `fix/geometry-qc-2026-09-05`, **12 commit**, đã push.
- **PR #2**: https://github.com/yudgnahk/mayhoa-asset/pull/2 — ~~chưa merge~~ **đã merge 2026-09-05**.
- ~~`master` vẫn ở `dd224e1`~~ → `master` nay ở `795e0b0` (sau PR #3 `assets/durian-pack`, merge 2026-09-09).
- Working tree sạch.

Kết quả QC: geometry core (canvas / contactY Δ0 / rootX / RGBA8) **PASS 95/95 file plant**, không regression so với đợt normalize 26-08.

## Đã xong trong phiên này

| | |
|---|---|
| `carrot` s04 | margin 22px → 26px (normalize lại từ bản gốc `5276109`, scale 0.9004) |
| `geometry_audit.py` | vá bug nuốt file sau khi gặp PNG hỏng; +7 test |
| 5 soil tile | palette → RGBA8, lossless, đối chiếu 100% pixel |
| `soil_tilled` | generate lại thành `v02` (v01 hỏng IDAT vĩnh viễn) |
| 3 doc gap | `rubber` / `water-mimosa` / `water-spinach` đã normalize nhưng không được ghi |
| Species tiếng Việt | `thien-ly` → `tonkin-jasmine`, `ngo-gai` → `culantro` |
| `tools/build_atlas.py` | mới, 33 test, idempotent — atlas giờ tái tạo được *(2026-09-10: thêm guard canvas/anchor, 42 test)* |
| 4 atlas runtime | gom theo class, thay 5 atlas cũ |
| Asset transport | bỏ hẳn chặng Google Drive + `gws` |

## Còn treo — 7 mục

**Cần pipeline sinh ảnh** (queue mục 6 checklist, specs+prompts sẵn ở `FARM_REGENERATION_PROMPTS.vi.md`):
- `carrot` s05 — harvest cue quá yếu (~10px ở display size)
- `tonkin-jasmine` cả pack — chuyển sang dạng dây leo giàn (Profile C như dragon-fruit)
- `lotus` s05 — bông sen nhỏ lại 60–70%
- **`6 fruit tree`** — silhouette đặc trưng từng loài. *Đáng làm nhất*: đã kiểm bằng mắt, tán mango và rambutan gần như trùng nhau, chỉ khác màu quả.

**Cần môi trường game** (game code chưa tồn tại):
- Playground: stage transition, root không nhảy khi sway
- Xác nhận engine ghim crop anchor vào tâm plate, khớp `(0.5, 0.89453125)`

## Cách chạy pipeline sinh ảnh

**Đã đổi. Không dùng Google Drive, không dùng `gws`** (`gws` token đã revoke, và không cần nữa).

1. Session Claude Code phải khởi động bằng `claude --chrome` — browser tool **không bật được giữa session**.
2. Đang có sẵn: tmux session **`chromebridge`** trong terminal Paseo `f023b260-b6de-497a-b07c-40dc566ef23e`, bridge còn sống (đã kiểm 2026-09-07).
3. Lái bằng `tmux send-keys -t chromebridge ...` + `tmux capture-pane -p -t chromebridge`.
   **`mcp__paseo__send_terminal_keys` KHÔNG gửi được phím mũi tên** — chỉ `Enter`/`Escape`/`BSpace`.
4. Một message ChatGPT: `@Create image` + prompt + ảnh reference.
5. Mở ảnh ở **fullscreen viewer**, bấm **"Save"** (không phải "Download", và không có nút này ở khung chat) → rơi vào `~/Downloads`.
6. Nhận diện file mới — đặt mốc TRƯỚC khi bấm Save:
   ```bash
   MARK=$(mktemp); touch "$MARK"
   find ~/Downloads -name 'ChatGPT Image*.png' -newer "$MARK" -print0 | xargs -0 ls -tr
   ```
7. Raw vào `.ai-bridge/<species>/`, QC, normalize, rồi mới vào `masters/`.

Chi tiết đầy đủ: mục "Asset sync transport" trong `FARM_ASSET_GENERATION_PLAN.vi.md`.

## Bẫy đã trả giá — đừng vấp lại

**Reference quyết định hình học output.** Đính `soil_empty` (plate 2.15:1) làm reference khiến Create Image cho ra plate 2.13:1 trong khi nhóm đích là 1.71:1 — tốn 2 vòng gen thừa. **Chỉ đính reference thuộc đúng nhóm hình học muốn khớp.**

**Đừng suy nội dung từ số đo hình học.** Agent QC thấy bbox `water-mimosa` và `water-spinach` trùng nhau trong 1px rồi kết luận artwork có thể trùng. Mở ảnh ra xem thì hai loài khác hẳn. Bbox trùng chỉ vì cùng normalize về một canvas/anchor.

**`rootX` bottom-band vô nghĩa với morphology rosette/aquatic** (spec §7.1). Nếu dùng nó làm `anchorX` thì `culantro` trượt ngang 37px mỗi lần đổi stage. `anchorX` **luôn = 0.5**; chỉ `contactY` mới đo. `build_atlas.py` đã làm đúng và in `NOTE QC` cho các species lệch.

**Chạy `normalize_pack.py` lên `water-mimosa`/`water-spinach` mà không có `--rootx` override sẽ phá alignment đang đúng** (dịch s02 khoảng −90px). Hai pack này ĐÃ đạt chuẩn, anchor `(384, 728)`.

**Normalize phải xuất phát từ artwork gốc**, không transform chồng lên master hiện tại. Margin stage-05 của `rubber`/`mango`/`pomelo` đang ở 25px, cushion chỉ 1px — resample thêm lần nữa là tụt dưới ngưỡng 24px.

**Bridge Claude-in-Chrome**: wrapper `~/.claude/chrome/chrome-native-host` pin theo version và tự regenerate mỗi lần chạy `claude --chrome`. **Đừng sửa tay** (sửa cũng bị ghi đè). Sau khi CLI auto-update: chạy `claude --chrome` một lần rồi `/chrome` → **"Reconnect extension"** (bước bắt buộc, không phải dự phòng). Panel `/chrome` báo `Status: Enabled` **không** có nghĩa là đã kết nối — chỉ tin `pgrep -fl chrome-native-host`.

## Lệnh hay dùng

```bash
python3 tools/geometry_audit.py masters/farm/<class>/<species>/*.png
python3 tools/build_atlas.py --dry-run          # xem kế hoạch
python3 tools/build_atlas.py                    # build lại 4 atlas
python3 -m unittest discover -s tools -p 'test_*.py'   # 67 test
python3 tools/dechecker.py raw.png out.png            # dựng lại alpha từ nền caro
python3 tools/make_selected.py idle.png selected.png  # state selected của tool icon
```

Atlas là **build product** — sửa master rồi chạy lại script, đừng sửa tay atlas.

## Quyết định đã chốt trong phiên (đừng mở lại nếu không có lý do mới)

- Atlas gom **theo class**, tên `<domain>_<class>_v01`. Cách chia core/herb cũ phản ánh phase sản xuất, không phản ánh nhu cầu lúc load.
- Frame key = **slot id** `<species>_stage-0N`. Nhãn stage lệch nhau giữa species (`coffee`→berry, `rubber`→tapping) nên key mang nhãn buộc game phải tra bảng. Semantic tách sang `stageNames`.
- Soil frame key dùng full stem (`soil_dry`), khác quy tắc trên — có chủ đích.
- `mango`/`rambutan` s05 nhỏ hơn s04: **chấp nhận**, do chùm hoa s04 biến mất chứ không phải cây teo.
- `water-mimosa` vs `water-spinach`: **PASS**, hai loài khác hẳn.

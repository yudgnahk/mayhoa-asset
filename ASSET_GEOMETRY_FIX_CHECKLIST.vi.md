# Mayhoa — Asset Geometry Fix Checklist

**Status:** normalize 2026-08-26 xong; **QC lại 2026-09-05** — 95/95 file plant PASS geometry core, phát sinh 2 việc blocking + 3 lỗ hổng tài liệu (xem mục 9)
**Baseline:** đo 2026-08-26 bằng `tools/geometry_audit.py` (alpha ≥ 24/255, bottom band 3%) — chi tiết ở §20 của spec
**Spec:** `MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.vi.md` (source of truth cho mọi con số)

---

## Quy tắc chung

**Công thức normalize mỗi pack** (chỉ dùng transform được phép theo spec §12.1 — scale + translate, KHÔNG redraw):

1. Scale **đồng nhất một hệ số `s` cho cả 5 stage** (giữ nguyên within-species progression), resample LANCZOS, giữ RGBA.
2. Translate **từng stage riêng** để root về đúng `(512, 970)` trên canvas `1024×1024`.
3. `s` do `tools/normalize_pack.py` tự tính = min các constraint để mọi pixel cách mép ≥ 24 px, tính theo extent thực quanh root từng stage (không giả định root nằm giữa bbox).

**Acceptance criteria** (verify bằng `python3 tools/geometry_audit.py masters/farm/<class>/<species>/*.png`):

- Canvas đúng target; contactY = 970, Δ = 0 (trừ crop — soil-plate anchor, spec §5.3).
- rootX = 512 ± 2 px; radial/rosette verify bằng mắt (spec §7.1).
- Không pixel nào cách mép < 24 px; không clip; style không vỡ sau resample.
- Verify trên raw PNG, không chỉ qua playground (spec §12.3).

---

## 0. Chuẩn bị — DONE

- [x] Baseline artwork gốc đã được stage trong git (user làm) — diff/compare bằng `git diff` với index.
- [x] `tools/normalize_pack.py` — viết xong (mode `root` cho tree/aquatic, mode `anchor` cho crop; auto-scale theo margin constraint; tự đo + tự verify sau transform).
- [x] Baseline khớp Appendix A.

## 1. Không đụng — DONE

- [x] **coffee** — PASS chuẩn calibration ngay từ đầu. Giữ nguyên, không transform.

## 2. Normalize tree packs — DONE (2026-08-26)

Root đích `(512, 970)` trên `1024×1024`. Scale **thực tế đã áp** (auto-tính, khác ước lượng ban đầu vì root không nằm giữa bbox — constraint tính theo extent trái/phải quanh root):

| Pack | Scale đã áp | Kết quả audit |
|---|---:|---|
| [x] dragon-fruit | 0.9823 | contactY 970 Δ0, rootX 512.0–512.5, margin ≥ 26 |
| [x] mango | 0.9271 | contactY 970 Δ0, rootX 511.7–512.4, margin ≥ 25 |
| [x] pomelo | 0.7447 | contactY 970 Δ0, rootX 511.7–512.4, margin ≥ 25 |
| [x] lemon | 0.8147 | contactY 970 Δ0, rootX 511.6–512.4, margin ≥ 25 |
| [x] star-apple | 0.7554 | contactY 970 Δ0, rootX 511.6–512.4, margin ≥ 25 |
| [x] lychee | 0.7855 | contactY 970 Δ0, rootX 511.6–512.3, margin ≥ 26 |
| [x] rambutan | 0.7682 | contactY 970 Δ0, rootX 511.7–512.1, margin ≥ 25 |
| [x] rubber | không truy được (*) | contactY 970 Δ0, rootX 512.0–512.4, margin ≥ 25 |
| [x] coconut | per-stage, xem mục 3 | contactY 970 Δ0, rootX 511.6–512.3, margin ≥ 26 |

(*) `rubber` **đã qua cùng pass normalize 2026-08-26 nhưng không được ghi lại hệ số scale** — không truy ngược được từ lịch sử, đừng đoán số. Provenance: pack chỉ xuất hiện ở commit `dd224e1`, mtime `Aug 26 03:42` (muộn hơn 6 pack còn lại ở `01:01–01:02`). Xác minh 2026-09-05: canvas `1024²`, RGBA8, ratio visH = 0.400 / 0.600 / 0.820 / 0.939 / 1.000 — cả 5 stage nằm trong band Profile A. Số đo per-stage ở Appendix B.

## 3. Coconut Profile B per-stage rescale — DONE (gộp 1 pass với mục 2)

- [x] Scale per-stage đã áp: s01 `0.392`, s02 `0.461`, s03 `0.584`, s04 `0.714`, s05 `0.768` (= base 0.768 × hệ số Profile B, resample 1 lần duy nhất cho chất lượng tốt nhất).
- [x] Ratio mới: **0.332 / 0.506 / 0.725 / 0.916 / 1.0** — nằm gọn trong band Profile B (0.25–0.35 / 0.40–0.55 / 0.65–0.78 / 0.88–0.96).
- [x] Visual check s01–s03: style painterly giữ tốt sau downscale, nét vẽ vẫn sắc → KHÔNG cần regenerate.

## 4. Lotus — DONE

- [x] Resample `0.8314` → 1024×1024, contactY → 970, rootX 511.9–512.5.
- [x] Phát hiện khi visual check: cả 5 stage lotus có **cụm thân hội tụ sát đáy, band đáy không dính lá** → bottom-band centroid ở đây chính là tâm bụi, dùng auto-align được (không cần đánh tay như dự phòng §7.1).
- [x] Spread progression giữ nguyên 0.25 / 0.64 / 0.81 / 0.95 — khớp Profile D (đã nới).

## 5. Crops — DONE (rev 2 cuối: bottom-anchor, trồng giữa luống)

Hai vòng chỉnh: (a) composite lên `soil_planted` (plate y 157–360) phát hiện chân crop lòi dưới plate; (b) user chỉ ra cây phải đứng **giữa ô đất** + calibration sheet xác nhận → chốt contract cuối (spec §5.3): **crop = sprite bottom-anchor như tree**, root `(256, 458)`, engine ghim vào **tâm plate `(256, 260)`**. Nhờ bỏ giả định bake-1:1, chiều cao dùng được tăng 326 → 434 px nên hầu hết pack giữ nguyên kích thước gốc.

Đã làm — restore bản gốc từ git index, transform một lần duy nhất (single resample):

| Pack | Scale | Align X | Kết quả |
|---|---:|---|---|
| [x] rice | 1.0 (chỉ translate) | bottom-band | contactY 458 Δ0, rootX ~256, RGBA8 |
| [x] corn | 0.8855 | bottom-band | contactY 458 Δ0, rootX ~256, RGBA8 |
| [x] carrot | 0.9040 | bottom-band | contactY 458 Δ0, rootX ~256, RGBA8 |
| [x] thien-ly | 1.0 (chỉ translate) | bbox center | contactY 458 Δ0, margin L/R đối xứng |
| [x] ngo-gai | 1.0 (chỉ translate) | bbox center | contactY 458 Δ0, margin L/R đối xứng |
| [x] mint | 1.0 (chỉ translate) | bbox center | contactY 458 Δ0 |

- [x] Composite QC 30 frame + playground: chân cây tại tâm plate, không lòi dưới plate.
- [x] Visual checks giữ nguyên kết luận cũ: carrot s05 củ cam rõ, thien-ly s05 hoa vàng rõ, ngo-gai cân đối — không regenerate.
- [ ] **Xác nhận phía game code**: engine ghim crop anchor vào tâm plate của tile (không phải mép/điểm khác), khớp anchor mới `(0.5, 0.89453125)`.

## 6. Regenerate queue — RỖNG 🎉

Toàn bộ 6 case ứng viên đều PASS visual check, không file nào phải generate lại:

- [x] rambutan s05: quả chôm chôm đỏ dày đặc, đọc trưởng thành hơn s04 rõ rệt.
- [x] mango s05: quả xoài vàng cam nổi bật.
- [x] dragon-fruit s05: quả thanh long hồng đậm, phân biệt tốt với s04 (hoa trắng).
- [x] coconut s01–s03: style giữ tốt sau downscale.
- [x] thien-ly s05, carrot s05: harvest cue đủ mạnh.

Ghi chú art-style (không blocking, ngoài scope geometry): thien-ly s05 và ngo-gai có bóng đổ nhẹ bake dưới gốc; carrot hơi vector-clean so với các pack painterly — cân nhắc khi có đợt regenerate style sau.

- [ ] **PHÁT HIỆN MỚI (khi dựng playground)**: `masters/farm/soil/soil_tilled_v01.png` **hỏng dữ liệu** — IDAT stream corrupt, PIL/zlib không decode được, bản trong git HEAD cũng hỏng y hệt (được commit trong tình trạng corrupt); sips decode ra toàn nhiễu trắng đen. Không cứu được → **phải regenerate tile tilled**. 5 soil state còn lại bình thường.

Bổ sung từ visual review của user (2026-08-26) — đợt regenerate kế tiếp:

- [ ] **carrot s05** — lộ vai củ cam nhiều hơn (harvest cue hiện chỉ ~10 px ở display size, quá yếu).
- [ ] **thien-ly (cả pack)** — chuyển sang dạng dây leo giàn với giàn cố định xuyên 5 stage, theo contract support-structure như dragon-fruit (Profile C).
- [ ] **lotus s05** — bông sen chính nhỏ lại ~60–70% hiện tại (đang to hơn cả lá lớn nhất — overload focal cue).
- [ ] **6 fruit tree** — regenerate với silhouette đặc trưng từng loài: xoài tán vòm rộng, vú sữa lá hai màu xanh/đồng, bưởi tán thưa quả to, vải/chôm chôm tán tròn dày thấp, chanh dạng citrus bụi thấp; hiện chỉ khác nhau ở quả.

Calibration display scale đã chốt (không đụng master): corn → class L (~224 px, cao vượt rice); lemon → fruit tree thấp nhất (~256 px, biên L/XL). Đã ghi vào spec §9.5.

**→ Specs + prompts cho toàn bộ queue trên: `FARM_REGENERATION_PROMPTS.vi.md`** (38 file: soil_tilled, carrot s05, thien-ly ×5, lotus s05, 6 fruit tree ×5). Generate xong bỏ file `_v02` vào masters rồi gọi Claude chạy pipeline QC/normalize.

## 7. Runtime metadata — MỘT PHẦN

- [x] `runtime/core_fruit_trees_v02.json` + `runtime/1x/farm/trees/core_fruit_trees_v02.png` — rebuild xong từ masters mới: atlas 1280×1024, cell 256×256, masterCanvas 1024×1024, anchor `(0.5, 0.947265625)`. File v01 giữ nguyên để so sánh/rollback.
- [ ] **CHỜ QUYẾT ĐỊNH NAMING**: atlas cho các pack chưa từng có runtime JSON — lychee, rambutan, coffee, dragon-fruit, coconut, lotus. Plan docs không định nghĩa cách gộp pack (1 atlas chung? theo wave? per-species?) và tên file ảnh hưởng code load của game → cần chốt trước khi build. Build bằng cùng script pattern như v02.
- [x] `core_crops_v01.png` / `herb_crops_v01.png` — **đã rebuild texture** từ masters bottom-anchored (960×576, cell 192, layout không đổi) và **đã sửa JSON**: `placementAnchor` + per-frame anchor đổi `(0.5, 0.684)` → `(0.5, 0.89453125)`. Game code load 2 atlas này cần dùng anchor mới + ghim vào tâm plate.

## 8. Verify cuối — CHỜ

- [ ] Playground: stage transition từng species — root không nhảy, không clip khi sway (cần môi trường game).
- [ ] User compare artwork trước/sau bằng `git diff` với bản đã staged.
- [ ] Commit theo pack sau khi duyệt (`fix: normalize <species> pack geometry to canonical anchor`).

---

## 9. QC round 2026-09-05 — audit lại toàn bộ 19 pack

**Cách chạy:** 4 subagent read-only song song (trees ×2, aquatic, crops) dùng `tools/geometry_audit.py`. Không file PNG nào bị sửa; `normalize_pack.py` không được gọi.

**Kết quả tổng:** geometry core (canvas / contactY Δ0 / rootX / RGBA8) **PASS 95/95 file plant**. **Không có regression** so với đợt normalize 2026-08-26 — số đo 4 pack ở mục 2 và 6 pack ở mục 5 trùng khớp chính xác bảng đã ghi.

| Nhóm | PASS | WARN | FAIL |
|---|---|---|---|
| trees (10) | coconut, coffee, rubber, pomelo, lychee, star-apple | dragon-fruit, mango, lemon, rambutan | — |
| aquatic (3) | water-mimosa, water-spinach | lotus | — |
| crops (6) | rice | corn, thien-ly, ngo-gai, mint | carrot |
| soil (6) | — | 5 tile (palette ct=3) | soil_tilled |

### 9.1 Blocking — phải sửa

- [x] **carrot s04 — vi phạm margin (PHÁT HIỆN MỚI).** `carrot_stage-04_mature_v01.png` bbox=(57,22)-(433,458), top margin **22 px < 24**. Không phải regression mà là **fix chưa trọn** ở mục 5: scale `0.9040` hơi lỏng, đúng phải ≈ `0.8999` (trần visH hợp lệ = 458−24+1 = 435, hiện 437). Baseline trước normalize là 12 px → đã cải thiện nhưng chưa đạt.
      **Bắt buộc:** normalize lại **từ bản gốc trong git**, KHÔNG transform chồng lên file hiện tại (tránh resample lần hai).
- [x] **`tools/geometry_audit.py` không bắt `zlib.error`.** Hàm `main()` chỉ `except ValueError`, nên gặp file IDAT hỏng là crash giữa chừng và **bỏ im lặng mọi file phía sau** trong glob (lần này bỏ sót `soil_wet_v01.png`). Hệ quả: mọi kết quả audit batch chạy trên thư mục có file hỏng đều có thể thiếu mà không ai biết. Bọc `zlib.decompress` trong `alpha_rows()` và raise `ValueError` để `main()` báo `ERR` rồi chạy tiếp.

### 9.2 Lỗ hổng tài liệu — 3 pack đã normalize đúng nhưng KHÔNG được ghi

`grep -n "rubber\|water-mimosa\|water-spinach"` trên file này → **0 hit**. Cả ba pack thực tế đều đã đạt chuẩn (số đo ở Appendix B). Đây là lỗi tài liệu, **không phải lỗi asset — KHÔNG normalize lại**.

- [x] Thêm `rubber` vào bảng mục 2 và vào Appendix B. Ratio visH = 0.400 / 0.600 / 0.820 / 0.939 / 1.000 — cả 5 stage nằm trong band Profile A. Provenance: chỉ có trong commit `dd224e1`, mtime `Aug 26 03:42` (muộn hơn 6 pack còn lại), tức đã qua cùng pass normalize nhưng không được ghi lại.
- [x] Sửa spec `MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.vi.md` §5.4 (dòng ~297): `water-mimosa` / `water-spinach` hiện ghi *"anchor chốt khi generate"*. Anchor thực tế **đã chốt là `(384, 728)`** — trong đó `728 = round(768 × 970/1024)`, đúng tỷ lệ bottom-padding convention của tree/lotus. Align X dùng **bbox center** (Profile E), không phải bottom-band.
- [x] **RỦI RO CỤ THỂ nếu không sửa:** session sau đọc doc sẽ tưởng 2 pack chưa làm và chạy `normalize_pack.py`. Nếu chạy **không có `--rootx` override**, bottom-band heuristic sẽ dịch `water-mimosa` s02 khoảng **−90 px** và **phá alignment đang đúng** (rootX bottom-band pack này trải 376.9–474.0 — đúng ca hỏng heuristic mà §7.1 đã gọi tên `water-mimosa`).

### 9.3 Soil — mở rộng phạm vi mục 6

- [ ] `soil_tilled_v01.png` — **xác nhận lại: hỏng vĩnh viễn.** IHDR/PLTE/tRNS/IEND CRC hợp lệ, riêng IDAT (5634 B) **CRC FAIL**; zlib `Error -3: incorrect data check`, giải nén ra 0/262656 byte. md5 working tree **trùng git HEAD** → không có bản lành trong lịch sử để restore. Phải regenerate.
- [x] **5 soil tile còn lại đều là palette PNG (colortype 3)** — vi phạm §6.3 (master bắt buộc RGBA8), giống các crop pack cũ trước khi normalize. Chưa từng được ghi nhận. Gộp vào cùng đợt regenerate `soil_tilled`.

### 9.4 Cần visual review của user (máy không kết luận được)

- [ ] **`water-mimosa` vs `water-spinach` giống nhau đáng ngờ.** X-extent gần trùng từng pixel ở cả 5 stage: visW `213/368/509/636/707` vs `213/369/509/636/708`; bbox s03 `(130,466)-(638,728)` vs `(129,466)-(637,728)`. Spec dòng ~628 yêu cầu water-spinach có *"distinct silhouette from water-mimosa"*. Geometry PASS, nhưng cần xem cạnh nhau để xác nhận không đọc ra cùng một cây.
- [ ] **`mango` s05 thấp hơn s04 80 px** (visH 921 → 841; top bbox 50 → 130) và **`rambutan` s05 co lại cả hai chiều** (visW −39, visH −44). Cả hai đã được duyệt visual ở mục 6 với lý do tán rủ khi đậu quả / trưởng thành đọc qua mật độ quả, nhưng vẫn lệch contract global "size tăng rõ s01<s02<s03<s04<s05". **Cần anh chốt: chấp nhận như species-specific reason, hay đưa vào regenerate queue.**
- [ ] `lotus` s05 visH 907 < s04 928 — art issue, normalize không sửa được. Đã nằm sẵn trong regenerate queue mục 6 (bông sen quá to).

> **Đã thực thi 2026-09-05** (branch `fix/geometry-qc-2026-09-05`): 9.1 và 9.2 xong; 9.3 mới xong phần convert RGBA8.
> `soil_tilled` và toàn bộ 9.4 vẫn treo — xem mục 9.7.

### 9.5 WARN không cần hành động (morphology đúng spec)

- `corn` visW thu hẹp khi lên cao — thân đơn, visH đơn điệu → §9.3 dominant metric PASS.
- `dragon-fruit` visH bão hòa ~942–945 px — Profile C support-structure, trụ giàn cố định chi phối; metric thật là visW (0.328/0.787/0.874/1.001/1.000).
- `lemon` s05 visH −3 px, `mint` s02 visW −6 px — dưới ngưỡng nhiễu đo.
- `ngo-gai` / `mint` / `thien-ly` rootX bottom-band trải rộng — rosette/bbox-center theo §7.1, margin L/R đối xứng Δ≤2 px xác nhận align đúng.

### 9.6 Cảnh báo cho đợt regenerate sắp tới

**Margin stage-05 đang sát trần 24 px, cushion chỉ 1–2 px:** rubber s05 top 25, mango s05 left 25, pomelo s05 top 25, carrot s04 top 22 (đã FAIL), coconut s05 top 26, dragon-fruit s03 top 26.

→ Queue regenerate ở mục 6 (soil_tilled, carrot s05, thien-ly ×5, lotus s05, 6 fruit tree) khi chạy normalize **phải xuất phát từ artwork gốc**, không transform chồng lên master hiện tại — jitter LANCZOS một lần resample nữa là tụt dưới ngưỡng.

---

## Appendix A — Số đo nguồn per-stage TRƯỚC normalize (2026-08-26, để đối chiếu)

Định dạng: `contactY / rootX / visW×visH`.

| Pack | s01 | s02 | s03 | s04 | s05 |
|---|---|---|---|---|---|
| coffee (1024²) | 970 / 511.1 / 349×340 | 970 / 511.6 / 548×580 | 970 / 512.7 / 780×780 | 970 / 511.8 / 882×870 | 970 / 512.2 / 951×900 |
| dragon-fruit (1024²) | 988 / 499.7 / 281×922 | 987 / 501.1 / 675×949 | 988 / 500.1 / 749×962 | 988 / 500.7 / 857×958 | 987 / 500.7 / 857×958 |
| coconut (1254²) | 1236 / 646.6 / 558×797 | 1236 / 646.2 / 864×1036 | 1236 / 646.4 / 1074×1172 | 1236 / 645.6 / 977×1214 | 1236 / 645.5 / 952×1231 |
| mango (1122×1402) | 1292 / 581.2 / 553×463 | 1310 / 571.2 / 792×696 | 1303 / 579.8 / 884×889 | 1282 / 568.2 / 1008×993 | 1290 / 580.3 / 1005×907 |
| pomelo (1122×1402) | 1290 / 568.1 / 430×297 | 1291 / 575.5 / 733×743 | 1347 / 573.7 / 907×1021 | 1342 / 575.7 / 1080×1112 | 1357 / 579.0 / 1106×1269 |
| lemon (1122×1402) | 1229 / 570.7 / 426×291 | 1167 / 560.7 / 575×699 | 1217 / 566.3 / 820×979 | 1259 / 581.3 / 985×1160 | 1253 / 573.3 / 1077×1158 |
| star-apple (1122×1402) | 1218 / 567.2 / 431×324 | 1275 / 569.8 / 677×659 | 1364 / 575.1 / 895×963 | 1342 / 568.4 / 1020×1121 | 1317 / 571.4 / 1093×1251 |
| lychee (1254²) | 1155 / 649.8 / 518×684 | 1187 / 698.0 / 745×976 | 1191 / 679.7 / 895×1103 | 1217 / 664.7 / 1163×1185 | 1230 / 659.7 / 1176×1203 |
| rambutan (1254²) | 1182 / 641.1 / 407×538 | 1177 / 647.5 / 572×844 | 1173 / 646.6 / 791×1032 | 1211 / 643.9 / 1233×1200 | 1188 / 640.9 / 1183×1143 |
| lotus (1254²) | 1187 / 626.6 / 292×476 | 1187 / 631.7 / 750×817 | 1186 / 647.5 / 951×974 | 1185 / 585.4 / 1116×1115 | 1187 / 597.1 / 1169×1090 |

## Appendix B — Số đo SAU normalize cho 3 pack thiếu trong Appendix A (đo 2026-09-05)

Định dạng: `contactY / rootX / visW×visH`. Cả 3 pack RGBA8 (ct=6), non-interlaced, canvas đồng nhất 5/5 stage.

| Pack | s01 | s02 | s03 | s04 | s05 |
|---|---|---|---|---|---|
| rubber (1024²) | 970 / 512.4 / 259×378 | 970 / 512.2 / 361×568 | 970 / 512.0 / 613×776 | 970 / 512.4 / 763×888 | 970 / 512.0 / 844×946 |
| water-mimosa (768²) | 728 / 376.9 / 213×79 | 728 / 474.0 / 368×154 | 728 / 423.8 / 509×263 | 728 / 411.7 / 636×344 | 728 / 390.9 / 707×432 |
| water-spinach (768²) | 728 / 385.1 / 213×113 | 728 / 401.3 / 369×186 | 728 / 390.9 / 509×263 | 728 / 381.9 / 636×336 | 728 / 410.8 / 708×402 |

**Lưu ý đọc bảng:** `rootX` của 2 pack aquatic là bottom-band centroid — **chỉ tham khảo**, không dùng để PASS/FAIL (§7.1, Profile E). Alignment thật của chúng là **bbox center X = 383.0–384.5** (tâm canvas 383.5, Δ ≤ 1.5 px), margin L/R đối xứng trong 1–2 px ở mọi stage.

---

## 9.7 Còn treo sau đợt fix 2026-09-05 — cần input ngoài

Hai nhóm dưới đây **không sửa được bằng code**, đã cố ý để checkbox trống.

### Cần pipeline sinh ảnh (ChatGPT Create image → Drive → gws)
- [x] `soil_tilled_v01.png` — đã generate lại thành **`soil_tilled_v02.png`** (2026-09-05).
      Qua 3 vòng: v1 aspect 2.13 (loại — đính nhầm `soil_empty_v01` làm reference nên bám tỷ lệ
      của tile đó), v2 1.80 (còn viền đỏ artifact 339px), **v3 1.64 — chọn bản này**.
      Fit về 512² bằng uniform scale 0.3818 khớp bề ngang: bbox `(81,147)-(430,360)` so với
      nhóm `dry/harvested/planted/wet` `(82,157)-(430,360)` — mép trái/phải lệch 1px, contactY
      khớp chính xác, sâu hơn 10px phía sau plate (chênh aspect còn lại, uniform scale không
      khử được). RGBA8. `v01` giữ nguyên trong repo dù hỏng, để đối chiếu lịch sử.
- [ ] Rebuild `runtime/soil_states_v01` từ `soil_tilled_v02` — atlas hiện dựng từ bản v01 hỏng.

### Cần quyết định visual của user
- [ ] `water-mimosa` vs `water-spinach` — silhouette gần trùng, xem 9.4.
- [ ] `mango` s05 / `rambutan` s05 — chấp nhận species-specific reason hay đưa vào regen queue.
- [ ] `lotus` s05 — đã nằm trong queue mục 6 từ trước.

### Ghi chú vận hành cho session sau
Bridge Claude-in-Chrome hỏng lại ngày 2026-09-05: `~/.claude/chrome/chrome-native-host` bị sinh lại
với đường dẫn pin version (`2.1.250`) trong khi CLI đã là `2.1.261` → `pgrep -fl chrome-native-host`
rỗng. Đã repoint về `/opt/homebrew/bin/claude --chrome-native-host` (backup `.bak.2.1.250`).
**Kiểm tra dòng exec của wrapper trước mỗi lần chạy pipeline asset.**

Session Claude Code chỉ có browser tool khi được khởi động với cờ `--chrome` (hoặc bật
"Enabled by default" qua `/chrome`) — không tự bật được giữa session. Theo docs
`code.claude.com/docs/en/chrome`: dùng `/chrome` để xem trạng thái và "Reconnect extension";
chỉ cần restart Chrome khi file cấu hình native messaging host mới được tạo lần đầu.

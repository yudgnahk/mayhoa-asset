# Mayhoa — Farm Missing Asset Plan

**Trạng thái:** Sẵn sàng generate
**Ngôn ngữ:** Tiếng Việt · [English](FARM_MISSING_ASSET_PLAN.en.md)
**Ngày kiểm kê:** 2026-09-08

## Trạng thái và quan hệ với tài liệu khác

Tài liệu này liệt kê **những asset còn thiếu để game chạy được**, đối chiếu giữa `masters/` hiện có và yêu cầu Gate A / Gate B trong repo `mayhoa` (`FARM-V1-SPEC.md` §3, `FARM-CONTENT.md` §1, `FARM-DEMO-BRIEF.md` §4).

Khác với các tài liệu sẵn có ở đây:

- `FARM_ASSET_GENERATION_PLAN.vi.md` liệt kê asset theo **phân loại nghệ thuật** (soil, crops, trees, weeds, pests, tools). Tài liệu này liệt kê theo **thứ đang chặn gameplay**.
- `FARM_REGENERATION_PROMPTS.vi.md` xử lý asset **đã có nhưng chưa đạt**. Tài liệu này xử lý asset **chưa tồn tại**.
- `FARM_REMAINING_PLANT_ASSET_PLAN.vi.md` đã hoàn tất phần cây; tài liệu này tiếp nối cho phần không phải cây.

Đây là tài liệu tạm: xoá khi mọi mục P0 và P1 đã xong.

---

## 1. Kết luận kiểm kê

107 master PNG đã sản xuất, **toàn bộ là cây và ô đất**. Không có một asset nào thuộc nhóm môi trường, UI, hiệu ứng, sinh vật gây hại hay công cụ.

Gate A cần khoảng 21 file trong số 107 file đã làm. **80% công sản xuất tới nay nằm ngoài thứ đang chặn đường.** Tỷ lệ này **xấu đi** so với lần kiểm kê 08/09 (79%/102 file) vì pack `durian` merge ngày 09/09 lại là cây. Đây là biểu hiện bằng số của xung đột `C-ART-02`.

| Nhóm | Trạng thái | Gate cần | Đã có spec? |
|---|---|---|---|
| Soil 6 state | ✅ Xong | A | — |
| Crop D-008 (rice, corn, carrot) | ✅ Xong | A | — |
| `carrot` stage-05 | ⚠️ Đạt geometry, **hỏng gameplay** | A | ✅ `FARM_REGENERATION_PROMPTS.vi.md` §B |
| **Pest** | ❌ Chưa có | **A** | Có danh sách (Phase 10), thiếu spec chi tiết |
| **Tool** | ❌ Chưa có | **A** | Có danh sách (Phase 11), thiếu spec chi tiết |
| **Farm scene / environment** | ❌ Chưa có | **A** | ❌ **không có trong taxonomy** |
| **Plot overlay** | ❌ Chưa có | **A** | ❌ không có |
| **Interaction FX** | ❌ Chưa có | **A** | ❌ không có |
| **Icon inventory** | ❌ Chưa có | **A** | ❌ không có |
| **Water surface / aquatic tile** | ❌ Chưa có | phụ thuộc scope | ❌ §6.2 nói "hệ riêng" nhưng hệ đó chưa tồn tại |
| **Building + UI kinh tế** | ❌ Chưa có | B | ❌ không có |
| Weed | ❌ Chưa có | không bắt buộc | Có danh sách (Phase 9) |

**Năm nhóm không nằm trong taxonomy §2 của generation plan:** environment/scene, water system, UI icon, interaction FX, building. Taxonomy hiện chỉ có `soil / crops / aquatic-crops / trees / weeds / pests / tools`. Cần mở rộng taxonomy trước khi generate các nhóm này.

---

## 2. P0 — Chặn nghiệm thu Gate A

### P0-1 · `carrot` stage-05

Đã nằm trong queue regenerate nhưng **bị xếp nhầm mức "polish"**. Thực tế nó chặn tiêu chí nghiệm thu ở `FARM-DEMO-BRIEF.md` §5: *"người chơi phân biệt được cây đã chín ở zoom thường"*. Cà rốt là `crop_tutorial`, cây đầu tiên người chơi gặp; tín hiệu chín hiện chỉ ~10px ở display size. Spec sẵn ở `FARM_REGENERATION_PROMPTS.vi.md` mục B.

### P0-2 · Pest pack

Gate A yêu cầu **đúng một loại pest** (`FARM-CONTENT.md` §1, `FARM-V1-SPEC.md` §3 verb "pest handling"). Phase 10 liệt kê 6 biến thể — **quá nhiều cho Gate A**. Chỉ cần 1 loại để mở khoá gate.

| Yêu cầu | Giá trị |
|---|---|
| Ưu tiên | `caterpillar_single` — đọc rõ nhất ở size nhỏ, hợp mọi tán lá |
| Canvas master | `512×512` trong suốt, cùng camera angle và ánh sáng trên-trái |
| Anchor | overlay bám tán lá, **không** bám gốc — không dùng anchor crop |
| Số state | tối thiểu 2: `idle` và `cleared`/biến mất |
| Điều kiện nghiệm thu | đọc rõ ở cell `192px` khi chồng lên rice (tán cao), carrot (rosette thấp) và corn (thân đứng); không che mất tín hiệu stage của cây |
| Ràng buộc | không bake cây vào sprite pest; không bake pest vào master cây |

5 biến thể còn lại của Phase 10 giữ nguyên cho sau Gate A.

### P0-3 · Tool pack

Gate A cần tối thiểu UI công cụ (`FARM-DEMO-BRIEF.md` §4). Phase 11 liệt kê 5 tool; Gate A chỉ dùng 5 hành động: till, plant, water, pest, harvest.

| Tool | Bắt buộc Gate A? |
|---|---|
| `watering_can` | ✅ hành động water |
| `harvest_hand` | ✅ hành động harvest |
| `pest_catcher` | ✅ hành động pest |
| `hoe` / dụng cụ xới | ✅ hành động till — **thiếu trong Phase 11**, danh sách hiện có `shovel` nhưng không có dụng cụ xới luống |
| `pruning_shears` | ❌ để sau |

Tool đánh giá ở **UI interaction size**, không đánh giá bằng world scale. Cần bản `idle` và bản `selected`/active cho mỗi tool để `FARM-INTERACTION.md` §4 hiển thị được công cụ đang chọn.

---

## 3. P1 — Cần cho Gate A, chưa có spec

### P1-1 · Farm scene / environment

**Đây là lỗ hổng lớn nhất và chưa ai ghi nhận.** `FARM-V1-SPEC.md` §3 yêu cầu *"one Farm scene"*, D-010 chốt ruộng **35 ô xếp chéo 7×5**. Hiện chỉ có một tile đất lặp lại, không có gì để 35 ô đó trông như một cái ruộng.

Cần tối thiểu:

- nền đất/cỏ ngoài vùng canh tác, tile được, không lộ đường lặp;
- ranh thửa hoặc bờ ruộng phân định vùng 7×5;
- ít nhất một lớp bao quanh để khung hình có điểm dừng, không phải ô trôi trong khoảng trống;
- giữ đúng camera angle và ánh sáng trên-trái của toàn bộ pack.

Chưa cần: nhà cửa, hàng rào trang trí, thời tiết, ngày đêm.

### P1-2 · Plot overlay

`FARM-CONTENT.md` §1 yêu cầu *"crop-compatible plot overlays"*. Cần lớp phủ trạng thái ô độc lập với sprite cây: ô đang chọn, ô hợp lệ khi kéo batch, ô không hợp lệ. `FARM-INTERACTION.md` §4 quy định phản hồi mục tiêu sai phải bằng hình khối và màu, **không mở modal**.

### P1-3 · Interaction FX

`FARM-INTERACTION.md` §3 quy định phản hồi bắt buộc cho từng hành động:

| Hành động | FX cần |
|---|---|
| Till | đất vỡ, sẫm lại, đổi hình mép — có thể xử bằng chuyển state soil |
| Water | vòng cung nước / splash, rồi chuyển sang state đất ẩm |
| Harvest | cây phản ứng, số vật phẩm tăng |
| Pest | sâu rời đi, tán lá ổn định lại |

Ràng buộc quan trọng ở `FARM-INTERACTION.md` §5: cây chín **không được** báo bằng icon nổi trên mọi ô. Tín hiệu chín phải nằm trong chính artwork của cây. Đây cũng là lý do P0-1 là chặn nghiệm thu chứ không phải polish.

### P1-4 · Icon inventory

Cần icon vật phẩm ở size UI, tách khỏi world sprite: 3 nông sản thu hoạch (gạo, bắp, cà rốt), 3 hạt giống tương ứng. Gate A có kho tối thiểu; số lượng và loại đầy đủ thuộc Gate B.

---

## 4. P2 — Gate B, chưa có gì

`FARM-V1-SPEC.md` §3 Gate B cần: kho chung, **một** nhà chế biến, hàng đợi sản xuất, tối đa 3 hàng chế biến, một bảng đơn hàng, tiền xu và tiến trình, mở rộng ô đất.

Chưa có asset nào cho nhóm này. Chưa cần spec chi tiết cho tới khi Gate A qua, nhưng cần biết trước để không lặp lại tình trạng làm thừa: **đừng generate thêm loài cây mới trước khi nhóm này có mặt.**

---

## 5. Water surface — quyết định còn treo

`FARM_ASSET_GENERATION_PLAN.vi.md` §6.2 quy định water surface, bờ ao và ripple FX *"thuộc hệ environment/water riêng"*. **Hệ đó chưa tồn tại**: không có trong taxonomy §2, không có phase nào, không có file nào.

Hệ quả: 15 master aquatic đã làm xong nhưng **chưa thể đặt vào game** vì không có mặt nước để đặt lên. Mức ưu tiên phụ thuộc việc repo `mayhoa` có đưa cây thủy sinh vào scope Farm V1 hay không.

---

## 6. Thứ tự đề xuất

```text
P0-1 carrot s05      → mở khoá tiêu chí nghiệm thu
P0-2 pest ×1         → mở khoá verb pest handling
P0-3 tool ×4         → mở khoá UI công cụ
P1-1 farm scene      → mở khoá "one Farm scene"
P1-2 plot overlay    → mở khoá phản hồi chọn/batch
P1-3 interaction FX  → mở khoá tiêu chí phản hồi tức thì
P1-4 icon inventory  → mở khoá kho tối thiểu
────────────── Gate A đủ asset ──────────────
P2   building + UI kinh tế
     water system (nếu aquatic vào scope)
     weed, 5 pest còn lại, 1 tool còn lại
```

Thứ tự này **thay thế** §17 của generation plan cho tới khi Gate A qua. Việc áp dụng nó chính là cách đóng `C-ART-02` đang OPEN bên repo `mayhoa`.

---

## 7. Những thứ KHÔNG thiếu

Ghi lại để không ai làm lại:

- 6 field crop × 5 stage, đã đóng atlas, anchor `(0.5, 0.89453125)`;
- **11 tree × 5 stage**, atlas cell `256×256`, **đã đóng atlas** — `durian` (tree thứ 11) đã normalize và vào atlas ngày 2026-09-10 (xem `ASSET_GEOMETRY_FIX_CHECKLIST.vi.md` mục 10); còn treo duy nhất một việc nội dung: quả stage-05 chìm trong tán, phải generate lại;
- 3 aquatic × 5 stage;
- 6 soil state, RGBA8, `soil_tilled` dùng bản `v02`;
- pipeline atlas tái tạo được bằng `tools/build_atlas.py`, 42 test, idempotent, có guard fail-loud khi master lệch chuẩn;
- geometry contract đã khoá và đã đồng bộ hai repo.

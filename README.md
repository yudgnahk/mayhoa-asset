# Mayhoa Asset

**Project:** Mayhoa — art production repo cho hệ Farm
**Phong cách:** Mayhoa Nostalgic Hand-Painted Farm Sprite
**Ngôn ngữ tài liệu:** Tiếng Việt. Các bản dịch `.en.md` đã được gỡ ngày 2026-09-07 vì là bản sao đi sau bản `.vi`; lấy lại từ lịch sử Git nếu cần.

Repo này là nơi sản xuất artwork (master art + runtime atlas) cho game Mayhoa: art style, kế hoạch generate, hình học/anchor và toàn bộ file PNG master nằm ở đây. Repo này **không** quyết định gameplay — mọi phạm vi, roster crop, gate demo và cơ chế chơi thuộc về repo song sinh `mayhoa` (product/docs). Theo quyết định **D-012** của `mayhoa`, repo đó chỉ ghi lại (a) game cần asset đại diện cho state gì và (b) integration contract mà demo phải tuân theo; mọi quyết định về art direction, prompt generation, master artwork, normalize hình học và đóng atlas thuộc về repo này. Game hiện đang ở **giai đoạn Farm-only** — chỉ roster crop D-008 (lúa, bắp, cà rốt) và hệ soil/pest/tool tối thiểu của Gate A là có liên quan gameplay ngay bây giờ; các species khác (cây ăn quả, thủy sinh) nằm ngoài scope Farm V1 dù artwork đã tồn tại.

---

## 1. Tài liệu ở root

| Tài liệu | Mục đích | Trạng thái |
|---|---|---|
| `FARM_ASSET_GENERATION_PLAN.vi.md` | Roadmap sản xuất: asset taxonomy, growth-stage system, size system, 12 production phase và thứ tự thực thi | Active cho taxonomy/roadmap/thứ tự phase; bảng canvas/anchor cụ thể (§5) đã bị geometry spec ghi đè — xem header trong file |
| `MAYHOA_ART_STYLE_SPEC.vi.md` | Spec phong cách nghệ thuật chuẩn (silhouette, outline, màu, shading, prompting rules) cho mọi asset | Canonical, active |
| `MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.vi.md` | Nguồn sự thật duy nhất cho canvas size, anchor, scale progression, alpha/QC hình học | **Canonical, ưu tiên cao nhất** khi có mâu thuẫn hình học với bất kỳ tài liệu nào khác (kể cả plan/style spec) |
| `ASSET_GEOMETRY_FIX_CHECKLIST.vi.md` | Nhật ký thực thi đợt normalize hình học toàn bộ `masters/` ngày 2026-08-26 | Đã thực thi xong phần chính; còn vài mục chờ (runtime metadata + verify cuối) — xem header trong file |
| `FARM_REGENERATION_PROMPTS.vi.md` | Prompt cụ thể cho đợt regenerate đầu tiên: soil_tilled hỏng, carrot stage-05, cả pack thien-ly, lotus stage-05, 6 fruit tree | Đang chờ generate (đợt 1), phát sinh từ checklist ở trên |
| `FARM_REMAINING_PLANT_ASSET_PLAN.vi.md` | Phân task generate 7 species cây/thủy sinh còn thiếu (coconut, dragon-fruit, coffee, rubber, lotus, water-mimosa, water-spinach) cho nhiều sub-agent song song | Sản xuất đã xong trên thực tế (`masters/` đủ 5/5 file mỗi species) — checklist chi tiết trong file chưa được tick hết, xem header trong file |

Trước đây repo duy trì song song bản `.en.md` cho generation plan, art style spec và hai README trong `masters/farm/`. Các bản này đã được gỡ ngày 2026-09-07: chúng là bản dịch đi sau bản `.vi` và việc duy trì song ngữ không có người đọc. **Tiếng Việt là ngôn ngữ canonical duy nhất.** Nội dung cũ vẫn lấy lại được từ lịch sử Git.

---

## 2. Trạng thái sản xuất hiện tại

**Đã hoàn tất** — 101 master PNG, đủ 5 growth stage mỗi species (trừ soil không có stage):

- **Soil** — 6 trạng thái (`empty`, `tilled`, `wet`, `planted`, `dry`, `harvested`). ⚠️ `soil_tilled_v01.png` hiện **hỏng dữ liệu** (IDAT stream corrupt, không decode được) — nằm trong hàng chờ regenerate ở `FARM_REGENERATION_PROMPTS.vi.md`.
- **Field crops** (6 species × 5 stage) — rice, corn, carrot, thien-ly, ngo-gai, mint.
- **Fruit/perennial trees** (10 species × 5 stage) — mango, pomelo, lemon, star-apple, rambutan, lychee, coconut, dragon-fruit, coffee, rubber.
- **Aquatic crops** (3 species × 5 stage) — lotus, water-mimosa, water-spinach.

**Chưa làm:**

- **Weeds** — chưa generate (Phase 9 của generation plan).
- **Pests** — chưa generate (Phase 10).
- **Tools** — chưa generate (Phase 11).

**Đang chờ regenerate** (chất lượng/geometry chưa đạt, xem `FARM_REGENERATION_PROMPTS.vi.md`): `soil_tilled`, `carrot` stage-05, toàn bộ pack `thien-ly` (chuyển sang dạng leo giàn), `lotus` stage-05, và cả 6 fruit tree pack (silhouette hiện chưa phân biệt rõ loài).

> ### ⚠️ Lưu ý quan trọng — `C-ART-02`
>
> Gate A của bản demo chơi được (`mayhoa` repo) **cần ít nhất một pest và một tool UI** để hoàn chỉnh vòng lặp gameplay. Nhưng theo thứ tự thực thi hiện tại của `FARM_ASSET_GENERATION_PLAN.vi.md` §17, pest (Phase 10) và tool (Phase 11) được xếp **cuối cùng**, sau cả các pack tree/aquatic (Phase 4–8) mà Farm V1 chưa dùng tới. Xung đột này được `mayhoa` repo theo dõi dưới mã **`C-ART-02`** (`docs/research/CONTRADICTIONS.md`), hiện **OPEN**. Ai đổi thứ tự production nên biết việc này trước khi ưu tiên thêm tree/aquatic species mới.

---

## 3. Geometry contract đã khóa (tóm tắt)

Bảng dưới trích từ `MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.vi.md` — xem file đó để biết đầy đủ audit/QC. Đây cũng là contract mà repo `mayhoa` đọc (xem `FARM-CONTENT.md` §1 bên đó); **không bên nào được đổi các số này một mình.**

| Thuộc tính | Giá trị |
|---|---|
| Runtime atlas cell | `192×192` px @1x |
| Crop master canvas | `512×512`, transparent |
| Crop placement anchor | `(0.5, 0.89453125)` — điểm tiếp đất của gốc cây, không phải tâm tán lá |
| Tree master canvas | `1024×1024` |
| Tree placement anchor | `(0.5, 0.947265625)` |
| Điểm ghim trên tile (plant attachment point) | tâm soil plate, `(0.5, 0.508)` trong hệ tọa độ soil-cell |
| Growth stages | 5 stage / species |

**Anchor crop đã đổi ngày 2026-08-26**, từ `(0.5, 0.684)` sang `(0.5, 0.89453125)`. Code hoặc runtime metadata nào còn dùng giá trị cũ sẽ khiến crop bị "nổi" phía trên ô đất thay vì đứng giữa plate.

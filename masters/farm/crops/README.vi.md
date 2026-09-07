# Phase 2 crop cốt lõi và Phase 3 herb / low crop

**Trạng thái:** Reference growth-stage chuẩn của Phase 2 và Phase 3<br>
**Project:** Mayhoa<br>
**Phong cách:** Mayhoa Nostalgic Hand-Painted Farm Sprite

Thư mục này chứa master của 5 giai đoạn phát triển cho lúa, bắp và cà rốt ở Phase 2, cùng thiên lý, ngò gai và bạc hà ở Phase 3. Mỗi crop có silhouette phát triển khác nhau về cấu trúc, không lấy một hình rồi chỉ scale lớn dần.

## Các growth stage

1. `stage-01_seeded`
2. `stage-02_sprout`
3. `stage-03_young`
4. `stage-04_mature`
5. `stage-05_harvestable`

## Crop cốt lõi Phase 2

- `rice/` — mầm nhỏ -> bụi cỏ mở rộng -> bụi lúa trưởng thành -> bông vàng rõ ở harvest.
- `corn/` — mầm nhỏ -> lá rộng hơn -> thân có cấu trúc -> tassel -> bắp nhìn rõ ở harvest.
- `carrot/` — mầm nhỏ -> rosette lá -> tán lá xẻ dày hơn -> vai củ nhẹ -> tín hiệu củ cam ở harvest.

## Herb / low crop Phase 3

- `tonkin-jasmine/` — thiên lý / Telosma cordata; dấu hiệu gieo hạt -> mầm dây nhỏ -> dây non nhiều lá -> dây trưởng thành với lá hình tim/bầu dục -> chùm hoa vàng-xanh nhạt tiết chế ở harvest.
- `culantro/` — ngò gai / Eryngium foetidum; mầm -> rosette gốc nhỏ -> rosette non mở rộng -> rosette trưởng thành dày -> rosette harvest xanh tốt với lá dài, hẹp và mép răng cưa gợi rõ. Không dùng dạng lá tơi của ngò rí.
- `mint/` — bạc hà; lá có texture hình bầu dục đến mũi mác mọc theo cặp -> thân phân nhánh -> bụi bạc hà ngày càng dày và xanh tốt, giữ cue mép lá/texture rõ ở gameplay scale.

## Quy tắc production đã khóa

- master canvas trong suốt 512x512;
- crop là sprite bottom-anchor: root `(256, 458)` = `(0.5, 0.89453125)`, engine ghim vào tâm soil plate (thay anchor cũ `(0.5, 0.684)` từ 2026-08-26);
- chân asset căn theo footprint đất của Phase 1;
- ánh sáng từ trên-trái, contact shadow mềm, viền chromatic tối có chọn lọc;
- không bake soil, weed, pest, UI, chữ hay background scene;
- tiến trình stage phải đổi silhouette, mật độ và focal cue;
- nhận diện loài vẫn phải rõ ở runtime cell 192px.

## Runtime atlas

`runtime/1x/farm/crops/farm_crops_v01.png` là shared-texture atlas 960x1152 với cell 192x192, gộp cả 6 crop pack (Phase 2 + Phase 3) vào một texture: 6 species x 5 stage = 30 frame. `runtime/farm_crops_v01.json` chứa frame coordinates, anchor từng frame và `stageNames`.

- Hàng theo thứ tự alphabet: carrot, corn, culantro, mint, rice, tonkin-jasmine. Cột theo `stageOrder` = `stage-01`..`stage-05`.
- Frame key là **slot id** `<species>_stage-0N` (ví dụ `culantro_stage-04`), không mang nhãn semantic — game dựng key thẳng từ species + stage index, không phải tra bảng. Nhãn semantic nằm trong `stageNames` (`<species> -> ["seeded","sprout",...]`) và chỉ dùng để hiển thị.
- Anchor đồng nhất `(0.5, 0.894531)` cho cả 30 frame (`anchorUniform: true`), khớp root master `(256, 458)`. `anchor.x` luôn = 0.5 vì mọi master đã được căn tâm canvas — **không** đo bottom-band centroid để suy ra anchorX (heuristic đó sai với morphology rosette, xem spec §7.1).
- `masterCanvas` = 512x512 cho toàn atlas.

Atlas này thay cho `core_crops_v01` + `herb_crops_v01` (đã xoá khỏi repo). Atlas là **sản phẩm sinh ra từ masters, không sửa tay** — build lại bằng:

```bash
python3 tools/build_atlas.py --atlas farm_crops_v01   # thêm --dry-run để xem trước
```

Chạy `python3 tools/build_atlas.py` không tham số để dựng lại cả 4 atlas (`farm_crops_v01`, `farm_trees_v01`, `farm_aquatic_v01`, `farm_soil_v01`). Script idempotent: chạy 2 lần ra byte y hệt nhau.

## Artwork và production pipeline

Phase 2 từng dùng workflow deterministic bằng Pillow. Chi tiết này chỉ được giữ như provenance lịch sử của Phase 2 và không phải quy tắc authoring cho Phase 3 hay các asset pack được vẽ/generate về sau.

Source art Phase 3 là artwork bitmap được vẽ/sinh thật bằng hệ thống imagegen tích hợp. Pillow, sips, ImageMagick và công cụ raster tương tự chỉ được phép dùng cho production không sáng tác artwork, như downsample theo tỉ lệ, đóng atlas, kiểm tra metadata/alpha, tạo contact sheet và QC. Không được dùng chúng để vẽ, tổng hợp, thêm hoặc đổi hình cây.

## Điều kiện nghiệm thu

Mỗi pack được khóa khi cả 15 frame: (1) phân biệt rõ ở gameplay size, (2) đặt hợp lý trên footprint farm chung, (3) giữ progression và relative scale nhất quán giữa các crop, và (4) harvestable đọc rõ hơn nhưng không glossy/neon.

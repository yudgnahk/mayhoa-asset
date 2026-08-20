# Phase 2 - Bộ crop cốt lõi

**Trạng thái:** Reference growth-stage chuẩn của Phase 2  
**Project:** Mayhoa  
**Phong cách:** Mayhoa Nostalgic Hand-Painted Farm Sprite

Thư mục này chứa master của 5 giai đoạn phát triển cho lúa, bắp và cà rốt. Mỗi stage thay đổi silhouette thật sự, không lấy một hình rồi chỉ scale lớn dần.

## Các growth stage

1. `stage-01_seeded`
2. `stage-02_sprout`
3. `stage-03_young`
4. `stage-04_mature`
5. `stage-05_harvestable`

## Crop chuẩn

- `rice/` — mầm nhỏ -> bụi cỏ mở rộng -> bụi lúa trưởng thành -> bông vàng rõ ở harvest.
- `corn/` — mầm nhỏ -> lá rộng hơn -> thân có cấu trúc -> tassel -> bắp nhìn rõ ở harvest.
- `carrot/` — mầm nhỏ -> rosette lá -> tán lá xẻ dày hơn -> vai củ nhẹ -> tín hiệu củ cam ở harvest.

## Quy tắc production đã khóa

- master canvas trong suốt 512x512;
- placement anchor chung khoảng `(0.5, 0.684)`;
- chân asset căn theo footprint đất của Phase 1;
- ánh sáng từ trên-trái, contact shadow mềm, viền chromatic tối có chọn lọc;
- không bake soil, weed, pest, UI, chữ hay background scene;
- tiến trình stage phải đổi silhouette, mật độ và focal cue;
- nhận diện loài vẫn phải rõ ở runtime cell 192px.

## Runtime atlas

`runtime/1x/farm/crops/core_crops_v01.png` là shared-texture atlas 960x576 với cell 192x192. `runtime/core_crops_v01.json` chứa frame coordinates và placement anchor chung. Các hàng lần lượt là rice, corn, carrot; các cột theo thứ tự 5 stage ở trên.

## Sinh asset có thể tái lập

Chạy `python scripts/generate_phase2_core_crops.py --root .` với Pillow 11.3.0 để tái tạo có tính quyết định 15 master, runtime atlas và manifest.

## Điều kiện kết thúc Phase 2

Phase 2 được khóa khi cả 15 frame: (1) phân biệt rõ ở gameplay size, (2) đặt hợp lý trên reference `soil_tilled` của Phase 1, (3) giữ relative scale nhất quán giữa các crop, và (4) harvestable đọc rõ hơn nhưng không glossy/neon.

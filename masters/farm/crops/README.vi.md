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

- `thien-ly/` — thiên lý / Telosma cordata; dấu hiệu gieo hạt -> mầm dây nhỏ -> dây non nhiều lá -> dây trưởng thành với lá hình tim/bầu dục -> chùm hoa vàng-xanh nhạt tiết chế ở harvest.
- `ngo-gai/` — ngò gai / Eryngium foetidum; mầm -> rosette gốc nhỏ -> rosette non mở rộng -> rosette trưởng thành dày -> rosette harvest xanh tốt với lá dài, hẹp và mép răng cưa gợi rõ. Không dùng dạng lá tơi của ngò rí.
- `mint/` — bạc hà; lá có texture hình bầu dục đến mũi mác mọc theo cặp -> thân phân nhánh -> bụi bạc hà ngày càng dày và xanh tốt, giữ cue mép lá/texture rõ ở gameplay scale.

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

`runtime/1x/farm/crops/herb_crops_v01.png` là atlas Phase 3 tương ứng, kích thước 960x576. `runtime/herb_crops_v01.json` chứa frame coordinates và placement anchor chung. Các hàng lần lượt là thien-ly, ngo-gai, mint; các cột theo cùng thứ tự 5 stage.

## Artwork và production pipeline

Phase 2 từng dùng workflow deterministic bằng Pillow. Chi tiết này chỉ được giữ như provenance lịch sử của Phase 2 và không phải quy tắc authoring cho Phase 3 hay các asset pack được vẽ/generate về sau.

Source art Phase 3 là artwork bitmap được vẽ/sinh thật bằng hệ thống imagegen tích hợp. Pillow, sips, ImageMagick và công cụ raster tương tự chỉ được phép dùng cho production không sáng tác artwork, như downsample theo tỉ lệ, đóng atlas, kiểm tra metadata/alpha, tạo contact sheet và QC. Không được dùng chúng để vẽ, tổng hợp, thêm hoặc đổi hình cây.

## Điều kiện nghiệm thu

Mỗi pack được khóa khi cả 15 frame: (1) phân biệt rõ ở gameplay size, (2) đặt hợp lý trên footprint farm chung, (3) giữ progression và relative scale nhất quán giữa các crop, và (4) harvestable đọc rõ hơn nhưng không glossy/neon.

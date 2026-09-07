# Phase 1 - Nền tảng đất trồng

**Trạng thái:** Reference đất chuẩn của Phase 1  
**Project:** Mayhoa  
**Phong cách:** Mayhoa Nostalgic Hand-Painted Farm Sprite

Thư mục này chứa bộ trạng thái đất chuẩn dùng làm nền tảng thị giác cho batch farm đầu tiên của Mayhoa.

## Các master state chuẩn

- `soil_empty_v01.png`
- `soil_tilled_v01.png` (IDAT hỏng vĩnh viễn — giữ lại chỉ để đối chiếu lịch sử) và `soil_tilled_v02.png` (canonical, 2026-09-05)
- `soil_wet_v01.png`
- `soil_planted_v01.png`
- `soil_dry_v01.png`
- `soil_harvested_v01.png`

Cả sáu master dùng canvas trong suốt 512x512, cùng góc camera, footprint, tâm đặt asset và logic bóng tiếp đất. Footprint xấp xỉ: x 88-424, y 163-355; tâm placement khoảng (256, 268).

## Ý nghĩa từng state

- `empty`: đất chưa xử lý, bề mặt tương đối phẳng và ít xáo trộn.
- `tilled`: pattern luống chuẩn, là reference chính để đặt crop.
- `wet`: đất ẩm tối hơn, phản sáng mềm rất tiết chế, không bóng.
- `planted`: đất đã xới với dấu lỗ gieo/hạt nhẹ; crop vẫn là overlay riêng.
- `dry`: đất sáng và khô hơn, có một ít vết nứt hữu cơ.
- `harvested`: đất sau thu hoạch với dấu xáo trộn và gốc rạ rất nhẹ.

## Quy tắc render được khóa

- viền nâu/chromatic tối có chọn lọc, không dùng đen thuần;
- ánh sáng nhẹ từ góc trên-trái và bóng tiếp đất mềm;
- bảng màu nâu ấm, hoài niệm, số tone giới hạn;
- texture painterly mềm, tránh glossy/vector-clean;
- không bake crop, weed, pest, UI hay background scene;
- nền trong suốt và geometry placement giống nhau giữa mọi state.

## Runtime atlas

Với PixiJS, soil dùng shared-texture atlas 1x:

- `runtime/1x/farm/soil/farm_soil_v01.png` - 576x384, sáu cell 192x192.
- `runtime/farm_soil_v01.json` - tọa độ frame + anchor từng frame.

Thứ tự frame theo alphabet: hàng trên `soil_dry`, `soil_empty`, `soil_harvested`; hàng dưới `soil_planted`, `soil_tilled`, `soil_wet`. Frame key ở đây là **full stem** của tile (`soil_dry`, `soil_tilled`...) — soil là ngoại lệ duy nhất, các atlas có stage đều dùng slot id `<species>_stage-0N`.

Anchor `x` luôn = 0.5; anchor `y` đo từng file nên không đồng nhất tuyệt đối: 0.701172 (`soil_empty`) đến 0.703125 (5 tile còn lại), `placementAnchor` đại diện là `(0.5, 0.703125)` kèm `anchorUniform: false`. `masterCanvas` = 512x512, tiếp tục là nguồn để xuất 2x/high-DPI về sau thay vì ship master quá lớn trực tiếp vào gameplay.

Ô `soil_tilled` lấy từ `soil_tilled_v02.png`: script luôn chọn version cao nhất **đọc được**, và `v01` thì hỏng IDAT vĩnh viễn.

Atlas này thay cho `soil_states_v01` (đã xoá khỏi repo). Atlas là **sản phẩm sinh ra từ masters, không sửa tay** — build lại bằng:

```bash
python3 tools/build_atlas.py --atlas farm_soil_v01   # thêm --dry-run để xem trước
```

Chạy `python3 tools/build_atlas.py` không tham số để dựng lại cả 4 atlas (`farm_crops_v01`, `farm_trees_v01`, `farm_aquatic_v01`, `farm_soil_v01`). Script idempotent: chạy 2 lần ra byte y hệt nhau.

## Điều kiện kết thúc Phase 1

Phase 1 được khóa khi cả sáu state vẫn phân biệt rõ ở runtime size nhưng giữ nguyên footprint và perspective. Phase 2 phải composite/review growth stage của crop trước hết trên `soil_tilled_v02.png`, sau đó spot-check thêm trên wet, dry và planted.

# Phase 1 - Nền tảng đất trồng

**Trạng thái:** Reference đất chuẩn của Phase 1  
**Project:** Mayhoa  
**Phong cách:** Mayhoa Nostalgic Hand-Painted Farm Sprite

Thư mục này chứa bộ trạng thái đất chuẩn dùng làm nền tảng thị giác cho batch farm đầu tiên của Mayhoa.

## Các master state chuẩn

- `soil_empty_v01.png`
- `soil_tilled_v01.png`
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

Với PixiJS, Phase 1 gồm shared-texture atlas 1x:

- `runtime/1x/farm/soil/soil_states_v01.png` - 576x384, sáu cell 192x192.
- `runtime/soil_states_v01.json` - tọa độ frame.

Thứ tự frame: hàng trên `empty`, `tilled`, `wet`; hàng dưới `planted`, `dry`, `harvested`. Master 512x512 tiếp tục là nguồn để xuất 2x/high-DPI về sau, thay vì ship master quá lớn trực tiếp vào gameplay.

## Điều kiện kết thúc Phase 1

Phase 1 được khóa khi cả sáu state vẫn phân biệt rõ ở runtime size nhưng giữ nguyên footprint và perspective. Phase 2 phải composite/review growth stage của crop trước hết trên `soil_tilled_v01.png`, sau đó spot-check thêm trên wet, dry và planted.

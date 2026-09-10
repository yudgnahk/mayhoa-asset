# Mayhoa — Gate A: Pest + Tool prompt spec

**Trạng thái:** Pha A (prompt) — chốt trước khi generate
**Nguồn queue:** `.ai-bridge/GATE_A_GEN_BRIEF.md`, `FARM_MISSING_ASSET_PLAN.vi.md` §P0-2 / §P0-3
**Specs liên quan:** `MAYHOA_ART_STYLE_SPEC.vi.md`, `MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.vi.md`

`FARM_MISSING_ASSET_PLAN.vi.md` ghi pest và tool là "có danh sách, thiếu spec chi tiết".
Đây là spec đó. Tài liệu này chỉ phủ **10 file Gate A**; 5 pest và 1 tool còn lại của
Phase 10/11 để sau.

---

## 1. Bảng output

| # | Asset | File | Canvas |
|---|---|---|---:|
| 1 | pest present | `masters/farm/pests/pest_caterpillar-single_present_v01.png` | 512 |
| 2 | pest cleared | `masters/farm/pests/pest_caterpillar-single_cleared_v01.png` | 512 |
| 3 | hoe idle | `masters/farm/tools/tool_hoe_idle_v01.png` | 512 |
| 4 | hoe selected | `masters/farm/tools/tool_hoe_selected_v01.png` | 512 |
| 5 | watering can idle | `masters/farm/tools/tool_watering-can_idle_v01.png` | 512 |
| 6 | watering can selected | `masters/farm/tools/tool_watering-can_selected_v01.png` | 512 |
| 7 | pest catcher idle | `masters/farm/tools/tool_pest-catcher_idle_v01.png` | 512 |
| 8 | pest catcher selected | `masters/farm/tools/tool_pest-catcher_selected_v01.png` | 512 |
| 9 | harvest hand idle | `masters/farm/tools/tool_harvest-hand_idle_v01.png` | 512 |
| 10 | harvest hand selected | `masters/farm/tools/tool_harvest-hand_selected_v01.png` | 512 |

Tên theo pattern `<asset>_<state>_v<nn>.png` của generation plan §11 (`tool_watering-can_idle_v01.png`).

---

## 2. Quyết định chốt trong pha A

**`hoe` là dụng cụ xới thật, không map tạm sang `shovel`.** Phase 11 thiếu hoe;
brief cho phép map tạm nhưng không cần — lưỡi bẹt vuông góc cán là silhouette
riêng, phân biệt được với xẻng ở UI size. Phase 11 nên bổ sung `hoe` vào danh sách.

**`selected` = cùng object, cùng pose, cùng silhouette — chỉ đổi rendering.**
Rim light vàng ấm + glow nhẹ + saturation cao hơn. Không đổi góc, không đổi tư thế,
không thêm hiệu ứng nước/đất. Lý do: `FARM-INTERACTION.md` §4 cần hiển thị *công cụ
đang chọn* trong thanh công cụ; nếu silhouette đổi theo state thì icon nhảy khi
người chơi bấm. Đây cũng là lý do không dùng pose "đang tưới" cho `watering_can_selected`.

**`cleared` không phải sprite rỗng.** Vẽ một puff bụi mềm + con sâu cuộn tròn bị
hất ra, nhỏ hơn ~55%. `FARM-INTERACTION.md` §3 quy định phản hồi pest là *"sâu rời
đi"* — một khung tĩnh đọc được ý đó cần thấy con sâu đang rời, không phải khoảng trống.

**Anchor pest = pivot giữa canvas `(0.5, 0.5)`, không phải root contact.**
`MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.vi.md` §5.5 cho phép: pest là overlay bám
tán lá, game gắn vào foliage attach point của từng loài, nên sprite không có
world-contact semantic. Tool cũng dùng `(0.5, 0.5)` — visual pivot theo §5.5.

**Không contact shadow cho tool.** Shared Style Block cho phép "very small soft
contact shadow" vì asset thường đứng trên đất. Tool là UI icon nổi trong thanh
công cụ, bóng đổ dưới đáy làm icon trông như đang đặt trên mặt phẳng vô hình.

---

## 3. Shared Style Block (paste đầu MỌI prompt)

Giống `FARM_REGENERATION_PROMPTS.vi.md` §2, trừ dòng shadow với tool.

```text
Art style — "Nostalgic Hand-Painted Farm Sprite": a cozy farming-game sprite
inspired by classic 2008–2012 browser/social farm games. Soft painterly
hand-painted rendering with light brush texture; selective soft outlines in
dark green/brown chromatic tones (never pure black, never thick uniform
vector lines); readable silhouette at small gameplay size; cheerful pastel
palette, slightly washed, higher saturation only on focal parts; gentle
shading, light source upper-left; organic asymmetric shapes. NOT
photorealistic, NOT glossy modern mobile art, NOT clean vector/cel-shade,
NOT neon.

Format: single isolated game sprite on a FULLY TRANSPARENT background.
One object only, whole object fully inside frame with margin on all sides.
No ground/soil/scene baked in, no text or watermark, no button or panel
background behind the object.
```

**Negative khi model bướng:** `no background, no soil tile, no scene, no frame, no border, no watermark, no photorealism, no 3D render, no neon colors, no multiple views, no sprite sheet, no UI button behind the object`.

**Reference:** attach `coffee_stage-05_berry_v01.png` làm style anchor duy nhất, kèm
ghi chú rõ *"style only — the object I want is different and much smaller"*.
Không attach soil tile hay master cây làm reference hình học: bẫy đã trả giá ở
`TASK_STATE.vi.md` là reference quyết định hình học output, mà pest/tool không thuộc
nhóm hình học của plate hay của cây.

---

## 4. Pest — `caterpillar_single`

### 4.1 Ràng buộc chung

- Không bake cây, lá, ô đất vào sprite. Không bake pest vào master cây.
- Đọc rõ khi chồng lên rice (tán cao), carrot (rosette thấp), corn (thân đứng) ở cell `192px`.
- Không che tín hiệu stage của cây → khối sâu gọn, không trải ngang.
- Cute/readable, **không** realistic insect horror (generation plan §8).
- Thân **không** được xanh lá thuần: đặt trên tán lá sẽ biến mất. Điểm focal phải là màu ấm.

### 4.2 `present`

```text
A single cute cartoon caterpillar sprite for a farming game, seen from a
slight 3/4 side angle.

Body: a chubby caterpillar made of 6 soft rounded segments, arched upward in
the middle like it is mid-crawl. Body color is a bright lime yellow-green
with slightly darker soft green bands between segments and a few small warm
orange dots along the back. Head is a rounded warm coral-red with two big
friendly cartoon eyes, a tiny smile, and two short soft antennae. Tiny stubby
orange feet under the front segments.

The warm coral head and orange dots are the focal contrast so the creature
stays readable when it sits on top of green foliage. Compact chunky shape,
wider than tall but not stretched into a long thin worm.

Nothing else in the image: no leaf, no branch, no plant, no soil.
```

Nghiệm thu: composite lên rice/carrot/corn ở 192px, sâu vẫn tách khỏi nền lá;
bbox không rộng quá ~55% canvas; không có mảnh lá/cành nào trong alpha.

### 4.3 `cleared`

```text
A "pest cleared" effect sprite for a farming game: the same cute cartoon
caterpillar as before, but now being knocked away.

The caterpillar is curled into a small comma shape, tilted, tumbling up and
to the right, drawn small — roughly half the size it would be at rest. Its
eyes are closed in a harmless dizzy way, still cute, not hurt or gory. Same
lime yellow-green body with a warm coral head.

Below and left of it, a soft pale mint-white cartoon dust puff made of 3–4
rounded overlapping lobes, plus three small four-point sparkles scattered
around. The puff is soft and airy with gentle painterly edges, semi-opaque.

Nothing else: no leaf, no plant, no soil, no impact lines, no text.
```

Nghiệm thu: đọc được là "sâu vừa bị bắt đi"; puff không đặc tới mức che ô đất;
cùng lighting trên-trái với `present`.

---

## 5. Tools — 4 cái × 2 state

### 5.1 Ràng buộc chung

- Gameplay interaction icon, không phải illustration realistic (generation plan §9).
- Silhouette cực rõ, contrast cao hơn world asset một chút.
- 4 tool phải phân biệt được với nhau **chỉ bằng silhouette** ở UI size.
- Không bake button background, không contact shadow.
- Object đặt chéo trong khung, chiếm phần lớn khung.

### 5.2 Suffix `selected` (nối vào cuối prompt idle, giữ nguyên phần còn lại)

```text
State: SELECTED — exactly the same object, same pose, same angle, same
silhouette as the idle version, only lit differently: a warm golden rim light
along the upper-left edges, slightly higher saturation and brightness overall,
and a soft warm glow bleeding just a few pixels outside the object's edge.
Do not change the shape, the pose, the framing, or the size.
```

### 5.3 `hoe`

```text
A farming hoe tool icon sprite for a farming game, seen at a slight 3/4
angle, lying diagonally across the frame with the blade at the lower left
and the handle going up to the upper right.

A wide flat trapezoid steel blade, mounted at a right angle to the end of a
straight wooden handle — clearly a soil-tilling hoe, NOT a shovel and NOT a
pickaxe. The blade is soft warm grey steel with a lightly worn edge and a
hint of dry earth on it; the handle is warm honey-brown wood with a soft
grain and a slightly darker binding collar where blade meets handle.
```

Nghiệm thu: lưỡi vuông góc cán (không thẳng trục như xẻng), một lưỡi bẹt (không nhọn, không hai ngạnh).

### 5.4 `watering_can`

```text
A watering can tool icon sprite for a farming game, seen at a slight 3/4
angle, standing upright and slightly turned, spout pointing to the left.

A rounded chubby metal watering can with a soft pastel mint-teal body, a
large rounded carry handle on top, a second small grip handle at the back,
and a long spout ending in a round sprinkler rose head. A warm cream painted
band runs around the belly of the can. Friendly, plump, storybook proportions.

The can is empty and not pouring: no water, no droplets, no splash.
```

Nghiệm thu: có rose head ở đầu vòi (phân biệt với bình/ấm trà); không có nước.

### 5.5 `pest_catcher`

```text
An insect-catching net tool icon sprite for a farming game, seen at a slight
3/4 angle, lying diagonally with the net hoop at the upper left and the
handle going down to the lower right.

A round hoop of pale gold metal holding a soft pale cream mesh net bag that
hangs down and slightly to the side with a gentle fabric droop; the mesh is
suggested with a light woven texture and is semi-translucent at its edge. A
straight warm honey-brown wooden handle with a small green cloth grip wrap
near the end.

Empty net: no insect, no butterfly, no caterpillar inside or nearby.
```

Nghiệm thu: vòng lưới tròn rỗng, túi lưới rủ mềm; không có côn trùng nào trong khung.

### 5.6 `harvest_hand`

```text
A harvesting glove tool icon sprite for a farming game: a single chunky
cartoon gloved hand seen at a slight 3/4 angle, tilted diagonally, fingers
curled into a soft open picking gesture as if about to pluck a fruit.

A plump rounded farm work glove in warm cream canvas with soft sage-green
accents on the back of the hand and a rolled green cuff at the wrist. Chunky
storybook fingers, no visible fingernails, no skin — it is a glove. The
opening at the wrist is closed off with a soft dark cuff lining, not an arm.

Just the glove: no arm, no crop, no fruit, no basket.
```

Nghiệm thu: là găng tay (không phải bàn tay trần), không có tay/cánh tay nối dài ra khỏi cổ tay, không cầm nông sản.

---

## 6. Pipeline sau khi Save

1. Raw về `.ai-bridge/pests/` hoặc `.ai-bridge/tools/`.
2. `python3 tools/geometry_audit.py` — kiểm canvas, RGBA8, margin.
3. `python3 tools/normalize_pack.py --mode anchor --canvas 512 512 --target 256 256 <file>` — scale quanh pivot giữa.
4. Composite QC: pest chồng lên rice/carrot/corn ở 192px; tool render ở UI size.
5. PASS mới promote sang `masters/farm/pests/` và `masters/farm/tools/`.
6. Cập nhật `TASK_STATE.vi.md` và §5.5 của geometry spec (canonical anchor cho 2 class mới).

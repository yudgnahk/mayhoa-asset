# Mayhoa — Regeneration Specs & Prompts (Đợt 1)

**Ngôn ngữ:** Tiếng Việt · [English](FARM_REGENERATION_PROMPTS.en.md)

**Status:** Sẵn sàng generate
**Nguồn queue:** `ASSET_GEOMETRY_FIX_CHECKLIST.vi.md` mục 6 (visual review 2026-08-26)
**Specs liên quan:** `MAYHOA_ART_STYLE_SPEC.vi.md`, `MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.vi.md`

---

## 1. Workflow

Với **một loài mới, luôn tách làm hai pha — viết prompt trước, generate assets sau.** Không gộp hai pha:
species block là source of truth, và sửa một đoạn prompt rẻ hơn nhiều so với gen lại 5 ảnh.

**Pha A — viết prompt (chưa generate ảnh nào):**

1. Thêm species block cho loài vào mục E–K bên dưới: silhouette đặc trưng, kiểu lá, hoa ở stage-04, quả ở stage-05.
2. Đối chiếu acceptance của nhóm — che quả đi thì silhouette vẫn phải phân biệt được với mọi loài đã có.
3. Commit phần prompt này **trước khi** chạy sang pha B.

**Pha B — generate assets:**

4. Với mỗi ảnh: paste **Shared Style Block + species block + đúng MỘT stage line** vào ChatGPT (kèm ảnh reference được ghi chú). Một prompt = một ảnh.
5. Tải PNG về, đặt tên đúng convention trong bảng, bỏ vào đúng thư mục `masters/`.
6. Báo Claude → pipeline tự chạy: `geometry_audit.py` → `normalize_pack.py` (resample + căn root) → composite QC lên soil tile → playground → báo PASS/FAIL từng file.

### Generation KHÔNG cần làm đúng (pipeline tự sửa)

- Canvas size / tỷ lệ khung — cứ ra square bất kỳ ≥1024 (tree) hoặc ≥512 (crop/tile), pipeline resample.
- Vị trí cây trong khung, root lệch tâm, sát mép, thiếu padding — pipeline scale + translate.
- Kích thước tương đối **giữa các loài khác nhau** — runtime display scale lo. (Không áp dụng cho tỷ lệ **giữa các stage trong cùng một pack** — cái đó bắt buộc, xem dưới.)

### Generation BẮT BUỘC làm đúng (transform không cứu được)

- Morphology đúng loài + silhouette đặc trưng (mục tiêu chính của đợt này).
- Style painterly nhất quán với pack hiện có.
- Harvest/flower cue đúng stage — không ra hoa/quả sớm.
- **Nền transparent thật** (không matte trắng/đen, không scene, không bake đất/tile).
- Một cây/một object duy nhất, không contact sheet, không text/watermark.
- Với pack nhiều stage: cùng một cá thể cây lớn dần, cấu trúc thay đổi thật (không phải một hình scale to dần).
- **Tỷ lệ chiều cao giữa các stage trong cùng pack** phải nằm trong band của profile loài đó (Profile A/B/C, `MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.vi.md` §523–560). Pipeline áp một hệ số scale chung cho cả pack nên **không sửa được** đường cong tăng trưởng sai.

---

## 2. Shared Style Block (paste đầu MỌI prompt)

```text
Art style — "Nostalgic Hand-Painted Farm Sprite": a cozy farming-game sprite
inspired by classic 2008–2012 browser/social farm games. Soft painterly
hand-painted rendering with light brush texture; selective soft outlines in
dark green/brown chromatic tones (never pure black, never thick uniform
vector lines); readable silhouette at small gameplay size; cheerful pastel
palette, slightly washed, higher saturation only on focal parts (fruit,
flowers); gentle shading, light source upper-left; organic asymmetric shapes.
NOT photorealistic, NOT glossy modern mobile art, NOT clean vector/cel-shade,
NOT neon.

Format: single isolated game sprite on a FULLY TRANSPARENT background.
One object only, whole object fully inside frame with margin on all sides.
A very small soft contact shadow directly under the base is allowed; no long
cast shadows, no ground/soil/scene baked in, no text or watermark.
```

**Negative nhắc lại khi model bướng:** `no background, no soil tile, no scene, no frame, no border, no watermark, no photorealism, no 3D render, no neon colors, no multiple views, no sprite sheet`.

**Reference:** luôn attach 1–2 asset PASS hiện có làm style anchor — tốt nhất là `coffee_stage-05_berry_v01.png` (chuẩn calibration) + 1 file cùng loài phiên bản cũ (để giữ nhận diện, kèm ghi chú điểm cần đổi).

---

## 3. Bảng output

| # | Hạng mục | Số file | Canvas tối thiểu | Đích |
|---|---|---:|---|---|
| A | soil_tilled | 1 | 512 | `masters/farm/soil/soil_tilled_v02.png` |
| B | carrot stage-05 | 1 | 512 | `masters/farm/crops/carrot/carrot_stage-05_harvestable_v02.png` |
| C | tonkin-jasmine pack | 5 | 512 | `masters/farm/crops/tonkin-jasmine/tonkin-jasmine_stage-0N_<semantic>_v02.png` |
| D | lotus stage-05 | 1 | 1024 | `masters/farm/aquatic-crops/lotus/lotus_stage-05_flowering_v02.png` |
| E–J | 6 fruit tree pack | 30 | 1024 | `masters/farm/trees/<species>/<species>_stage-0N_<semantic>_v02.png` |
| K | durian pack (loài mới) | 5 | 1024 | `masters/farm/trees/durian/durian_stage-0N_<semantic>_v01.png` — **đã generate 2026-09-08** |

Stage semantics giữ như v01 (tree: sprout/sapling/young/flowering/fruiting; crop: seeded/sprout/young/mature/harvestable; tonkin-jasmine xem mục C).

---

## A. soil_tilled (file v01 hỏng dữ liệu)

Attach reference: `soil_empty_v01.png` + `soil_planted_v01.png`.

```text
A farmland soil tile sprite for a farming game, matching the attached soil
tiles exactly in style, palette, perspective and plate shape: a rounded
oval/elliptical dirt plate seen from a high 3/4 top-down angle, soft dark
earthy rim, warm brown dirt surface.

State: TILLED — the surface is freshly ploughed into 4–6 neat parallel
furrow rows that follow the oval perspective of the plate, with soft ridges
and shallow trenches, slightly darker moist soil in the trenches. No plants,
no seeds, no grass.
```

Nghiệm thu: cùng hình dáng/kích thước plate với 5 tile kia (pipeline sẽ overlay so alpha); rãnh cày theo phối cảnh oval; không cây cỏ.

---

## B. carrot stage-05 (lộ vai củ)

Attach reference: `carrot_stage-04_mature_v01.png` + `carrot_stage-05_harvestable_v01.png` (ghi chú: giữ foliage, đổi phần củ).

```text
Harvest-ready carrot plant sprite, same species and foliage style as the
attached reference: a lush rosette of feathery green carrot tops growing
from one point.

Key change: at the base, 2–3 plump bright-orange carrot shoulders push
clearly up out of the ground — big, rounded, unmistakably readable as
carrots even at small size, taking roughly the bottom 1/5 of the plant
height, with a hint of root taper. This is the harvest cue: make the orange
pop against the green foliage.
```

Nghiệm thu: vai củ cam đọc rõ ở ~150 px; foliage vẫn cùng loài với s01–s04; cam chỉ xuất hiện ở s05 (s04 giữ nguyên v01).

---

## C. tonkin-jasmine — cả pack 5 stage, dạng leo giàn

Contract mới: **support-structure plant** như thanh long (spec §9.4 Profile C) — giàn gỗ cố định, **giống hệt nhau ở cả 5 ảnh** (kích thước, vị trí, kiểu dáng), chỉ dây leo phát triển. Đo progression bằng plant coverage, không tính giàn.

Attach reference: `dragon-fruit_stage-03_young_v01.png` (kiểu trụ đỡ + độ mộc) + 1 ảnh tonkin-jasmine v01 (giữ lá hình tim + hoa vàng-xanh đặc trưng).

Base prompt cho cả pack (thêm dòng stage tương ứng):

```text
A Tonkin jasmine vine (Telosma cordata, Vietnamese: thien ly) growing on a small rustic
wooden trellis — two upright weathered wooden posts with 2–3 horizontal
crossbars, simple and hand-made looking. The trellis is a FIXED structure:
keep its exact size, shape and position identical across all growth stages;
only the vine changes. Heart-shaped soft green leaves, slender twining stems.
```

| Stage | Dòng thêm vào prompt | File |
|---|---|---|
| 01 seeded | `Stage: just planted — the bare empty trellis, freshly disturbed soil spot at its base with a tiny 2-leaf sprout emerging. No vine on the trellis yet.` | `tonkin-jasmine_stage-01_seeded_v02.png` |
| 02 sprout | `Stage: young sprout — a single thin vine has started twining up one post, reaching the first crossbar, a handful of small heart-shaped leaves.` | `tonkin-jasmine_stage-02_sprout_v02.png` |
| 03 young | `Stage: young vine — the vine now covers about half the trellis with fresh green heart-shaped leaves, a few stems dangling. No flowers.` | `tonkin-jasmine_stage-03_young_v02.png` |
| 04 mature | `Stage: mature — dense foliage covering most of the trellis, layered heart-shaped leaves, a few curling stem tips. No flowers yet.` | `tonkin-jasmine_stage-04_mature_v02.png` |
| 05 harvestable | `Stage: harvestable — full lush coverage plus several restrained clusters of small pale yellow-green Tonkin jasmine flower buds tucked among the leaves; flowers are the focal cue but must not overload the sprite.` | `tonkin-jasmine_stage-05_harvestable_v02.png` |

Nghiệm thu: giàn đồng nhất 5/5 ảnh (pipeline sẽ diff silhouette giàn); coverage tăng theo Profile C (0.20–0.35 / 0.40–0.55 / 0.65–0.80 / 0.88–0.96 / 1.0); hoa chỉ có ở s05.

---

## D. lotus stage-05 (hoa nhỏ lại)

Attach reference: `lotus_stage-04_budding_v01.png` + `lotus_stage-05_flowering_v01.png` (ghi chú: giữ toàn bộ lá, chỉ sửa tỷ lệ hoa).

```text
Flowering lotus plant sprite, same species, leaf style and radial
composition as the attached stage-05 reference.

Key change: the main pink lotus bloom must be CLEARLY SMALLER than the
largest leaf — about 60–70% of its current size — botanically believable
while still the focal point through its saturated pink color. Keep one
green seed pod and one closed pink bud among the leaves. Leaves unchanged:
large round pastel green lotus pads on upright stems, radial spread.
```

Nghiệm thu: đường kính bông chính < đường kính lá lớn nhất; vẫn đọc là harvest stage nhờ màu; spread ratio không tụt so với s04 (Profile D).

---

## E–J. 6 fruit tree — regenerate cả pack, silhouette đặc trưng từng loài

Vấn đề đợt v01: 6 cây cùng công thức "tán tròn + thân nâu", chỉ khác quả. Đợt này **silhouette phải nhận diện được loài ngay cả khi che quả đi**.

### Template stage (dùng chung, thay `<SPECIES BLOCK>`)

```text
<SHARED STYLE BLOCK>

<SPECIES BLOCK — dán khối riêng từng loài bên dưới>

Same individual tree across all 5 stages, structure genuinely changing:
Stage 01 — sprout: small seedling, 2–4 leaves showing the species' leaf character.
  HEIGHT: 0.35–0.45 of the mature stage-05 tree.
Stage 02 — sapling: young tree, thin trunk, first branches, species leaf shape clear.
  HEIGHT: 0.55–0.65 of the mature stage-05 tree.
Stage 03 — young: distinctly smaller and simpler than mature, but the species
silhouette is already recognizable. No flowers, no fruit.
  HEIGHT: 0.75–0.88 of the mature stage-05 tree.
Stage 04 — flowering: near-full silhouette with the species' flowers. No fruit.
  HEIGHT: 0.90–0.98 of the mature stage-05 tree.
Stage 05 — fruiting: full mature silhouette, harvest-ready fruit as focal cue.
  HEIGHT: this is the reference — 1.0.
```

> **Dòng `HEIGHT:` là bắt buộc, phải nằm trong prompt của từng stage.** Vì mỗi
> prompt chỉ mang **một** dòng stage, ràng buộc kích thước không đặt ngay trên
> dòng đó thì model không bao giờ thấy. Bỏ dòng này là lý do `coconut` vỡ
> Profile B (`0.65/0.84/0.95/0.99`) và `durian` vỡ Profile A
> (`0.66/0.95/0.99/1.00`) — cây gần như không lớn nữa từ stage 02.
>
> `normalize_pack.py` áp **một** hệ số scale cho cả pack nên **không cứu được**
> đường cong tăng trưởng bẹt: sai là phải generate lại.
>
> Số trên là **Profile A** (cây thân gỗ đứng — E–J, `durian`, `coffee`,
> `rubber`). Loài khác profile phải thay số: **Profile B** cọ/dừa
> (`0.25–0.35 / 0.40–0.55`), **Profile C** cây leo giàn
> (`0.20–0.35 / 0.40–0.55`). Bảng đầy đủ: `MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.vi.md` §523–560.

Generate **từng ảnh một** (một prompt = shared block + species block + đúng một dòng stage).

### E. Xoài `mango`

```text
MANGO TREE. Silhouette: a BROAD SPREADING DOME — the canopy is clearly wider
than tall, with 2–3 heavy near-horizontal limbs. Long slender dark-green
leaves drooping in clusters, young leaf flush in coppery red-bronze at
branch tips. Flowers (stage 4): upright pale yellow panicle plumes at the
canopy edge. Fruit (stage 5): yellow-orange mangoes DANGLING on long string-
like stalks well below the foliage — the hanging stalks are the signature.
```

### F. Bưởi `pomelo`

```text
POMELO TREE. Silhouette: an OPEN, slightly sparse and irregular crown where
individual sturdy branches stay visible through the foliage; thick trunk.
Large rounded glossy leaves with winged leaf stalks. Flowers (stage 4):
large white citrus blossoms. Fruit (stage 5): only a FEW but VERY LARGE
round green-yellow pomelos, visibly heavy, bending their branches downward —
few-but-huge is the signature.
```

### G. Chanh `lemon`

```text
LEMON TREE. Silhouette: a SMALL LOW BUSHY citrus — clearly the shortest
fruit tree, crown starting near the ground, almost shrub-like, dense with
small glossy pointed leaves, thin twiggy branches. Flowers (stage 4): small
white-purple-tinged citrus blossoms. Fruit (stage 5): many small bright
yellow lemons scattered evenly through the low canopy. Keep the whole tree
compact and low — it must NOT look like a tall tree.
```

### H. Vú sữa `star-apple`

```text
STAR APPLE TREE (vu sua, Chrysophyllum cainito). Silhouette: dense layered
canopy with slightly DROOPING branch tips. Signature: TWO-TONE FOLIAGE —
leaves glossy dark green on top with a distinctly COPPERY GOLDEN-BROWN
underside, so the canopy shimmers green-and-bronze wherever leaves turn.
This two-tone shimmer must read at a glance. Flowers (stage 4): tiny
inconspicuous purplish-white clusters along twigs. Fruit (stage 5): round
smooth fruits in purple and green-purple, sitting close to the branches.
```

### I. Vải `lychee`

```text
LYCHEE TREE. Silhouette: a DENSE LOW ROUNDED MUSHROOM-shaped canopy, wider
than tall, compact and full with almost no gaps; short stout trunk. Pinnate
leaves in drooping clusters. Flowers (stage 4): airy pale yellow-green
panicle sprays on the canopy surface. Fruit (stage 5): bright red round
fruits with a BUMPY knobbly rind, hanging in tight grape-like BUNCHES at
the canopy edge.
```

### J. Chôm chôm `rambutan`

```text
RAMBUTAN TREE. Silhouette: an irregular OPEN spreading crown with a few
distinct foliage clumps and visible gaps between them (less tidy than
lychee); slightly leaning character in the trunk. Flowers (stage 4): subtle
greenish-yellow clusters. Fruit (stage 5): red fruits covered in SOFT HAIRY
GREEN-TIPPED SPINES, in loose clusters — the hairy texture is the signature
and must be visible.
```

### K. Sầu riêng `durian`

```text
DURIAN TREE (Durio zibethinus). Silhouette: a SLENDER, TALL PYRAMIDAL / CONICAL
CANOPY — distinctly taller than wide. Central upright straight woody trunk with
elegant vertical taper, branching outward into 3–4 clearly SEPARATED horizontal
scaffold tiers (pagoda-like tiered architecture). Between the tiers there must be
EMPTY TRANSPARENT GAPS you can see straight through — the canopy is a few
distinct foliage shelves stacked with air between them, NOT one continuous
conical mass and NOT a round dense dome. Think stacked pagoda roofs, not a
Christmas tree.
Foliage: slender elongated lanceolate leaves with sharp pointed tips. Two-tone
coloring: upper leaf surface is a light, soft warm olive-green and sunny pastel
sage-green with crisp pale-yellow midrib veins and glossy sunlight highlights;
underside has a soft shimmering light golden-bronze / dusty gold sheen.
Flowers (stage 4): clusters of creamy-white and pale golden-butter blossoms
hanging directly beneath the horizontal woody branches (cauliflory), dangling
down into the open gaps between tiers so each cluster is silhouetted against
empty space instead of being buried in the leaves.
Fruit (stage 5): 5–7 large, spiky DURIAN fruits with sharp pyramidal thorns,
bright golden-olive green, hanging on thick rope-like woody stalks directly
underneath the horizontal tiered limbs (cauliflory). Each fruit is BIG — at
least as wide as the trunk — and hangs DOWN INTO THE EMPTY GAP below its own
branch tier, fully silhouetted against the transparent background with clear
space around it. No fruit may be tucked inside or overlapped by the foliage
mass. The fruits must be the single loudest read in the image at 150 px.
```

Nghiệm thu nhóm E–K:

- Che phần quả đi vẫn phân biệt được 7 loài qua silhouette (đặc biệt: xoài rộng-vòm, chanh thấp-bụi, vải nấm-đặc, chôm chôm mở-lởm chởm, vú sữa hai màu lá, sầu riêng cao-dáng tháp-phân tầng cành).
- Chanh: thấp nhất nhóm (display target đã hạ ~256 px — spec §9.5).
- Không hoa ở s01–s03, không quả ở s01–s04.
- **Harvest cue phải nằm trong khoảng trống.** Quả (và hoa) treo ra chỗ hở, tách khỏi khối lá, viền rõ trên nền transparent. Quả chìm vào tán là FAIL kể cả khi ảnh vẽ đẹp — ở 150 px người chơi không đọc được là cây đã tới lứa hay chưa.
- Progression Profile A (đã nới s03 ≤ 0.88).
- Pipeline sẽ tự căn root (512, 970) và margin — không cần canh khi generate.

---

## 4. Sau khi generate

- File v02 đặt cạnh v01 (không xóa v01 cho tới khi PASS).
- Claude chạy: audit → normalize → composite → playground → báo cáo per-file theo format spec §17.
- File PASS: v02 thành canonical, v01 archive; runtime atlas rebuild ở bước cuối.

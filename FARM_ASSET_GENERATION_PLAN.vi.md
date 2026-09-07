# Mayhoa Farm Asset Generation Plan

**Status:** Production roadmap  
**Project:** Mayhoa  
**Art style:** Mayhoa Nostalgic Hand-Painted Farm Sprite  
**Language:** Tiếng Việt  

Tài liệu này định nghĩa kế hoạch generate artwork cho hệ thống farm đầu tiên của Mayhoa. Mọi asset trong kế hoạch này phải tuân theo `MAYHOA_ART_STYLE_SPEC.vi.md`.

---

## 1. Mục tiêu

Xây dựng bộ artwork farm nền tảng có thể dùng trực tiếp trong game, bao gồm:

- ô đất và các trạng thái đất;
- cây trồng ngắn ngày;
- cây trồng thủy sinh cho khu vực mặt nước / ao;
- cây ăn quả / cây lâu năm;
- cỏ dại xuất hiện trên ô đất;
- sâu, bọ và infestation overlays;
- dụng cụ tương tác với farm;
- hệ size, naming và export phù hợp với PixiJS.

Nguyên tắc triển khai:

1. Không generate toàn bộ asset ngay từ đầu.
2. Khóa visual calibration trước.
3. Generate theo batch tuần tự.
4. Mỗi batch phải QC trước khi batch kế tiếp bắt đầu.
5. Growth stage phải thay đổi silhouette, không chỉ scale cùng một ảnh.
6. Master asset và runtime asset được tách riêng.

---

## 2. Asset taxonomy

```text
farm/
  soil/
  crops/
  aquatic-crops/
  trees/
  weeds/
  pests/
  tools/
```

### 2.1 `farm/soil`

Ô đất và trạng thái của đất.

### 2.2 `farm/crops`

Cây trồng ngắn ngày / cây thấp hoặc trung bình:

- rice / lúa nước
- corn / bắp
- carrot
- tonkin-jasmine / hoa thiên lý
- culantro / ngò gai
- mint / bạc hà

### 2.3 `farm/aquatic-crops`

Cây trồng thủy sinh hoặc bán thủy sinh, được trồng trên slot mặt nước thay vì soil tile:

- lotus / sen (`Nelumbo nucifera`)
- water-mimosa / rau nhút (`Neptunia oleracea`)
- water-spinach / rau muống (`Ipomoea aquatica`)

Artwork cây phải tách khỏi water surface, pond edge và ripple FX để có thể compose với hệ ao / mặt nước riêng.

### 2.4 `farm/trees`

Cây ăn quả và cây lâu năm:

- mango / xoài
- pomelo / bưởi
- lemon / chanh
- coconut / dừa
- dragon-fruit / thanh long
- coffee / cà phê
- star-apple / vú sữa
- rubber / cao su
- rambutan / chôm chôm
- lychee / vải

### 2.5 `farm/weeds`

Cỏ dại được render như overlay riêng và đặt chung với cây trên ô đất.

### 2.6 `farm/pests`

Sâu, bọ, infestation overlays.

### 2.7 `farm/tools`

- harvest hand / bàn tay thu hoạch
- watering can / bình tưới
- pest catcher / dụng cụ bắt sâu
- pruning shears / kéo cắt tỉa
- shovel / xẻng

---

## 3. Phân nhóm cây theo cấu trúc hình học

### 3.1 Field crops

```text
rice
corn
carrot
tonkin-jasmine
culantro
mint
```

Đặc điểm:

- footprint chủ yếu trong một ô đất;
- silhouette thấp hoặc trung bình;
- đọc rõ ở gameplay size;
- dùng growth system 5 stage mặc định.

### 3.2 Aquatic crops

```text
lotus
water-mimosa
water-spinach
```

Đặc điểm:

- anchor theo waterline / root-origin chung, không center theo canvas;
- không bake nước, bờ ao, đất hoặc ripple vào sprite cây;
- lotus có silhouette cao và rộng hơn, còn rau nhút / rau muống thiên về cụm ngang;
- foliage có thể vượt nhẹ khỏi slot hình học nhưng gameplay footprint phải ổn định;
- dùng growth system 5 stage, mỗi stage phải phát triển cấu trúc thật chứ không scale cùng một ảnh.

### 3.3 Fruit trees

```text
mango
pomelo
lemon
star-apple
rambutan
lychee
```

Đặc điểm:

- trunk + branch logic rõ;
- canopy theo foliage masses;
- fruit chỉ cần đủ để nhận diện species;
- scale tương đối phải nhất quán giữa các tree.

### 3.4 Special tropical structures

```text
coconut
dragon-fruit
```

Hai asset này cần batch riêng vì silhouette khác mạnh so với fruit tree thông thường.

### 3.5 Industrial / perennial crops

```text
coffee
rubber
```

Coffee có shrub/tree form và berry focal points. Rubber có thân cao hơn và có thể cần harvest/tapping state nếu gameplay hỗ trợ.

---

## 4. Growth stage system

### 4.1 Crop ngắn ngày — 5 stage

```text
stage-01_seeded
stage-02_sprout
stage-03_young
stage-04_mature
stage-05_harvestable
```

Mỗi stage phải thay đổi silhouette và structural complexity.

### 4.2 Aquatic crop — 5 stage

```text
stage-01_planted
stage-02_sprout
stage-03_young
stage-04_mature
stage-05_harvestable
```

Tên visual state có thể chuyên biệt theo species. Lotus có thể dùng `stage-04_budding` và `stage-05_flowering`, còn rau nhút / rau muống thể hiện độ trưởng thành chủ yếu bằng mật độ và độ lan của foliage.

Lotus hỗ trợ nhiều harvest output từ cùng một species:

```text
lotus_flower    # hoa sen
lotus_rhizome   # củ sen
lotus_stem      # ngó sen
lotus_seed      # hạt sen
```

Đây là gameplay/item IDs, không phải bốn lifecycle sprite độc lập. **Scope plant/aquatic hiện tại chỉ cần 5 world lifecycle assets của lotus** (`planted`, `sprout`, `young`, `budding`, `flowering`). Artwork thu hoạch/inventory cho cả bốn output `lotus_flower`, `lotus_rhizome`, `lotus_stem`, `lotus_seed` **được defer sang item/inventory phase sau và không phải generate cùng bộ 5 lifecycle hiện tại**. Nếu gameplay sau này cần phân biệt thời điểm thu hoạch, có thể thêm late-stage variant/overlay như `flowering` hoặc `seed-pod`. Phần thân rễ chìm dưới nước không vẽ lộ trong world sprite thông thường.

Rau nhút và rau muống mặc định thu hoạch thân/lá non. Nếu sau này có cơ chế cắt rồi mọc lại, thêm `regrowing` state ngoài core 5-stage set.

### 4.3 Fruit tree / perennial — 5 stage mặc định

```text
stage-01_sprout
stage-02_sapling
stage-03_young
stage-04_flowering-or-mature
stage-05_harvestable
```

`harvestable` có thể là `fruiting`, `berry`, hoặc `tapping` tùy loại cây.

#### 4.3.1 Hard generation contract cho fruit tree

Mọi lần generate một fruit tree/perennial theo lifecycle 5 stage phải tuân các rule sau:

1. **5 stages = 5 ảnh độc lập.** Phải output đúng năm image asset riêng biệt, mỗi ảnh chứa đúng một stage. Không ghép năm cây vào cùng một ảnh, không tạo contact sheet, không tạo sprite sheet thay cho năm master image.
2. **Cùng canvas, cùng root anchor.** Cả năm ảnh phải dùng cùng canvas size / aspect ratio và cùng một tọa độ `root-origin` / điểm tiếp xúc thấp nhất của gốc cây. Không center từng stage theo bounding box riêng; gameplay anchor mới là điểm cố định.
3. **Scale tăng tuần tự.** Perceived height, canopy spread và structural complexity phải tăng rõ ràng theo thứ tự `stage-01 < stage-02 < stage-03 < stage-04 < stage-05`. Mỗi stage phải lớn hơn stage trước một cách hợp lý, không được có early stage lớn ngang hoặc lớn hơn mature stage.
4. **Không chỉ scale cùng một hình.** Mỗi stage phải phát triển cấu trúc thật: thân dày dần, branching logic rõ hơn, canopy phức tạp hơn và silhouette thay đổi theo lifecycle.
5. **Stage 01 — sprout:** nhỏ nhất; thân non / early trunk, rất ít lá, chưa có canopy trưởng thành; không hoa, không trái.
6. **Stage 02 — sapling:** cây non rõ ràng; thân mảnh, một vài nhánh, canopy nhỏ; **không hoa và tuyệt đối không có trái**.
7. **Stage 03 — young:** cây trẻ; branching và canopy phát triển hơn stage 02 nhưng vẫn chưa trưởng thành; **không hoa, không trái**.
8. **Stage 04 — flowering-or-mature:** cây trưởng thành hơn stage 03. Với species có flowering state, hoa bắt đầu xuất hiện ở đây; không render harvest-ready fruit trừ khi gameplay/spec của species explicit yêu cầu khác.
9. **Stage 05 — harvestable / fruiting:** stage lớn nhất và hoàn thiện nhất; fruit/berry/harvest focal point xuất hiện ở đây theo species.
10. Nếu dùng stage 05 hoặc ảnh reference có trái để giữ species identity, reference đó chỉ được dùng cho morphology, leaf/trunk language và fruit identity; **không copy hoa/trái ngược lifecycle vào stage 01–03**.
11. Tree sprite không bake soil, pot, ground tile hoặc environment vào master artwork trừ khi spec của asset explicit yêu cầu.

Prompt generation cho một full fruit-tree set phải explicit chứa các constraint tương đương:

```text
OUTPUT REQUIREMENT: Generate exactly five separate image assets, not one composite image and not a sprite sheet. One output image per lifecycle stage: stage-01, stage-02, stage-03, stage-04, stage-05.

ANCHOR REQUIREMENT: All five images must use the exact same canvas size and the exact same root-origin coordinate. The lowest/root contact point of the trunk must remain fixed across all five outputs. Do not center each tree independently.

GROWTH REQUIREMENT: Tree size and structural complexity must increase monotonically from stage 01 through stage 05. Each successive stage must be visibly larger than the previous stage while preserving believable biological growth.

LIFECYCLE REQUIREMENT: stage-02 is strictly a sapling — foliage only, no flowers and absolutely no fruit. stage-03 is a young vegetative tree — no flowers and no fruit. Flowers begin only at stage-04 when applicable; harvestable fruit appears only at stage-05.
```

---

## 5. Size system

Không ship master artwork trực tiếp vào runtime.

### 5.1 Master generation size

| Asset class | Master target |
|---|---:|
| Small crop / weed / pest | 512×512 |
| Medium crop / herb | 768×768 |
| Aquatic crop | 768×768; lotus có thể dùng 1024×1024 nếu cần canopy/flower breathing room |
| Tree / animal-sized farm asset | 1024×1024 |
| Tall/special tree | 1024×1280 hoặc square master với padding |
| Tool icon | 512×512 |

### 5.2 Runtime semantic size classes

| Class | Khoảng hiển thị gợi ý | Dùng cho |
|---|---:|---|
| S | 64–96 px | weed, pest, tiny growth stage, small tool |
| M | 128–160 px | rice, carrot, herbs, rau nhút, rau muống, mature low crop |
| L | 192–256 px | corn, coffee, dragon fruit, lotus |
| XL | 256–384 px | mango, pomelo, coconut, rubber, fruit trees |

Kích thước runtime cuối cùng sẽ được điều chỉnh theo camera và world scale của game, nhưng phải giữ cùng perceived scale giữa các asset.

---

## 6. Grounding / surface systems

### 6.1 Soil system

`farm/soil` là foundation của toàn bộ visual calibration.

### Required states

```text
soil_empty
soil_tilled
soil_wet
soil_planted
soil_dry
soil_harvested
```

### Quy tắc

- crop, weed và pest phải có thể đặt lên soil tile chuẩn;
- wet/dry state phải đọc rõ nhưng không quá saturated;
- footprint và camera angle phải cố định;
- weed/pest không bake cố định vào soil texture;
- crop shadow phải tương thích với grounding của soil tile.

### 6.2 Aquatic crop area

Khu aquatic crop là vùng canh tác trên mặt nước nông / ao, dùng cho lotus, water-mimosa và water-spinach.

Quy tắc:

- `farm/aquatic-crops` chỉ chứa artwork cây;
- water surface / pond tile, bờ ao và ripple FX thuộc hệ environment/water riêng, không bake vào crop master;
- mọi stage của cùng species dùng chung waterline/root anchor để đổi sprite không bị nhảy vị trí;
- không center cây theo canvas; giữ gameplay anchor ổn định;
- contact ripple/shadow chỉ là optional overlay/FX;
- không vẽ lộ phần thân rễ/củ chìm dưới nước trong world sprite thông thường;
- khi đặt chung fish/pond gameplay, foliage không được che kín vùng nước tới mức làm mất readability của cá hoặc interaction marker;
- giữ cùng camera angle, upper-left lighting và perceived world scale với phần farm còn lại.

---

## 7. Weed system

MVP weed pack:

```text
weed_small_01
weed_small_02
weed_medium_01
weed_medium_02
weed_dense_01
```

Quy tắc:

- overlay riêng;
- silhouette messy hơn crop chính;
- không che mất crop identity;
- green phải khác crop foliage đủ để nhận diện;
- có thể random variant/rotation nhẹ trong runtime.

---

## 8. Pest system

MVP pest pack:

```text
caterpillar
beetle
aphid_cluster
snail
leaf_bug
```

Ưu tiên đầu tiên:

```text
caterpillar_single
caterpillar_cluster
beetle_single
aphid_cluster
```

Quy tắc:

- exaggerate scale nhẹ để đọc được trong gameplay;
- pest sprite và infestation marker có thể là hai asset khác nhau;
- không render theo hướng realistic gross/insect horror;
- vẫn giữ cute/readable Mayhoa style.

---

## 9. Tool system

Required tools:

```text
harvest-hand
watering-can
pest-catcher
pruning-shears
shovel
```

### Visual rules

- gameplay interaction icon, không phải realistic illustration;
- silhouette cực rõ;
- 3/4 angle nhẹ nếu phù hợp;
- contrast cao hơn world asset một chút;
- không bake button background vào artwork;
- hover/disabled/pressed ưu tiên xử lý bằng UI/runtime thay vì generate asset riêng.

### Minimal artwork state

```text
idle
active   # chỉ khi interaction animation cần sprite riêng
```

---

## 10. Folder structure đề xuất

```text
masters/
  farm/
    soil/
    crops/
      rice/
      corn/
      carrot/
      tonkin-jasmine/
      culantro/
      mint/
    aquatic-crops/
      lotus/
      water-mimosa/
      water-spinach/
    trees/
      mango/
      pomelo/
      lemon/
      coconut/
      dragon-fruit/
      coffee/
      star-apple/
      rubber/
      rambutan/
      lychee/
    weeds/
    pests/
    tools/

runtime/
  1x/
    farm/
  2x/
    farm/
```

`masters/` lưu artwork nguồn chất lượng cao. `runtime/` lưu bản đã resize/optimize cho game.

---

## 11. Naming convention

Pattern:

```text
<asset>_<state-or-stage>_v<nn>.png
```

Ví dụ:

```text
rice_stage-01_seeded_v01.png
rice_stage-05_harvestable_v01.png
mango_stage-01_sprout_v01.png
mango_stage-04_flowering_v01.png
weed_small_v01.png
pest_caterpillar_single_v01.png
tool_watering-can_idle_v01.png
```

Không encode resolution trực tiếp trong logical filename; resolution được phân tách bằng thư mục runtime như `1x/`, `2x/`.

---

## 12. Production phases

# Phase 0 — Calibration Set

Mục tiêu: khóa perspective, scale, outline, palette, shadow, foliage density và perceived detail level trước khi tạo full production pack.

Generate representative state trước:

1. `soil_tilled`
2. `rice_stage-05_harvestable`
3. `corn_stage-05_harvestable`
4. `mango_stage-05_fruiting`
5. `weed_small_01`
6. `caterpillar_single`
7. `tool_watering-can_idle`

### Exit criteria

Chỉ chuyển sang Phase 1 khi cả 7 asset:

- nhìn như cùng một game;
- cùng lighting logic;
- scale tương đối hợp lý;
- outline và detail density nhất quán;
- đặt được cùng soil tile mà không lệch camera/perspective;
- vẫn đọc tốt ở runtime size.

---

# Phase 1 — Soil Foundation

Generate full soil states:

- empty
- tilled
- wet
- planted
- dry
- harvested

Sau đó khóa soil tile làm reference foundation cho toàn bộ crop production.

---

# Phase 2 — Core Crop Pack

Generate full growth stages cho:

1. rice
2. corn
3. carrot

Mỗi loại 5 stage.

Mục tiêu của phase này là khóa growth-stage language cho cả crop system.

---

# Phase 3 — Herb / Low Crop Pack

Generate full growth stages cho:

1. tonkin-jasmine
2. culantro
3. mint

Mỗi loại 5 stage nếu gameplay không yêu cầu ít hơn.

---

# Phase 4 — Core Fruit Tree Pack

Generate:

1. mango
2. pomelo
3. lemon
4. star-apple

Mỗi loại 5 stage:

- sprout / early sapling
- sapling
- young
- flowering
- fruiting / harvestable

---

# Phase 5 — Tropical Fruit Tree Pack

Generate:

1. rambutan
2. lychee

Mỗi loại 5 stage theo lifecycle fruit tree/perennial chuẩn.

---

# Phase 6 — Special Structure Pack

Generate:

1. coconut
2. dragon-fruit

Mỗi loại 5 stage; tên state có thể chuyên biệt theo cấu trúc của species.

Mỗi loại cần visual calibration riêng về footprint và vertical scale, nhưng vẫn phải tuân world scale chung.

---

# Phase 7 — Industrial / Perennial Pack

Generate:

1. coffee
2. rubber

Mỗi loại 5 stage theo lifecycle perennial chuẩn.

Coffee harvest state cần berry focal points. Rubber harvest state có thể dùng tapping representation nếu gameplay xác nhận cơ chế này.

---

# Phase 8 — Aquatic Crop Area Pack

Generate full growth stages cho:

1. lotus
2. water-mimosa
3. water-spinach

Mỗi loại 5 stage.

Acceptance requirements riêng:

- shared waterline/root anchor ổn định giữa mọi stage;
- không bake water surface hoặc pond edge vào plant sprite;
- lotus stage cuối phải đọc rõ identity bằng lá + hoa hoặc seed-pod focal point;
- lotus gameplay mapping hỗ trợ `lotus_flower`, `lotus_rhizome`, `lotus_stem`, `lotus_seed` mà không cần bốn lifecycle độc lập;
- rau nhút và rau muống phải có silhouette đủ khác nhau ở runtime size;
- test composition trên ít nhất một neutral water tile trước khi approve.

---

# Phase 9 — Weed Pack

Generate full weed variants:

- 2 small
- 2 medium
- 1 dense

Test overlay với ít nhất rice, corn, carrot và mango/fruit tree plot nếu applicable.

---

# Phase 10 — Pest Pack

Generate:

- caterpillar single
- caterpillar cluster
- beetle single
- aphid cluster
- snail
- leaf bug

Test trên crop có foliage thấp, cao và tree foliage.

---

# Phase 11 — Farming Tool Pack

Generate:

- harvest hand
- watering can
- pest catcher
- pruning shears
- shovel

Tool pack cần được test ở UI interaction size riêng, không đánh giá bằng world scale của crop/tree.

---

## 13. Batch execution rule

Mỗi phase được thực hiện theo chu trình:

```text
PLAN -> GENERATE -> REVIEW -> REVISE -> APPROVE -> SYNC -> VERIFY -> OPTIMIZE -> COMMIT
```

### Asset sync transport

Claude-in-Chrome tải thẳng ảnh từ ChatGPT xuống đĩa local. **Không dùng Google Drive, không dùng `gws`.**

Luồng transport chính thức:

```text
ChatGPT Create image output
-> mở ảnh ở fullscreen viewer, bấm nút "Save"
-> file rơi vào ~/Downloads, tên dạng "ChatGPT Image <ngày giờ>.png"
-> nhận diện file mới theo mốc thời gian
-> verify MIME, dimensions, alpha thật
-> move vào `.ai-bridge/<species>/`; chỉ bản approved mới vào `masters/...`
```

Nhận diện file mới an toàn cho cả mẻ nhiều ảnh — đặt mốc **trước** khi bấm Save:

```bash
MARK=$(mktemp); touch "$MARK"
# ... bấm Save lần lượt theo đúng thứ tự stage ...
find ~/Downloads -name 'ChatGPT Image*.png' -newer "$MARK" -print0 | xargs -0 ls -tr
# thứ tự cũ -> mới = đúng thứ tự đã bấm
```

Quy tắc:

- Nút tải tên là **"Save"**, chỉ có trong fullscreen viewer (cùng thanh với Remove BG / Erase). Khung chat KHÔNG có nút Download.
- Cách này chỉ đúng khi Chrome và repo ở **cùng một máy** — đúng với setup hiện tại. Nếu tách máy thì phải quay lại dùng staging layer.
- Không dựa vào ChatGPT `openai/fileParams` cho canonical asset transport.
- Không invoke local Codex, Codex CLI, `codex exec` hoặc bất kỳ Codex-backed executor nào để sync asset.
- Giữ raw + prompt trong `.ai-bridge/<species>/`; chỉ approved asset mới được đưa vào `masters/`.
- Phải verify downloaded file đúng image type và có alpha thật trước khi nhận vào canonical asset set.

> **Lịch sử:** trước 2026-09-05 luồng này đi qua Google Drive + `gws` vì CodexPro2 không nhận binary
> trực tiếp từ Create image. Chuyển sang Claude-in-Chrome thì bỏ được cả chặng đó: bớt một connector
> call, bớt một lần click Allow, và bỏ hẳn rủi ro OAuth token hết hạn — `gws` token đã bị revoke đúng
> lúc cần dùng (2026-09-05).

Không generate phase tiếp theo trước khi phase hiện tại đạt acceptance criteria, trừ khi asset chỉ được tạo thử nghiệm và không merge vào production set.

---

## 14. QC checklist cho mỗi asset

- đúng species / object identity;
- đúng Mayhoa art style;
- silhouette rõ ở gameplay size;
- không quá vector-clean;
- không glossy;
- không neon;
- không over-detail;
- outline dark-chromatic và có chọn lọc;
- ánh sáng upper-left nhất quán;
- shadow mềm;
- organic asymmetry hợp lý;
- crop/tree structure logic rõ;
- relative scale hợp với soil và asset lân cận;
- transparent background sạch;
- không text / UI / scene background không cần thiết;
- master có đủ breathing room;
- runtime export không bị halo, blur hoặc mất silhouette.

---

## 15. Git workflow

### Mỗi production batch

Mỗi phase/batch được commit riêng sau khi đã approve.

Commit message gợi ý:

```text
assets: add farm calibration set
assets: add soil state pack
assets: add core crop growth stages
assets: add herb crop pack
assets: add core fruit tree pack
assets: add tropical fruit tree pack
assets: add special tropical crops
assets: add perennial crop pack
assets: add aquatic crop area pack
assets: add weed pack
assets: add pest pack
assets: add farming tool pack
```

### Không commit

- rejected generation;
- duplicate variants không còn dùng;
- master lỗi composition;
- runtime export chưa QC.

Nếu cần giữ exploratory generations, đặt ở khu vực riêng và không coi là canonical runtime asset.

---

## 16. Estimated initial scope

Ước lượng production sprite masters ban đầu:

- Soil: ~6
- Field crops: ~30
- Aquatic crops: ~15
- Trees/perennials: ~50
- Weeds: ~5
- Pests: ~6
- Tools: ~5

Tổng khoảng **115+ master sprites**, chưa tính revisions, harvest-item artwork và optional UI/animation variants.

---

## 17. Execution order chính thức

Thứ tự mặc định:

```text
Phase 0  Calibration Set
Phase 1  Soil Foundation
Phase 2  Core Crop Pack
Phase 3  Herb / Low Crop Pack
Phase 4  Core Fruit Tree Pack
Phase 5  Tropical Fruit Tree Pack
Phase 6  Special Structure Pack
Phase 7  Industrial / Perennial Pack
Phase 8  Aquatic Crop Area Pack
Phase 9  Weed Pack
Phase 10 Pest Pack
Phase 11 Farming Tool Pack
```

Sau khi Phase 0 được approve, artwork sẽ được generate tuần tự theo thứ tự trên trừ khi gameplay priority thay đổi.

---

## 18. First production task

**Task ID:** `FARM-P0-CALIBRATION`

Generate 7 representative assets:

```text
soil_tilled
rice_stage-05_harvestable
corn_stage-05_harvestable
mango_stage-05_fruiting
weed_small_01
pest_caterpillar_single_v01
tool_watering-can_idle_v01
```

Mục tiêu của task này không phải số lượng asset mà là khóa visual language cho toàn bộ farm pack.

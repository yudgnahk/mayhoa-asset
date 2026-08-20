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
- thien-ly / hoa thiên lý
- ngo-gai / ngò gai
- mint / bạc hà

### 2.3 `farm/trees`

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

### 2.4 `farm/weeds`

Cỏ dại được render như overlay riêng và đặt chung với cây trên ô đất.

### 2.5 `farm/pests`

Sâu, bọ, infestation overlays.

### 2.6 `farm/tools`

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
thien-ly
ngo-gai
mint
```

Đặc điểm:

- footprint chủ yếu trong một ô đất;
- silhouette thấp hoặc trung bình;
- đọc rõ ở gameplay size;
- dùng growth system 5 stage mặc định.

### 3.2 Fruit trees

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

### 3.3 Special tropical structures

```text
coconut
dragon-fruit
```

Hai asset này cần batch riêng vì silhouette khác mạnh so với fruit tree thông thường.

### 3.4 Industrial / perennial crops

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

### 4.2 Fruit tree / perennial — 4 stage mặc định

```text
stage-01_sapling
stage-02_young
stage-03_mature
stage-04_harvestable
```

`harvestable` có thể là `fruiting`, `berry`, hoặc `tapping` tùy loại cây.

Nếu gameplay sau này cần flowering state, thêm một stage riêng thay vì bake vào mature.

---

## 5. Size system

Không ship master artwork trực tiếp vào runtime.

### 5.1 Master generation size

| Asset class | Master target |
|---|---:|
| Small crop / weed / pest | 512×512 |
| Medium crop / herb | 768×768 |
| Tree / animal-sized farm asset | 1024×1024 |
| Tall/special tree | 1024×1280 hoặc square master với padding |
| Tool icon | 512×512 |

### 5.2 Runtime semantic size classes

| Class | Khoảng hiển thị gợi ý | Dùng cho |
|---|---:|---|
| S | 64–96 px | weed, pest, tiny growth stage, small tool |
| M | 128–160 px | rice, carrot, herbs, mature low crop |
| L | 192–256 px | corn, coffee, dragon fruit |
| XL | 256–384 px | mango, pomelo, coconut, rubber, fruit trees |

Kích thước runtime cuối cùng sẽ được điều chỉnh theo camera và world scale của game, nhưng phải giữ cùng perceived scale giữa các asset.

---

## 6. Soil system

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
      thien-ly/
      ngo-gai/
      mint/
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
mango_stage-01_sapling_v01.png
mango_stage-04_fruiting_v01.png
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
4. `mango_stage-04_fruiting`
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

1. thien-ly
2. ngo-gai
3. mint

Mỗi loại 5 stage nếu gameplay không yêu cầu ít hơn.

---

# Phase 4 — Core Fruit Tree Pack

Generate:

1. mango
2. pomelo
3. lemon
4. star-apple

Mỗi loại 4 stage:

- sapling
- young
- mature
- fruiting/harvestable

---

# Phase 5 — Tropical Fruit Tree Pack

Generate:

1. rambutan
2. lychee

Mỗi loại 4 stage.

---

# Phase 6 — Special Structure Pack

Generate:

1. coconut
2. dragon-fruit

Mỗi loại cần visual calibration riêng về footprint và vertical scale, nhưng vẫn phải tuân world scale chung.

---

# Phase 7 — Industrial / Perennial Pack

Generate:

1. coffee
2. rubber

Coffee harvest state cần berry focal points. Rubber harvest state có thể dùng tapping representation nếu gameplay xác nhận cơ chế này.

---

# Phase 8 — Weed Pack

Generate full weed variants:

- 2 small
- 2 medium
- 1 dense

Test overlay với ít nhất rice, corn, carrot và mango/fruit tree plot nếu applicable.

---

# Phase 9 — Pest Pack

Generate:

- caterpillar single
- caterpillar cluster
- beetle single
- aphid cluster
- snail
- leaf bug

Test trên crop có foliage thấp, cao và tree foliage.

---

# Phase 10 — Farming Tool Pack

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
PLAN -> GENERATE -> REVIEW -> REVISE -> APPROVE -> OPTIMIZE -> COMMIT
```

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
- Trees/perennials: ~40
- Weeds: ~5
- Pests: ~6
- Tools: ~5

Tổng khoảng **90+ master sprites**, chưa tính revisions và optional UI/animation variants.

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
Phase 8  Weed Pack
Phase 9  Pest Pack
Phase 10 Farming Tool Pack
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
mango_stage-04_fruiting
weed_small_01
pest_caterpillar_single_v01
tool_watering-can_idle_v01
```

Mục tiêu của task này không phải số lượng asset mà là khóa visual language cho toàn bộ farm pack.

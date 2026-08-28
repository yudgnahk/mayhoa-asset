# Mayhoa — Remaining Plant Asset Generation Plan

**Status:** Ready for parallel execution  
**Project:** Mayhoa  
**Art style:** Mayhoa Nostalgic Hand-Painted Farm Sprite  
**Canonical references:** `MAYHOA_ART_STYLE_SPEC.vi.md`, `FARM_ASSET_GENERATION_PLAN.vi.md`  
**Purpose:** Checklist và work partition để nhiều sub-agent generate các plant assets còn thiếu mà không overlap.

---

## 1. Snapshot hiện tại

Đã kiểm tra trực tiếp `masters/farm/`.

### Đã hoàn tất

Field crops — 6/6 species, mỗi species đủ 5 stage:

- [x] rice
- [x] corn
- [x] carrot
- [x] thien-ly
- [x] ngo-gai
- [x] mint

Fruit trees đã hoàn tất — 6/10 tree/perennial species trong roadmap:

- [x] mango
- [x] pomelo
- [x] lemon
- [x] star-apple
- [x] rambutan
- [x] lychee

### Còn phải generate

- [x] coconut — 5 images
- [x] dragon-fruit — 5 images
- [x] coffee — 5 images
- [x] rubber — 5 images
- [x] lotus — 5 images
- [x] water-mimosa — 5 images
- [x] water-spinach — 5 images

**Remaining total: 7 species / 35 master images.**

---

## 2. Parallelization rule

Mỗi species là một task độc lập và mặc định giao cho **một sub-agent riêng**.

Không chia nhiều agent cùng generate các stage của cùng một species vì 5 stage cần:

- cùng canvas size;
- cùng root-origin / gameplay anchor;
- cùng visual language;
- tăng kích thước tuần tự;
- giữ morphology nhất quán xuyên suốt lifecycle.

Recommended parallel layout:

```text
Agent A -> coconut
Agent B -> dragon-fruit
Agent C -> coffee
Agent D -> rubber
Agent E -> lotus
Agent F -> water-mimosa
Agent G -> water-spinach
```

Các task ghi vào destination path riêng nên có thể generate/QC song song mà không conflict file.

---

## 3. Global generation contract

Mọi sub-agent phải đọc và tuân theo:

1. `MAYHOA_ART_STYLE_SPEC.vi.md`
2. `FARM_ASSET_GENERATION_PLAN.vi.md`

Các rule bắt buộc:

- [ ] Mỗi species output **đúng 5 ảnh độc lập**; không contact sheet, không sprite sheet, không ghép 5 stage vào một ảnh.
- [ ] Background transparent sạch.
- [ ] Không bake soil, ground tile, pond surface, pond edge hoặc scene background vào plant master.
- [ ] 5 ảnh của cùng species phải dùng cùng canvas/aspect ratio.
- [ ] Root-origin / gameplay anchor phải giữ **cùng tọa độ** xuyên suốt 5 stage.
- [ ] Không center từng stage theo bounding box riêng.
- [ ] Kích thước và structural complexity phải tăng rõ theo thứ tự stage 01 < 02 < 03 < 04 < 05.
- [ ] Không chỉ scale cùng một hình; mỗi stage phải phát triển cấu trúc thật.
- [ ] Stage 02 phải đúng là sapling/sprout stage, không hoa, không trái.
- [ ] Stage 03 là young vegetative stage, không hoa, không trái.
- [ ] Harvest focal point chỉ xuất hiện ở stage cuối, trừ khi species-specific lifecycle explicit yêu cầu khác.
- [ ] Không text, UI label, watermark hoặc decorative clutter.
- [ ] Lighting upper-left, soft painterly rendering, selective dark-chromatic outlines, organic asymmetry.
- [ ] Species identity phải đọc rõ ở gameplay size.

### Tree/perennial canvas target

- Normal tree/perennial master: `1024x1024`.
- Tall/special tree: có thể dùng `1024x1280` nếu cần, nhưng toàn bộ 5 stage của cùng species phải giống nhau.

### Aquatic crop canvas target

- Mặc định `768x768`.
- Lotus có thể dùng `1024x1024` nếu cần breathing room.
- Cùng waterline/root anchor xuyên suốt 5 stage.

---

## 4. Task checklist — Special Structure Pack

### TASK TREE-COCONUT — Coconut / Dừa

**Destination:** `masters/farm/trees/coconut/`

- [ ] `coconut_stage-01_sprout_v01.png`
- [ ] `coconut_stage-02_sapling_v01.png`
- [ ] `coconut_stage-03_young_v01.png`
- [ ] `coconut_stage-04_mature_v01.png`
- [ ] `coconut_stage-05_fruiting_v01.png`

Species-specific notes:

- stage 01–02 phải nhỏ, trunk chưa phát triển thành palm trunk trưởng thành;
- stage 03 bắt đầu đọc rõ coconut palm silhouette nhưng chưa có fruit;
- stage 04 có crown trưởng thành hơn, chưa harvest-ready;
- stage 05 có coconut clusters vừa đủ để nhận diện, không overload canopy;
- giữ root/base anchor tuyệt đối ổn định dù chiều cao tăng mạnh.

Acceptance:

- [ ] 5 separate files.
- [ ] Same anchor.
- [ ] Monotonic height/crown growth.
- [ ] No coconut fruit before stage 05.
- [ ] No soil baked into sprite.

---

### TASK TREE-DRAGON-FRUIT — Dragon Fruit / Thanh long

**Destination:** `masters/farm/trees/dragon-fruit/`

- [ ] `dragon-fruit_stage-01_sprout_v01.png`
- [ ] `dragon-fruit_stage-02_sapling_v01.png`
- [ ] `dragon-fruit_stage-03_young_v01.png`
- [ ] `dragon-fruit_stage-04_flowering_v01.png`
- [ ] `dragon-fruit_stage-05_fruiting_v01.png`

Species-specific notes:

- lifecycle phải thể hiện rõ cấu trúc cactus climbing/branching;
- nếu dùng support post/trellis như một phần cấu trúc canh tác canonical thì support phải nhất quán giữa các stage và không được biến thành environment scene;
- stage 02 không hoa/trái;
- stage 03 có nhiều segment hơn nhưng vẫn vegetative;
- stage 04 mới bắt đầu flower;
- stage 05 có dragon fruit vừa đủ để nhận diện.

Acceptance:

- [ ] 5 separate files.
- [ ] Same base/support anchor.
- [ ] Clear structural growth, not scaled duplicates.
- [ ] No flower before stage 04.
- [ ] No fruit before stage 05.

---

## 5. Task checklist — Industrial / Perennial Pack

### TASK TREE-COFFEE — Coffee / Cà phê

**Destination:** `masters/farm/trees/coffee/`

- [ ] `coffee_stage-01_sprout_v01.png`
- [ ] `coffee_stage-02_sapling_v01.png`
- [ ] `coffee_stage-03_young_v01.png`
- [ ] `coffee_stage-04_flowering_v01.png`
- [ ] `coffee_stage-05_berry_v01.png`

Species-specific notes:

- shrub/tree form thấp hơn major fruit trees;
- leaf arrangement và branching phải đọc giống coffee plant;
- stage 01–03 hoàn toàn vegetative;
- stage 04 có white coffee flowers vừa phải;
- stage 05 có ripe berry focal points, không biến thành cây phủ kín berries.

Acceptance:

- [ ] 5 separate files.
- [ ] Same root anchor.
- [ ] Stage sizes tăng đều.
- [ ] No flower before stage 04.
- [ ] No berry before stage 05.

---

### TASK TREE-RUBBER — Rubber / Cao su

**Destination:** `masters/farm/trees/rubber/`

- [x] `rubber_stage-01_sprout_v01.png`
- [x] `rubber_stage-02_sapling_v01.png`
- [x] `rubber_stage-03_young_v01.png`
- [x] `rubber_stage-04_mature_v01.png`
- [x] `rubber_stage-05_tapping_v01.png`

Species-specific notes:

- trunk development là tín hiệu lifecycle chính;
- stage 01–03 không tapping hardware;
- stage 04 là mature tree, chưa harvest representation;
- stage 05 có tapping cut/cup representation đủ rõ để hiểu gameplay, nhưng không excessive industrial detail;
- tree vẫn phải giữ Mayhoa cute/readable style, không photorealistic plantation rendering.

Acceptance:

- [ ] 5 separate files.
- [ ] Same root anchor.
- [ ] Trunk thickness/height tăng hợp lý.
- [ ] No tapping state before stage 05.
- [ ] No soil or plantation scene baked in.

---

## 6. Task checklist — Aquatic Crop Area Pack

### TASK AQUATIC-LOTUS — Lotus / Sen

**Destination:** `masters/farm/aquatic-crops/lotus/`

- [ ] `lotus_stage-01_planted_v01.png`
- [ ] `lotus_stage-02_sprout_v01.png`
- [ ] `lotus_stage-03_young_v01.png`
- [ ] `lotus_stage-04_budding_v01.png`
- [ ] `lotus_stage-05_flowering_v01.png`

Species-specific notes:

- plant artwork tách khỏi water surface và pond edge;
- waterline/root anchor cố định;
- stage 01–03 phát triển leaf/stem structure trước khi budding;
- stage 04 có bud focal point;
- stage 05 đọc rõ lotus identity qua lotus leaves + flower, có thể có seed-pod nhẹ nếu không làm rối silhouette;
- `lotus_flower`, `lotus_rhizome`, `lotus_stem`, `lotus_seed` là gameplay item mapping, không phải 4 lifecycle sprite riêng; artwork thu hoạch/inventory của cả 4 output này được defer sang item/inventory phase sau. Task lotus hiện tại chỉ cần đúng 5 lifecycle/world assets ở trên.

Acceptance:

- [ ] 5 separate files.
- [ ] Same waterline/root anchor.
- [ ] No baked water/pond/ripple.
- [ ] No flower before stage 05; stage 04 chỉ budding.
- [ ] Stage 05 silhouette vẫn readable ở runtime size.

---

### TASK AQUATIC-WATER-MIMOSA — Water Mimosa / Rau nhút

**Destination:** `masters/farm/aquatic-crops/water-mimosa/`

- [x] `water-mimosa_stage-01_planted_v01.png`
- [x] `water-mimosa_stage-02_sprout_v01.png`
- [x] `water-mimosa_stage-03_young_v01.png`
- [x] `water-mimosa_stage-04_mature_v01.png`
- [x] `water-mimosa_stage-05_harvestable_v01.png`

Species-specific notes:

- form thiên về cụm ngang trên waterline;
- growth chủ yếu thể hiện bằng số lượng stem, leaf density và spread;
- giữ identity của rau nhút, không để silhouette bị nhầm với water spinach;
- không bake water surface.

Acceptance:

- [ ] 5 separate files.
- [ ] Same waterline/root anchor.
- [ ] Horizontal spread tăng tuần tự.
- [ ] Distinct species identity.
- [ ] No water/pond baked into sprite.

---

### TASK AQUATIC-WATER-SPINACH — Water Spinach / Rau muống

**Destination:** `masters/farm/aquatic-crops/water-spinach/`

- [x] `water-spinach_stage-01_planted_v01.png`
- [x] `water-spinach_stage-02_sprout_v01.png`
- [x] `water-spinach_stage-03_young_v01.png`
- [x] `water-spinach_stage-04_mature_v01.png`
- [x] `water-spinach_stage-05_harvestable_v01.png`

Species-specific notes:

- form lan ngang nhưng stem/leaf language phải khác rau nhút;
- stage progression bằng stem count, leaf mass và spread;
- harvestable stage trông tươi, edible, không overgrown/messy như weed;
- không bake water surface.

Acceptance:

- [ ] 5 separate files.
- [ ] Same waterline/root anchor.
- [ ] Structural growth rõ ở từng stage.
- [ ] Distinct from water-mimosa at gameplay size.
- [ ] No water/pond baked into sprite.

---

## 7. Recommended execution waves

Tất cả 7 species có thể chạy song song nếu đủ agent. Nếu muốn giảm rủi ro visual drift, dùng 2 wave:

### Wave A — tree/perennial

- [ ] TREE-COCONUT
- [ ] TREE-DRAGON-FRUIT
- [ ] TREE-COFFEE
- [x] TREE-RUBBER

Sau khi Wave A hoàn tất:

- [ ] cross-QC scale giữa 4 species với mango/pomelo/lemon reference;
- [ ] confirm root anchor consistency trong từng set;
- [ ] approve trước khi sync canonical masters.

### Wave B — aquatic crops

- [ ] AQUATIC-LOTUS
- [x] AQUATIC-WATER-MIMOSA
- [x] AQUATIC-WATER-SPINACH

Sau khi Wave B hoàn tất:

- [ ] cross-QC waterline anchors;
- [ ] test composition trên neutral water tile;
- [ ] verify lotus / rau nhút / rau muống không bị nhầm silhouette.

---

## 8. Per-agent handoff template

Mỗi sub-agent nhận đúng một task ở trên và báo cáo theo format:

```text
Task ID:
Species:
Destination:
Generated files: 5/5
Canvas:
Anchor rule verified: yes/no
Stage order verified: yes/no
Lifecycle contamination found: yes/no
Transparent background verified: yes/no
Style spec verified: yes/no
Open issues:
Ready for approval: yes/no
```

Sub-agent không được tự ý đổi naming convention hoặc ghi file sang task của agent khác.

---

## 9. Final integration checklist

Chỉ tick hoàn tất species sau khi đủ cả generation + QC + sync.

### Tree/perennial

- [ ] coconut 5/5 approved and synced
- [ ] dragon-fruit 5/5 approved and synced
- [ ] coffee 5/5 approved and synced
- [x] rubber 5/5 approved and synced

### Aquatic crops

- [ ] lotus 5/5 approved and synced
- [ ] water-mimosa 5/5 approved and synced
- [ ] water-spinach 5/5 approved and synced

### Pack-level QC

- [ ] Remaining 35/35 master images exist.
- [ ] Every species has exactly 5 lifecycle images.
- [ ] No composite/contact-sheet file used as canonical master.
- [ ] Same-anchor rule passes inside every lifecycle set.
- [ ] Stage growth is monotonic for every species.
- [ ] No early-stage fruit/flower contamination.
- [ ] No soil/water/environment baked into plant masters.
- [ ] Cross-species world scale is coherent.
- [ ] Runtime silhouette remains readable.
- [ ] Approved assets are ready for runtime export/optimization.

---

## 10. Out of scope for this plan

Không bao gồm:

- weeds;
- pests;
- farming tools;
- inventory item artwork;
- pond/water surface tiles;
- runtime resizing/optimization;
- optional regrowing states;
- animation frames ngoài core 5-stage lifecycle.

Các phần trên vẫn thuộc roadmap farm tổng nhưng không phải **remaining plant generation** trong checklist này.

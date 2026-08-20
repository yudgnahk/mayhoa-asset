# Mayhoa Farm Asset Generation Plan

**Status:** Production roadmap  
**Project:** Mayhoa  
**Art style:** Mayhoa Nostalgic Hand-Painted Farm Sprite  
**Language:** English  

This document defines the production plan for the first Mayhoa farm artwork set. Every asset in this plan must follow `MAYHOA_ART_STYLE_SPEC.en.md`.

---

## 1. Goal

Build the foundational farm artwork set for direct use in the game, including:

- soil plots and soil states;
- short-cycle crops;
- fruit trees and perennial plants;
- weeds that appear on farm plots;
- pests and infestation overlays;
- farm interaction tools;
- a consistent size, naming, and export system suitable for PixiJS.

Execution principles:

1. Do not generate the entire asset set at once.
2. Lock visual calibration first.
3. Generate sequentially by production batch.
4. Every batch must pass QC before the next batch starts.
5. Growth stages must change silhouette, not simply scale one image.
6. Master artwork and runtime artwork are separate deliverables.

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

Farm plots and soil states.

### 2.2 `farm/crops`

Short-cycle, low, or medium-height crops:

- rice
- corn
- carrot
- thien-ly / Telosma cordata flower vine
- ngo-gai / culantro
- mint

### 2.3 `farm/trees`

Fruit trees and perennial plants:

- mango
- pomelo
- lemon
- coconut
- dragon fruit
- coffee
- star apple
- rubber
- rambutan
- lychee

### 2.4 `farm/weeds`

Separate weed overlays placed together with crops on farm plots.

### 2.5 `farm/pests`

Pests, bugs, and infestation overlays.

### 2.6 `farm/tools`

- harvest hand
- watering can
- pest catcher
- pruning shears
- shovel

---

## 3. Plant grouping by visual structure

### 3.1 Field crops

```text
rice
corn
carrot
thien-ly
ngo-gai
mint
```

Characteristics:

- footprint mainly fits within one plot;
- low or medium silhouette;
- readable at gameplay scale;
- default 5-stage growth system.

### 3.2 Fruit trees

```text
mango
pomelo
lemon
star-apple
rambutan
lychee
```

Characteristics:

- clear trunk and branch logic;
- canopy built from foliage masses;
- fruit count only needs to be sufficient for species recognition;
- consistent relative scale across the tree family.

### 3.3 Special tropical structures

```text
coconut
dragon-fruit
```

These require their own batch because their silhouettes differ strongly from conventional fruit trees.

### 3.4 Industrial / perennial crops

```text
coffee
rubber
```

Coffee uses a shrub/tree form with visible berry focal points. Rubber has a taller trunk and may need a tapping harvest state if gameplay supports that mechanic.

---

## 4. Growth stage system

### 4.1 Short-cycle crops — 5 stages

```text
stage-01_seeded
stage-02_sprout
stage-03_young
stage-04_mature
stage-05_harvestable
```

Every stage must change silhouette and structural complexity.

### 4.2 Fruit trees / perennials — default 4 stages

```text
stage-01_sapling
stage-02_young
stage-03_mature
stage-04_harvestable
```

`harvestable` may be represented as `fruiting`, `berry`, or `tapping` depending on the plant.

If gameplay later needs a flowering state, add it as a separate stage rather than baking it into mature.

---

## 5. Size system

Do not ship master artwork directly as runtime textures.

### 5.1 Master generation size

| Asset class | Master target |
|---|---:|
| Small crop / weed / pest | 512×512 |
| Medium crop / herb | 768×768 |
| Tree / animal-sized farm asset | 1024×1024 |
| Tall/special tree | 1024×1280 or square master with padding |
| Tool icon | 512×512 |

### 5.2 Runtime semantic size classes

| Class | Suggested display range | Typical use |
|---|---:|---|
| S | 64–96 px | weed, pest, tiny growth stage, small tool |
| M | 128–160 px | rice, carrot, herbs, mature low crop |
| L | 192–256 px | corn, coffee, dragon fruit |
| XL | 256–384 px | mango, pomelo, coconut, rubber, fruit trees |

Final runtime size may be tuned to camera and world scale, but perceived scale must stay consistent across related assets.

---

## 6. Soil system

`farm/soil` is the visual calibration foundation for the whole farm set.

### Required states

```text
soil_empty
soil_tilled
soil_wet
soil_planted
soil_dry
soil_harvested
```

### Rules

- crops, weeds, and pests must be composable on the standard soil tile;
- wet/dry states must read clearly without becoming oversaturated;
- footprint and camera angle remain fixed;
- weeds and pests are not baked permanently into soil textures;
- crop shadows must match the soil grounding system.

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

Rules:

- separate overlays;
- messier silhouette than the main crop;
- must not obscure crop identity;
- green treatment should differ enough from crop foliage to be readable;
- runtime may apply light random variant/rotation behavior.

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

Initial priority:

```text
caterpillar_single
caterpillar_cluster
beetle_single
aphid_cluster
```

Rules:

- slightly exaggerate scale for gameplay readability;
- pest sprite and infestation marker may be separate assets;
- avoid realistic gross insect treatment or horror styling;
- keep the cute/readable Mayhoa visual language.

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

- gameplay interaction icons rather than realistic equipment illustrations;
- extremely clear silhouettes;
- slight 3/4 angle when appropriate;
- slightly higher contrast than world assets;
- do not bake button backgrounds into the artwork;
- hover/disabled/pressed states should preferably be handled by UI/runtime instead of separate generated artwork.

### Minimal artwork states

```text
idle
active   # only when interaction animation needs a separate sprite
```

---

## 10. Recommended folder structure

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

`masters/` stores high-quality source artwork. `runtime/` stores resized and optimized game-ready exports.

---

## 11. Naming convention

Pattern:

```text
<asset>_<state-or-stage>_v<nn>.png
```

Examples:

```text
rice_stage-01_seeded_v01.png
rice_stage-05_harvestable_v01.png
mango_stage-01_sapling_v01.png
mango_stage-04_fruiting_v01.png
weed_small_v01.png
pest_caterpillar_single_v01.png
tool_watering-can_idle_v01.png
```

Do not encode resolution directly into logical filenames. Separate resolutions through runtime folders such as `1x/` and `2x/`.

---

## 12. Production phases

# Phase 0 — Calibration Set

Goal: lock perspective, scale, outlines, palette, shadow, foliage density, and perceived detail level before full production begins.

Generate representative states first:

1. `soil_tilled`
2. `rice_stage-05_harvestable`
3. `corn_stage-05_harvestable`
4. `mango_stage-04_fruiting`
5. `weed_small_01`
6. `caterpillar_single`
7. `tool_watering-can_idle`

### Exit criteria

Move to Phase 1 only when all seven assets:

- clearly belong to the same game;
- share the same lighting logic;
- have plausible relative scale;
- use consistent outline and detail density;
- can be placed with the same soil tile without perspective/camera mismatch;
- remain readable at runtime size.

---

# Phase 1 — Soil Foundation

Generate the full soil state pack:

- empty
- tilled
- wet
- planted
- dry
- harvested

Then lock the soil tile as the visual reference foundation for crop production.

---

# Phase 2 — Core Crop Pack

Generate full growth stages for:

1. rice
2. corn
3. carrot

Five stages each.

This phase locks the growth-stage visual language for the crop system.

---

# Phase 3 — Herb / Low Crop Pack

Generate full growth stages for:

1. thien-ly
2. ngo-gai
3. mint

Use five stages each unless gameplay later requires fewer.

---

# Phase 4 — Core Fruit Tree Pack

Generate:

1. mango
2. pomelo
3. lemon
4. star apple

Four stages each:

- sapling
- young
- mature
- fruiting/harvestable

---

# Phase 5 — Tropical Fruit Tree Pack

Generate:

1. rambutan
2. lychee

Four stages each.

---

# Phase 6 — Special Structure Pack

Generate:

1. coconut
2. dragon fruit

Each needs individual footprint and vertical-scale calibration while still following the shared world scale.

---

# Phase 7 — Industrial / Perennial Pack

Generate:

1. coffee
2. rubber

Coffee harvest state should use berry focal points. Rubber harvest state may use a tapping representation if gameplay confirms that mechanic.

---

# Phase 8 — Weed Pack

Generate the full weed set:

- 2 small
- 2 medium
- 1 dense

Test overlays with at least rice, corn, carrot, and a fruit-tree plot when applicable.

---

# Phase 9 — Pest Pack

Generate:

- caterpillar single
- caterpillar cluster
- beetle single
- aphid cluster
- snail
- leaf bug

Test on low foliage crops, tall crops, and tree foliage.

---

# Phase 10 — Farming Tool Pack

Generate:

- harvest hand
- watering can
- pest catcher
- pruning shears
- shovel

The tool pack must be evaluated at UI interaction size, not using crop/tree world scale.

---

## 13. Batch execution rule

Every phase follows this loop:

```text
PLAN -> GENERATE -> REVIEW -> REVISE -> APPROVE -> OPTIMIZE -> COMMIT
```

Do not start production for the next phase until the current phase passes acceptance criteria, unless an asset is explicitly exploratory and will not be merged into the canonical production set.

---

## 14. QC checklist for every asset

- correct species / object identity;
- correct Mayhoa art style;
- readable silhouette at gameplay size;
- not overly vector-clean;
- not glossy;
- no neon palette;
- no excessive detail;
- selective dark-chromatic outlines;
- consistent upper-left lighting;
- soft shadows;
- believable organic asymmetry;
- clear crop/tree structural logic;
- relative scale matches the soil tile and neighboring assets;
- clean transparent background;
- no unnecessary text / UI / scene background;
- sufficient breathing room in master art;
- runtime export has no halo, blur, or silhouette loss.

---

## 15. Git workflow

### Per production batch

Commit each approved phase/batch separately.

Suggested commit messages:

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

### Do not commit

- rejected generations;
- obsolete duplicate variants;
- masters with broken composition;
- runtime exports that have not passed QC.

If exploratory generations need to be preserved, keep them in a separate non-canonical area.

---

## 16. Estimated initial scope

Approximate initial production masters:

- Soil: ~6
- Field crops: ~30
- Trees/perennials: ~40
- Weeds: ~5
- Pests: ~6
- Tools: ~5

Total: approximately **90+ master sprites**, excluding revisions and optional UI/animation variants.

---

## 17. Official execution order

Default sequence:

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

After Phase 0 is approved, artwork should be generated sequentially in this order unless gameplay priority changes.

---

## 18. First production task

**Task ID:** `FARM-P0-CALIBRATION`

Generate seven representative assets:

```text
soil_tilled
rice_stage-05_harvestable
corn_stage-05_harvestable
mango_stage-04_fruiting
weed_small_01
pest_caterpillar_single_v01
tool_watering-can_idle_v01
```

The purpose of this task is not asset quantity. It is to lock the visual language for the entire farm pack.

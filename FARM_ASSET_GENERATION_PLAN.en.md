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
- aquatic crops for pond / water-surface farming areas;
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
  aquatic-crops/
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

### 2.3 `farm/aquatic-crops`

Aquatic or semi-aquatic crops planted on water slots rather than soil tiles:

- lotus / sen (`Nelumbo nucifera`)
- water mimosa / rau nhut (`Neptunia oleracea`)
- water spinach / rau muong (`Ipomoea aquatica`)

Plant artwork must stay separate from water surfaces, pond edges, and ripple FX so it can compose with a dedicated pond/water system.

### 2.4 `farm/trees`

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

### 2.5 `farm/weeds`

Separate weed overlays placed together with crops on farm plots.

### 2.6 `farm/pests`

Pests, bugs, and infestation overlays.

### 2.7 `farm/tools`

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

### 3.2 Aquatic crops

```text
lotus
water-mimosa
water-spinach
```

Characteristics:

- anchor to a shared waterline / root origin rather than canvas center;
- never bake water, pond edges, soil, or ripple FX into the plant sprite;
- lotus uses a taller/wider silhouette while water mimosa and water spinach spread more horizontally;
- foliage may extend slightly outside the visual slot, but the gameplay footprint must remain stable;
- use the default 5-stage lifecycle, with real structural development rather than scaled copies.

### 3.3 Fruit trees

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

### 3.4 Special tropical structures

```text
coconut
dragon-fruit
```

These require their own batch because their silhouettes differ strongly from conventional fruit trees.

### 3.5 Industrial / perennial crops

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

### 4.2 Aquatic crops — 5 stages

```text
stage-01_planted
stage-02_sprout
stage-03_young
stage-04_mature
stage-05_harvestable
```

Visual state names may specialize by species. Lotus may use `stage-04_budding` and `stage-05_flowering`, while water mimosa and water spinach communicate maturity mainly through foliage density and spread.

Lotus supports multiple harvest outputs from the same species:

```text
lotus_flower
lotus_rhizome   # lotus root / cu sen
lotus_stem      # ngo sen
lotus_seed
```

These are gameplay/item IDs, not four independent lifecycle sprite sets. **The current plant/aquatic scope requires only the 5 lotus world lifecycle assets** (`planted`, `sprout`, `young`, `budding`, `flowering`). Harvest/inventory artwork for all four outputs — `lotus_flower`, `lotus_rhizome`, `lotus_stem`, and `lotus_seed` — **is deferred to a later item/inventory phase and must not be generated as part of the current 5-stage lifecycle set**. If gameplay later needs separate harvest timing, optional late-stage variants/overlays such as `flowering` or `seed-pod` may be added. Submerged rhizomes must not be exposed in the normal world sprite.

Water mimosa and water spinach primarily harvest tender stems/leaves. If gameplay later supports cut-and-regrow behavior, add a `regrowing` state outside the core 5-stage set.

### 4.3 Fruit trees / perennials — default 5 stages

```text
stage-01_sprout
stage-02_sapling
stage-03_young
stage-04_flowering-or-mature
stage-05_harvestable
```

`harvestable` may be represented as `fruiting`, `berry`, or `tapping` depending on the plant.

#### 4.3.1 Hard generation contract for fruit trees

Every generation run for a 5-stage fruit tree / perennial lifecycle must follow these rules:

1. **5 stages = 5 separate images.** Output exactly five independent image assets, one image containing one stage. Do not combine all five trees into one image, contact sheet, or sprite sheet in place of the five master images.
2. **Same canvas, same root anchor.** All five images must use the same canvas size / aspect ratio and the same `root-origin` / lowest trunk-contact coordinate. Do not center each stage independently by its bounding box; the gameplay anchor is the fixed point.
3. **Monotonic scale progression.** Perceived height, canopy spread, and structural complexity must clearly increase in the order `stage-01 < stage-02 < stage-03 < stage-04 < stage-05`. An early stage must never appear as large as, or larger than, a later mature stage.
4. **Do not only scale one drawing.** Each stage must show real structural development: thicker trunk, clearer branching logic, more complex canopy, and lifecycle-appropriate silhouette changes.
5. **Stage 01 — sprout:** smallest stage; early stem/trunk, very limited foliage, no mature canopy; no flowers and no fruit.
6. **Stage 02 — sapling:** clearly juvenile; slim trunk, a few branches, small canopy; **no flowers and absolutely no fruit**.
7. **Stage 03 — young:** more developed branching and canopy than stage 02 but still not mature; **no flowers and no fruit**.
8. **Stage 04 — flowering-or-mature:** more mature than stage 03. For species with a flowering state, flowers begin here; do not render harvest-ready fruit unless the species gameplay/spec explicitly requires otherwise.
9. **Stage 05 — harvestable / fruiting:** largest and most complete stage; species-appropriate fruit/berry/harvest focal points appear here.
10. If stage 05 or another fruit-bearing reference is used to preserve species identity, use it only for morphology, leaf/trunk language, and fruit identity; **do not copy flowers or fruit backward into stages 01–03**.
11. Tree sprites must not bake soil, pots, ground tiles, or environment into the master artwork unless the asset spec explicitly requires it.

A full fruit-tree generation prompt must explicitly contain equivalent constraints:

```text
OUTPUT REQUIREMENT: Generate exactly five separate image assets, not one composite image and not a sprite sheet. One output image per lifecycle stage: stage-01, stage-02, stage-03, stage-04, stage-05.

ANCHOR REQUIREMENT: All five images must use the exact same canvas size and the exact same root-origin coordinate. The lowest/root contact point of the trunk must remain fixed across all five outputs. Do not center each tree independently.

GROWTH REQUIREMENT: Tree size and structural complexity must increase monotonically from stage 01 through stage 05. Each successive stage must be visibly larger than the previous stage while preserving believable biological growth.

LIFECYCLE REQUIREMENT: stage-02 is strictly a sapling — foliage only, no flowers and absolutely no fruit. stage-03 is a young vegetative tree — no flowers and no fruit. Flowers begin only at stage-04 when applicable; harvestable fruit appears only at stage-05.
```

---

## 5. Size system

Do not ship master artwork directly as runtime textures.

### 5.1 Master generation size

| Asset class | Master target |
|---|---:|
| Small crop / weed / pest | 512×512 |
| Medium crop / herb | 768×768 |
| Aquatic crop | 768×768; lotus may use 1024×1024 when extra canopy/flower breathing room is needed |
| Tree / animal-sized farm asset | 1024×1024 |
| Tall/special tree | 1024×1280 or square master with padding |
| Tool icon | 512×512 |

### 5.2 Runtime semantic size classes

| Class | Suggested display range | Typical use |
|---|---:|---|
| S | 64–96 px | weed, pest, tiny growth stage, small tool |
| M | 128–160 px | rice, carrot, herbs, water mimosa, water spinach, mature low crop |
| L | 192–256 px | corn, coffee, dragon fruit, lotus |
| XL | 256–384 px | mango, pomelo, coconut, rubber, fruit trees |

Final runtime size may be tuned to camera and world scale, but perceived scale must stay consistent across related assets.

---

## 6. Grounding / surface systems

### 6.1 Soil system

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

### 6.2 Aquatic crop area

The aquatic crop area is a shallow-water / pond farming surface for lotus, water mimosa, and water spinach.

Rules:

- `farm/aquatic-crops` contains plant artwork only;
- water surfaces / pond tiles, pond edges, and ripple FX belong to a separate environment/water system and must not be baked into crop masters;
- all stages of one species share the same waterline/root anchor so sprite replacement does not jump;
- do not center plants by canvas; preserve a stable gameplay anchor;
- contact ripples/shadows are optional overlays or runtime FX;
- do not expose submerged rhizomes/roots in normal world sprites;
- when sharing a pond with fish gameplay, foliage must not cover so much water that fish or interaction markers lose readability;
- preserve the same camera angle, upper-left lighting, and perceived world scale as the rest of the farm.

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
mango_stage-01_sprout_v01.png
mango_stage-04_flowering_v01.png
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
4. `mango_stage-05_fruiting`
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

Five stages each:

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

Five stages each, following the standard fruit-tree/perennial lifecycle.

---

# Phase 6 — Special Structure Pack

Generate:

1. coconut
2. dragon fruit

Five stages each; state names may specialize for each species structure.

Each needs individual footprint and vertical-scale calibration while still following the shared world scale.

---

# Phase 7 — Industrial / Perennial Pack

Generate:

1. coffee
2. rubber

Five stages each, following the standard perennial lifecycle.

Coffee harvest state should use berry focal points. Rubber harvest state may use a tapping representation if gameplay confirms that mechanic.

---

# Phase 8 — Aquatic Crop Area Pack

Generate full growth stages for:

1. lotus
2. water-mimosa
3. water-spinach

Five stages each.

Specific acceptance requirements:

- stable shared waterline/root anchor across every stage;
- no baked water surface or pond edge in plant sprites;
- final lotus stage reads clearly through leaves plus a flower or seed-pod focal point;
- lotus gameplay mapping supports `lotus_flower`, `lotus_rhizome`, `lotus_stem`, and `lotus_seed` without requiring four independent lifecycles;
- water mimosa and water spinach must remain visually distinct at runtime size;
- test composition on at least one neutral water tile before approval.

---

# Phase 9 — Weed Pack

Generate the full weed set:

- 2 small
- 2 medium
- 1 dense

Test overlays with at least rice, corn, carrot, and a fruit-tree plot when applicable.

---

# Phase 10 — Pest Pack

Generate:

- caterpillar single
- caterpillar cluster
- beetle single
- aphid cluster
- snail
- leaf bug

Test on low foliage crops, tall crops, and tree foliage.

---

# Phase 11 — Farming Tool Pack

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
PLAN -> GENERATE -> REVIEW -> REVISE -> APPROVE -> SYNC -> VERIFY -> OPTIMIZE -> COMMIT
```

### Asset sync transport

Claude-in-Chrome downloads images from ChatGPT straight to the local disk. **No Google Drive, no `gws`.**

Canonical transport flow:

```text
ChatGPT Create image output
-> open the image in the fullscreen viewer, click "Save"
-> the file lands in ~/Downloads as "ChatGPT Image <date time>.png"
-> identify new files by timestamp
-> verify MIME, dimensions, real alpha
-> move to `.ai-bridge/<species>/`; only approved assets go to `masters/...`
```

Identifying new files safely for a multi-image batch — set the marker **before** clicking Save:

```bash
MARK=$(mktemp); touch "$MARK"
# ... click Save for each image in stage order ...
find ~/Downloads -name 'ChatGPT Image*.png' -newer "$MARK" -print0 | xargs -0 ls -tr
# oldest -> newest matches the order you clicked
```

Rules:

- The download button is labelled **"Save"** and exists only in the fullscreen viewer (same bar as Remove BG / Erase). There is NO download button in the chat pane.
- This only works while Chrome and the repo are on the **same machine** — true for the current setup. Split them and you must go back to a staging layer.
- Do not rely on ChatGPT `openai/fileParams` for canonical asset transport.
- Do not invoke local Codex, Codex CLI, `codex exec`, or any Codex-backed executor for asset syncing.
- Keep raws and prompts under `.ai-bridge/<species>/`; only approved assets belong under `masters/`.
- Verify the downloaded file is the expected image type and carries real alpha before accepting it.

> **History:** before 2026-09-05 this ran through Google Drive + `gws`, because CodexPro2 could not
> accept binaries directly from Create image. Moving to Claude-in-Chrome removed that leg entirely:
> one fewer connector call, one fewer Allow click, and no OAuth-token expiry risk — the `gws` token
> had in fact been revoked exactly when it was needed (2026-09-05).

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
assets: add aquatic crop area pack
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
- Aquatic crops: ~15
- Trees/perennials: ~50
- Weeds: ~5
- Pests: ~6
- Tools: ~5

Total: approximately **115+ master sprites**, excluding revisions, harvest-item artwork, and optional UI/animation variants.

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
Phase 8  Aquatic Crop Area Pack
Phase 9  Weed Pack
Phase 10 Pest Pack
Phase 11 Farming Tool Pack
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
mango_stage-05_fruiting
weed_small_01
pest_caterpillar_single_v01
tool_watering-can_idle_v01
```

The purpose of this task is not asset quantity. It is to lock the visual language for the entire farm pack.

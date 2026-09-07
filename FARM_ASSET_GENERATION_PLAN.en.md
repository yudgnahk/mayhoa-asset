# Mayhoa Farm Asset Generation Plan

**Language:** [Tiếng Việt](FARM_ASSET_GENERATION_PLAN.vi.md) · English

**Status:** Production roadmap  
**Project:** Mayhoa  
**Art style:** Mayhoa Nostalgic Hand-Painted Farm Sprite  

This document defines the artwork generation plan for the first Mayhoa farm system. Every asset in this plan must follow `MAYHOA_ART_STYLE_SPEC.en.md`.

---

## Status and relationship to other documents

This document is **still active** for the roadmap part: asset taxonomy (§2–3), the growth-stage system (§4), the folder/naming convention (§10–11), production phases and the **official execution order** (§12, §17).

The **specific canvas/anchor content in §5 (Size system) has been superseded by `MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.en.md`** — that geometry spec is the source of truth for the real canvas/anchor measurements (for example, the crop anchor has changed relative to the values implied here). When the two documents disagree on geometry numbers, `MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.en.md` wins.

Operational note: the phase order in §17 (pest = Phase 10, tool = Phase 11, both placed after the tree/aquatic Phases 4–8) is the source of conflict `C-ART-02`, currently OPEN in the `mayhoa` repo — the demo's Gate A needs pest + tool earlier than this order prescribes. See `README.md` at the root of this repo for details.

---

## 1. Goal

Build the foundational farm artwork set that can be used directly in the game, including:

- soil plots and soil states;
- short-cycle crops;
- aquatic crops for water-surface / pond areas;
- fruit trees / perennial plants;
- weeds that appear on farm plots;
- pests, bugs, and infestation overlays;
- tools that interact with the farm;
- a size, naming, and export system suitable for PixiJS.

Execution principles:

1. Do not generate the entire asset set up front.
2. Lock visual calibration first.
3. Generate sequentially by batch.
4. Every batch must pass QC before the next batch starts.
5. Growth stages must change silhouette, not merely scale the same image.
6. Master assets and runtime assets are kept separate.

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

Short-cycle crops / low or medium-height plants:

- rice (Vietnamese: lúa nước)
- corn (Vietnamese: bắp)
- carrot
- tonkin-jasmine (Vietnamese: hoa thiên lý)
- culantro (Vietnamese: ngò gai)
- mint (Vietnamese: bạc hà)

### 2.3 `farm/aquatic-crops`

Aquatic or semi-aquatic crops planted on water slots rather than soil tiles:

- lotus (Vietnamese: sen) (`Nelumbo nucifera`)
- water-mimosa (Vietnamese: rau nhút) (`Neptunia oleracea`)
- water-spinach (Vietnamese: rau muống) (`Ipomoea aquatica`)

Plant artwork must stay separate from water surfaces, pond edges, and ripple FX so it can compose with a dedicated pond/water system.

### 2.4 `farm/trees`

Fruit trees and perennial plants:

- mango (Vietnamese: xoài)
- pomelo (Vietnamese: bưởi)
- lemon (Vietnamese: chanh)
- coconut (Vietnamese: dừa)
- dragon-fruit (Vietnamese: thanh long)
- coffee (Vietnamese: cà phê)
- star-apple (Vietnamese: vú sữa)
- rubber (Vietnamese: cao su)
- rambutan (Vietnamese: chôm chôm)
- lychee (Vietnamese: vải)

### 2.5 `farm/weeds`

Weeds are rendered as separate overlays and placed together with crops on the farm plot.

### 2.6 `farm/pests`

Pests, bugs, infestation overlays.

### 2.7 `farm/tools`

- harvest hand
- watering can
- pest catcher
- pruning shears
- shovel

---

## 3. Plant grouping by geometric structure

### 3.1 Field crops

```text
rice
corn
carrot
tonkin-jasmine
culantro
mint
```

Characteristics:

- footprint fits mainly within one farm plot;
- low or medium silhouette;
- reads clearly at gameplay size;
- uses the default 5-stage growth system.

### 3.2 Aquatic crops

```text
lotus
water-mimosa
water-spinach
```

Characteristics:

- anchor to a shared waterline / root-origin rather than the canvas center;
- do not bake water, pond edges, soil, or ripple FX into the plant sprite;
- lotus has a taller and wider silhouette, while water mimosa / water spinach lean toward horizontal clusters;
- foliage may extend slightly outside the geometric slot, but the gameplay footprint must remain stable;
- uses the 5-stage growth system, and each stage must develop real structure rather than scale the same image.

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

- clear trunk + branch logic;
- canopy built from foliage masses;
- fruit only needs to be sufficient for species recognition;
- relative scale must stay consistent across trees.

### 3.4 Special tropical structures

```text
coconut
dragon-fruit
```

These two assets need their own batch because their silhouettes differ strongly from conventional fruit trees.

### 3.5 Industrial / perennial crops

```text
coffee
rubber
```

Coffee has a shrub/tree form and berry focal points. Rubber has a taller trunk and may need a harvest/tapping state if gameplay supports it.

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

Visual state names may specialize by species. Lotus may use `stage-04_budding` and `stage-05_flowering`, while water mimosa / water spinach express maturity mainly through foliage density and spread.

Lotus supports multiple harvest outputs from the same species:

```text
lotus_flower    # lotus flower
lotus_rhizome   # lotus root
lotus_stem      # young lotus stem
lotus_seed      # lotus seed
```

These are gameplay/item IDs, not four independent lifecycle sprites. **The current plant/aquatic scope only requires the 5 lotus world lifecycle assets** (`planted`, `sprout`, `young`, `budding`, `flowering`). Harvest/inventory artwork for all four outputs `lotus_flower`, `lotus_rhizome`, `lotus_stem`, `lotus_seed` **is deferred to a later item/inventory phase and must not be generated together with the current 5-stage lifecycle set**. If gameplay later needs to distinguish harvest timing, a late-stage variant/overlay such as `flowering` or `seed-pod` may be added. Submerged rhizomes/roots are not exposed in the normal world sprite.

Water mimosa and water spinach harvest tender stems/leaves by default. If a cut-and-regrow mechanic is added later, add a `regrowing` state outside the core 5-stage set.

### 4.3 Fruit tree / perennial — default 5 stages

```text
stage-01_sprout
stage-02_sapling
stage-03_young
stage-04_flowering-or-mature
stage-05_harvestable
```

`harvestable` may be `fruiting`, `berry`, or `tapping` depending on the plant.

#### 4.3.1 Hard generation contract for fruit trees

Every time a fruit tree/perennial is generated on the 5-stage lifecycle, these rules must be followed:

1. **5 stages = 5 independent images.** Exactly five separate image assets must be output, each image containing exactly one stage. Do not combine five trees into one image, do not create a contact sheet, do not create a sprite sheet in place of the five master images.
2. **Same canvas, same root anchor.** All five images must use the same canvas size / aspect ratio and the same `root-origin` / lowest trunk-contact coordinate. Do not center each stage by its own bounding box; the gameplay anchor is the fixed point.
3. **Monotonically increasing scale.** Perceived height, canopy spread, and structural complexity must clearly increase in the order `stage-01 < stage-02 < stage-03 < stage-04 < stage-05`. Each stage must be reasonably larger than the previous one; no early stage may be as large as or larger than a mature stage.
4. **Do not merely scale the same drawing.** Each stage must develop real structure: a progressively thicker trunk, clearer branching logic, a more complex canopy, and a silhouette that changes across the lifecycle.
5. **Stage 01 — sprout:** the smallest; young stem / early trunk, very few leaves, no mature canopy yet; no flowers, no fruit.
6. **Stage 02 — sapling:** clearly a young tree; slim trunk, a few branches, small canopy; **no flowers and absolutely no fruit**.
7. **Stage 03 — young:** a young tree; branching and canopy more developed than stage 02 but still not mature; **no flowers, no fruit**.
8. **Stage 04 — flowering-or-mature:** more mature than stage 03. For species with a flowering state, flowers begin to appear here; do not render harvest-ready fruit unless the species gameplay/spec explicitly requires otherwise.
9. **Stage 05 — harvestable / fruiting:** the largest and most complete stage; the fruit/berry/harvest focal point appears here, per species.
10. If stage 05 or a fruit-bearing reference image is used to preserve species identity, that reference may only be used for morphology, leaf/trunk language, and fruit identity; **do not copy flowers/fruit backward into stages 01–03**.
11. Tree sprites must not bake soil, pots, ground tiles, or environment into the master artwork unless the asset spec explicitly requires it.

The generation prompt for a full fruit-tree set must explicitly contain equivalent constraints:

```text
OUTPUT REQUIREMENT: Generate exactly five separate image assets, not one composite image and not a sprite sheet. One output image per lifecycle stage: stage-01, stage-02, stage-03, stage-04, stage-05.

ANCHOR REQUIREMENT: All five images must use the exact same canvas size and the exact same root-origin coordinate. The lowest/root contact point of the trunk must remain fixed across all five outputs. Do not center each tree independently.

GROWTH REQUIREMENT: Tree size and structural complexity must increase monotonically from stage 01 through stage 05. Each successive stage must be visibly larger than the previous stage while preserving believable biological growth.

LIFECYCLE REQUIREMENT: stage-02 is strictly a sapling — foliage only, no flowers and absolutely no fruit. stage-03 is a young vegetative tree — no flowers and no fruit. Flowers begin only at stage-04 when applicable; harvestable fruit appears only at stage-05.
```

---

## 5. Size system

Do not ship master artwork directly into runtime.

### 5.1 Master generation size

| Asset class | Master target |
|---|---:|
| Small crop / weed / pest | 512×512 |
| Medium crop / herb | 768×768 |
| Aquatic crop | 768×768; lotus may use 1024×1024 if canopy/flower breathing room is needed |
| Tree / animal-sized farm asset | 1024×1024 |
| Tall/special tree | 1024×1280 or a square master with padding |
| Tool icon | 512×512 |

### 5.2 Runtime semantic size classes

| Class | Suggested display range | Used for |
|---|---:|---|
| S | 64–96 px | weed, pest, tiny growth stage, small tool |
| M | 128–160 px | rice, carrot, herbs, water mimosa, water spinach, mature low crop |
| L | 192–256 px | corn, coffee, dragon fruit, lotus |
| XL | 256–384 px | mango, pomelo, coconut, rubber, fruit trees |

The final runtime size will be tuned to the game's camera and world scale, but perceived scale must stay consistent across assets.

---

## 6. Grounding / surface systems

### 6.1 Soil system

`farm/soil` is the foundation of all visual calibration.

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

- crops, weeds, and pests must be placeable on the standard soil tile;
- wet/dry states must read clearly without becoming oversaturated;
- footprint and camera angle must stay fixed;
- weeds/pests are not baked permanently into the soil texture;
- crop shadows must be compatible with the soil tile's grounding.

### 6.2 Aquatic crop area

The aquatic crop area is a farming zone on shallow water / a pond, used for lotus, water mimosa, and water spinach.

Rules:

- `farm/aquatic-crops` contains plant artwork only;
- water surfaces / pond tiles, pond edges, and ripple FX belong to a separate environment/water system and are not baked into crop masters;
- every stage of the same species shares one waterline/root anchor so swapping sprites does not jump position;
- do not center the plant by canvas; keep the gameplay anchor stable;
- contact ripples/shadows are optional overlays/FX only;
- do not expose submerged rhizomes/roots in the normal world sprite;
- when placed together with fish/pond gameplay, foliage must not cover the water so much that fish or interaction markers lose readability;
- keep the same camera angle, upper-left lighting, and perceived world scale as the rest of the farm.

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
- green must differ enough from crop foliage to stay recognizable;
- runtime may apply light random variant/rotation.

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

First priority:

```text
caterpillar_single
caterpillar_cluster
beetle_single
aphid_cluster
```

Rules:

- exaggerate scale slightly so they read in gameplay;
- the pest sprite and the infestation marker may be two different assets;
- do not render in a realistic gross / insect-horror direction;
- keep the cute/readable Mayhoa style.

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

- gameplay interaction icons, not realistic illustrations;
- extremely clear silhouettes;
- a slight 3/4 angle when appropriate;
- slightly higher contrast than world assets;
- do not bake button backgrounds into the artwork;
- hover/disabled/pressed states are preferably handled by UI/runtime rather than generating separate assets.

### Minimal artwork state

```text
idle
active   # only when the interaction animation needs a separate sprite
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

`masters/` stores high-quality source artwork. `runtime/` stores versions resized/optimized for the game.

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

Do not encode resolution directly in the logical filename; resolution is separated by runtime folders such as `1x/` and `2x/`.

---

## 12. Production phases

# Phase 0 — Calibration Set

Goal: lock perspective, scale, outline, palette, shadow, foliage density, and perceived detail level before creating the full production pack.

Generate representative states first:

1. `soil_tilled`
2. `rice_stage-05_harvestable`
3. `corn_stage-05_harvestable`
4. `mango_stage-05_fruiting`
5. `weed_small_01`
6. `caterpillar_single`
7. `tool_watering-can_idle`

### Exit criteria

Move to Phase 1 only when all 7 assets:

- look like they belong to the same game;
- share the same lighting logic;
- have plausible relative scale;
- use consistent outline and detail density;
- can be placed on the same soil tile without camera/perspective mismatch;
- still read well at runtime size.

---

# Phase 1 — Soil Foundation

Generate the full soil states:

- empty
- tilled
- wet
- planted
- dry
- harvested

Then lock the soil tile as the reference foundation for all crop production.

---

# Phase 2 — Core Crop Pack

Generate full growth stages for:

1. rice
2. corn
3. carrot

Five stages each.

The goal of this phase is to lock the growth-stage language for the whole crop system.

---

# Phase 3 — Herb / Low Crop Pack

Generate full growth stages for:

1. tonkin-jasmine
2. culantro
3. mint

Five stages each unless gameplay requires fewer.

---

# Phase 4 — Core Fruit Tree Pack

Generate:

1. mango
2. pomelo
3. lemon
4. star-apple

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

Five stages each, following the standard fruit tree/perennial lifecycle.

---

# Phase 6 — Special Structure Pack

Generate:

1. coconut
2. dragon-fruit

Five stages each; state names may specialize by the species' structure.

Each needs its own visual calibration for footprint and vertical scale, but must still follow the shared world scale.

---

# Phase 7 — Industrial / Perennial Pack

Generate:

1. coffee
2. rubber

Five stages each, following the standard perennial lifecycle.

The coffee harvest state needs berry focal points. The rubber harvest state may use a tapping representation if gameplay confirms that mechanic.

---

# Phase 8 — Aquatic Crop Area Pack

Generate full growth stages for:

1. lotus
2. water-mimosa
3. water-spinach

Five stages each.

Specific acceptance requirements:

- a stable shared waterline/root anchor across every stage;
- no water surface or pond edge baked into the plant sprite;
- the final lotus stage must read clearly through leaves plus a flower or seed-pod focal point;
- lotus gameplay mapping supports `lotus_flower`, `lotus_rhizome`, `lotus_stem`, `lotus_seed` without requiring four independent lifecycles;
- water mimosa and water spinach must have sufficiently different silhouettes at runtime size;
- test composition on at least one neutral water tile before approval.

---

# Phase 9 — Weed Pack

Generate the full weed variants:

- 2 small
- 2 medium
- 1 dense

Test the overlay with at least rice, corn, carrot, and a mango/fruit-tree plot when applicable.

---

# Phase 10 — Pest Pack

Generate:

- caterpillar single
- caterpillar cluster
- beetle single
- aphid cluster
- snail
- leaf bug

Test on crops with low foliage, tall crops, and tree foliage.

---

# Phase 11 — Farming Tool Pack

Generate:

- harvest hand
- watering can
- pest catcher
- pruning shears
- shovel

The tool pack must be tested at its own UI interaction size, not evaluated by the world scale of crops/trees.

---

## 13. Batch execution rule

Every phase runs through this loop:

```text
PLAN -> GENERATE -> REVIEW -> REVISE -> APPROVE -> SYNC -> VERIFY -> OPTIMIZE -> COMMIT
```

### Asset sync transport

Claude-in-Chrome downloads images from ChatGPT straight to the local disk. **Do not use Google Drive, do not use `gws`.**

Canonical transport flow:

```text
ChatGPT Create image output
-> open the image in the fullscreen viewer, click the "Save" button
-> the file lands in ~/Downloads, named "ChatGPT Image <date time>.png"
-> identify the new file by timestamp
-> verify MIME, dimensions, real alpha
-> move into `.ai-bridge/<species>/`; only approved versions go into `masters/...`
```

Safe new-file identification even for a multi-image batch — set the marker **before** clicking Save:

```bash
MARK=$(mktemp); touch "$MARK"
# ... click Save one at a time, in the correct stage order ...
find ~/Downloads -name 'ChatGPT Image*.png' -newer "$MARK" -print0 | xargs -0 ls -tr
# oldest -> newest = exactly the order you clicked
```

Rules:

- The download button is named **"Save"** and exists only in the fullscreen viewer (same bar as Remove BG / Erase). The chat pane has NO Download button.
- This approach only works when Chrome and the repo are on the **same machine** — which is the case for the current setup. If they are split across machines, you must go back to using a staging layer.
- Do not rely on ChatGPT `openai/fileParams` for canonical asset transport.
- Do not invoke local Codex, Codex CLI, `codex exec`, or any Codex-backed executor to sync assets.
- Keep raws + prompts in `.ai-bridge/<species>/`; only approved assets are moved into `masters/`.
- The downloaded file must be verified as the correct image type and as having real alpha before it is accepted into the canonical asset set.

> **History:** before 2026-09-05 this flow went through Google Drive + `gws` because CodexPro2 could not take
> binaries directly from Create image. Moving to Claude-in-Chrome removed that whole leg: one fewer connector
> call, one fewer Allow click, and it eliminated the OAuth-token-expiry risk entirely — the `gws` token was
> revoked at exactly the moment it was needed (2026-09-05).

Do not generate the next phase before the current phase meets its acceptance criteria, unless the asset is only created experimentally and will not be merged into the production set.

---

## 14. QC checklist for every asset

- correct species / object identity;
- correct Mayhoa art style;
- clear silhouette at gameplay size;
- not overly vector-clean;
- not glossy;
- not neon;
- not over-detailed;
- dark-chromatic, selective outlines;
- consistent upper-left lighting;
- soft shadows;
- believable organic asymmetry;
- clear crop/tree structural logic;
- relative scale that suits the soil and neighboring assets;
- clean transparent background;
- no unnecessary text / UI / scene background;
- sufficient breathing room in the master;
- runtime export with no halo, blur, or silhouette loss.

---

## 15. Git workflow

### Per production batch

Each phase/batch is committed separately after approval.

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
- duplicate variants no longer in use;
- masters with broken composition;
- runtime exports that have not passed QC.

If exploratory generations need to be kept, put them in a separate area and do not treat them as canonical runtime assets.

---

## 16. Estimated initial scope

Estimated initial production sprite masters:

- Soil: ~6
- Field crops: ~30
- Aquatic crops: ~15
- Trees/perennials: ~50
- Weeds: ~5
- Pests: ~6
- Tools: ~5

Total roughly **115+ master sprites**, excluding revisions, harvest-item artwork, and optional UI/animation variants.

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

After Phase 0 is approved, artwork will be generated sequentially in this order unless gameplay priority changes.

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

The goal of this task is not asset quantity but locking the visual language for the entire farm pack.

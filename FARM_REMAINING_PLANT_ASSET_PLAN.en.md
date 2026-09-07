# Mayhoa — Remaining Plant Asset Generation Plan

**Language:** [Tiếng Việt](FARM_REMAINING_PLANT_ASSET_PLAN.vi.md) · English

**Status:** Ready for parallel execution  
**Project:** Mayhoa  
**Art style:** Mayhoa Nostalgic Hand-Painted Farm Sprite  
**Canonical references:** `MAYHOA_ART_STYLE_SPEC.en.md`, `FARM_ASSET_GENERATION_PLAN.en.md`  
**Purpose:** A checklist and work partition so that several sub-agents can generate the missing plant assets without overlapping.

---

## Status and relationship to the other documents

**Production can be considered finished.** All 7 species in this file's scope (coconut, dragon-fruit, coffee, rubber, lotus, water-mimosa, water-spinach) already have all 5/5 master files in `masters/farm/` — matching the "Still to generate" snapshot in §1 below, which is already fully ticked `[x]`.

A note before reading on: the more detailed checklists in §4–§9 (per-task checkboxes, acceptance criteria, execution waves, final integration checklist) **were not kept in sync** — only `rubber`, `water-mimosa` and `water-spinach` are ticked there, while `coconut`, `dragon-fruit`, `coffee` and `lotus` still show `[ ]` even though the artwork exists and has been through geometry normalization (see §20.1 of `MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.en.md`). Treat **§1 as the correct source for production status**, not the checkboxes further down.

This document complements `FARM_ASSET_GENERATION_PLAN.en.md` (Phase 4–8, the original roadmap for these species) and follows the per-species geometry policy in §9.6 of `MAYHOA_ASSET_GEOMETRY_AND_LAYOUT_SPEC.en.md`.

---

## 1. Current snapshot

Checked directly against `masters/farm/`.

### Completed

Field crops — 6/6 species, each species with all 5 stages:

- [x] rice
- [x] corn
- [x] carrot
- [x] tonkin-jasmine
- [x] culantro
- [x] mint

Fruit trees completed — 6/10 tree/perennial species in the roadmap:

- [x] mango
- [x] pomelo
- [x] lemon
- [x] star-apple
- [x] rambutan
- [x] lychee

### Still to generate

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

Each species is an independent task and by default is assigned to **its own sub-agent**.

Do not split the stages of a single species across several agents, because the 5 stages need:

- the same canvas size;
- the same root-origin / gameplay anchor;
- the same visual language;
- a sequential size increase;
- consistent morphology throughout the lifecycle.

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

The tasks write to separate destination paths, so they can be generated/QC'd in parallel without file conflicts.

---

## 3. Global generation contract

Every sub-agent must read and follow:

1. `MAYHOA_ART_STYLE_SPEC.en.md`
2. `FARM_ASSET_GENERATION_PLAN.en.md`

Mandatory rules:

- [ ] Each species outputs **exactly 5 separate images**; no contact sheet, no sprite sheet, no merging 5 stages into one image.
- [ ] A clean transparent background.
- [ ] Do not bake soil, ground tiles, pond surface, pond edge or scene background into the plant master.
- [ ] The 5 images of the same species must use the same canvas/aspect ratio.
- [ ] The root-origin / gameplay anchor must stay at the **same coordinates** across all 5 stages.
- [ ] Do not center each stage on its own bounding box.
- [ ] Size and structural complexity must increase clearly in stage order 01 < 02 < 03 < 04 < 05.
- [ ] Do not simply scale one and the same image; every stage must develop real structure.
- [ ] Stage 02 must genuinely be the sapling/sprout stage, no flowers, no fruit.
- [ ] Stage 03 is the young vegetative stage, no flowers, no fruit.
- [ ] The harvest focal point appears only at the final stage, unless a species-specific lifecycle explicitly requires otherwise.
- [ ] No text, UI labels, watermarks or decorative clutter.
- [ ] Upper-left lighting, soft painterly rendering, selective dark-chromatic outlines, organic asymmetry.
- [ ] Species identity must read clearly at gameplay size.

### Tree/perennial canvas target

- Normal tree/perennial master: `1024x1024`.
- Tall/special tree: `1024x1280` may be used if needed, but all 5 stages of the same species must be identical.

### Aquatic crop canvas target

- Default `768x768`.
- Lotus may use `1024x1024` if it needs breathing room.
- The same waterline/root anchor across all 5 stages.

---

## 4. Task checklist — Special Structure Pack

### TASK TREE-COCONUT — Coconut (Vietnamese: dừa)

**Destination:** `masters/farm/trees/coconut/`

- [ ] `coconut_stage-01_sprout_v01.png`
- [ ] `coconut_stage-02_sapling_v01.png`
- [ ] `coconut_stage-03_young_v01.png`
- [ ] `coconut_stage-04_mature_v01.png`
- [ ] `coconut_stage-05_fruiting_v01.png`

Species-specific notes:

- stages 01–02 must be small, the trunk not yet developed into a mature palm trunk;
- stage 03 starts to read clearly as a coconut palm silhouette but has no fruit yet;
- stage 04 has a more mature crown, not yet harvest-ready;
- stage 05 has just enough coconut clusters to be recognizable, without overloading the canopy;
- keep the root/base anchor absolutely stable even though the height increases sharply.

Acceptance:

- [ ] 5 separate files.
- [ ] Same anchor.
- [ ] Monotonic height/crown growth.
- [ ] No coconut fruit before stage 05.
- [ ] No soil baked into sprite.

---

### TASK TREE-DRAGON-FRUIT — Dragon Fruit (Vietnamese: thanh long)

**Destination:** `masters/farm/trees/dragon-fruit/`

- [ ] `dragon-fruit_stage-01_sprout_v01.png`
- [ ] `dragon-fruit_stage-02_sapling_v01.png`
- [ ] `dragon-fruit_stage-03_young_v01.png`
- [ ] `dragon-fruit_stage-04_flowering_v01.png`
- [ ] `dragon-fruit_stage-05_fruiting_v01.png`

Species-specific notes:

- the lifecycle must clearly show the cactus climbing/branching structure;
- if a support post/trellis is used as part of the canonical cultivation structure, the support must be consistent between stages and must not turn into an environment scene;
- stage 02 has no flowers/fruit;
- stage 03 has more segments but is still vegetative;
- stage 04 is where flowering begins;
- stage 05 has just enough dragon fruit to be recognizable.

Acceptance:

- [ ] 5 separate files.
- [ ] Same base/support anchor.
- [ ] Clear structural growth, not scaled duplicates.
- [ ] No flower before stage 04.
- [ ] No fruit before stage 05.

---

## 5. Task checklist — Industrial / Perennial Pack

### TASK TREE-COFFEE — Coffee (Vietnamese: cà phê)

**Destination:** `masters/farm/trees/coffee/`

- [ ] `coffee_stage-01_sprout_v01.png`
- [ ] `coffee_stage-02_sapling_v01.png`
- [ ] `coffee_stage-03_young_v01.png`
- [ ] `coffee_stage-04_flowering_v01.png`
- [ ] `coffee_stage-05_berry_v01.png`

Species-specific notes:

- a shrub/tree form lower than the major fruit trees;
- the leaf arrangement and branching must read like a coffee plant;
- stages 01–03 are fully vegetative;
- stage 04 has a moderate amount of white coffee flowers;
- stage 05 has ripe berry focal points, without turning into a tree completely covered in berries.

Acceptance:

- [ ] 5 separate files.
- [ ] Same root anchor.
- [ ] Stage sizes increase evenly.
- [ ] No flower before stage 04.
- [ ] No berry before stage 05.

---

### TASK TREE-RUBBER — Rubber (Vietnamese: cao su)

**Destination:** `masters/farm/trees/rubber/`

- [x] `rubber_stage-01_sprout_v01.png`
- [x] `rubber_stage-02_sapling_v01.png`
- [x] `rubber_stage-03_young_v01.png`
- [x] `rubber_stage-04_mature_v01.png`
- [x] `rubber_stage-05_tapping_v01.png`

Species-specific notes:

- trunk development is the main lifecycle signal;
- stages 01–03 have no tapping hardware;
- stage 04 is a mature tree, with no harvest representation yet;
- stage 05 has a tapping cut/cup representation clear enough for the gameplay to be understood, but without excessive industrial detail;
- the tree must still keep the Mayhoa cute/readable style, not a photorealistic plantation rendering.

Acceptance:

- [ ] 5 separate files.
- [ ] Same root anchor.
- [ ] Trunk thickness/height increases sensibly.
- [ ] No tapping state before stage 05.
- [ ] No soil or plantation scene baked in.

---

## 6. Task checklist — Aquatic Crop Area Pack

### TASK AQUATIC-LOTUS — Lotus (Vietnamese: sen)

**Destination:** `masters/farm/aquatic-crops/lotus/`

- [ ] `lotus_stage-01_planted_v01.png`
- [ ] `lotus_stage-02_sprout_v01.png`
- [ ] `lotus_stage-03_young_v01.png`
- [ ] `lotus_stage-04_budding_v01.png`
- [ ] `lotus_stage-05_flowering_v01.png`

Species-specific notes:

- the plant artwork is separate from the water surface and the pond edge;
- a fixed waterline/root anchor;
- stages 01–03 develop the leaf/stem structure before budding;
- stage 04 has the bud focal point;
- stage 05 reads clearly as lotus through its lotus leaves + flower, and may include a light seed pod if it does not clutter the silhouette;
- `lotus_flower`, `lotus_rhizome`, `lotus_stem`, `lotus_seed` are gameplay item mappings, not 4 separate lifecycle sprites; the harvest/inventory artwork for all 4 of those outputs is deferred to a later item/inventory phase. The current lotus task only needs exactly the 5 lifecycle/world assets above.

Acceptance:

- [ ] 5 separate files.
- [ ] Same waterline/root anchor.
- [ ] No baked water/pond/ripple.
- [ ] No flower before stage 05; stage 04 is budding only.
- [ ] Stage 05 silhouette is still readable at runtime size.

---

### TASK AQUATIC-WATER-MIMOSA — Water Mimosa (Vietnamese: rau nhút)

**Destination:** `masters/farm/aquatic-crops/water-mimosa/`

- [x] `water-mimosa_stage-01_planted_v01.png`
- [x] `water-mimosa_stage-02_sprout_v01.png`
- [x] `water-mimosa_stage-03_young_v01.png`
- [x] `water-mimosa_stage-04_mature_v01.png`
- [x] `water-mimosa_stage-05_harvestable_v01.png`

Species-specific notes:

- the form leans towards a horizontal cluster on the waterline;
- growth is mainly expressed through stem count, leaf density and spread;
- keep the identity of water mimosa, do not let the silhouette be confused with water spinach;
- do not bake in the water surface.

Acceptance:

- [ ] 5 separate files.
- [ ] Same waterline/root anchor.
- [ ] Horizontal spread increases progressively.
- [ ] Distinct species identity.
- [ ] No water/pond baked into sprite.

---

### TASK AQUATIC-WATER-SPINACH — Water Spinach (Vietnamese: rau muống)

**Destination:** `masters/farm/aquatic-crops/water-spinach/`

- [x] `water-spinach_stage-01_planted_v01.png`
- [x] `water-spinach_stage-02_sprout_v01.png`
- [x] `water-spinach_stage-03_young_v01.png`
- [x] `water-spinach_stage-04_mature_v01.png`
- [x] `water-spinach_stage-05_harvestable_v01.png`

Species-specific notes:

- the form spreads horizontally, but the stem/leaf language must differ from water mimosa;
- stage progression comes from stem count, leaf mass and spread;
- the harvestable stage looks fresh and edible, not overgrown/messy like a weed;
- do not bake in the water surface.

Acceptance:

- [ ] 5 separate files.
- [ ] Same waterline/root anchor.
- [ ] Structural growth is clear at every stage.
- [ ] Distinct from water-mimosa at gameplay size.
- [ ] No water/pond baked into sprite.

---

## 7. Recommended execution waves

All 7 species can run in parallel if there are enough agents. To reduce the risk of visual drift, use 2 waves:

### Wave A — tree/perennial

- [ ] TREE-COCONUT
- [ ] TREE-DRAGON-FRUIT
- [ ] TREE-COFFEE
- [x] TREE-RUBBER

Once Wave A is complete:

- [ ] cross-QC the scale between the 4 species against the mango/pomelo/lemon reference;
- [ ] confirm root anchor consistency within each set;
- [ ] approve before syncing the canonical masters.

### Wave B — aquatic crops

- [ ] AQUATIC-LOTUS
- [x] AQUATIC-WATER-MIMOSA
- [x] AQUATIC-WATER-SPINACH

Once Wave B is complete:

- [ ] cross-QC the waterline anchors;
- [ ] test composition on a neutral water tile;
- [ ] verify that the lotus / water mimosa / water spinach silhouettes are not mistaken for one another.

---

## 8. Per-agent handoff template

Each sub-agent takes exactly one task above and reports in this format:

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

A sub-agent must not change the naming convention on its own or write files into another agent's task.

---

## 9. Final integration checklist

Only tick a species as complete after generation + QC + sync are all done.

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

Not included:

- weeds;
- pests;
- farming tools;
- inventory item artwork;
- pond/water surface tiles;
- runtime resizing/optimization;
- optional regrowing states;
- animation frames beyond the core 5-stage lifecycle.

The items above still belong to the overall farm roadmap but are not part of the **remaining plant generation** in this checklist.
